"""
Generate the version changes table for changelog

Usage:

python3 tools/package_table.py --before 4.5.5 --after 5.0.0 | pbcopy
"""

import argparse
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from subprocess import check_output

import yaml
from packaging.requirements import Requirement

repo_root = Path(__file__).absolute().parents[1]


@dataclass(kw_only=True)
class Package:
    name: str
    url: str = ""
    changelog_template: str
    note: str = ""


@dataclass(kw_only=True)
class PythonPackage(Package):
    pypi_name: str | None = None
    note: str = "Run in the `hub` pod"

    def get_version(self, revision="HEAD") -> str:
        hub_requirements = Path("images/hub/requirements.txt")
        requirements_dict = load_requirements(hub_requirements, revision=revision)
        name = self.pypi_name or self.name
        return requirements_dict.get(name, None)


@dataclass(kw_only=True)
class Image(Package):
    values_path: str

    def get_version(self, revision="HEAD") -> str:
        """Get image version from a values.yaml"""
        values = load_values("jupyterhub/values.yaml", revision=revision)
        parts = self.values_path.split(".")
        value = values
        for part in parts:
            if part.isdigit():
                part = int(part)
            value = value[part]
        if isinstance(value, dict):
            return value["tag"]
        elif isinstance(value, str):
            return value.partition(":")[-1]
        else:
            raise TypeError(f"{value!r}")


# the actual packages to check
# order is preserved in the table
packages = [
    PythonPackage(
        name="jupyterhub",
        changelog_template="https://jupyterhub.readthedocs.io/en/{version}/reference/changelog.html",
    ),
    PythonPackage(
        name="kubespawner",
        pypi_name="jupyterhub-kubespawner",
        changelog_template="https://jupyterhub-kubespawner.readthedocs.io/en/{version}/changelog.html",
    ),
    PythonPackage(
        name="oauthenticator",
        changelog_template="https://oauthenticator.readthedocs.io/en/stable/changelog.html",
    ),
    PythonPackage(
        name="nativeauthenticator",
        pypi_name="jupyterhub-nativeauthenticator",
        changelog_template="https://native-authenticator.readthedocs.io/en/{version}/",
    ),
    PythonPackage(
        name="jupyterhub-idle-culler",
        changelog_template="https://github.com/jupyterhub/jupyterhub-idle-culler/blob/{version}/CHANGELOG.md",
    ),
    Image(
        name="configurable-http-proxy",
        values_path="proxy.chp.image",
        changelog_template="https://github.com/jupyterhub/configurable-http-proxy/blob/{version}/docs/source/changelog.md",
        note="Run in the `proxy` pod",
    ),
    Image(
        name="traefik",
        url="https://github.com/traefik/traefik",
        values_path="proxy.traefik.image",
        changelog_template="https://github.com/traefik/traefik/blob/{version}/CHANGELOG.md",
        note="Run in the `autohttps` pod",
    ),
    Image(
        name="kube-scheduler",
        url="https://github.com/kubernetes/kube-scheduler",
        values_path="scheduling.userScheduler.image",
        changelog_template="https://github.com/kubernetes/kubernetes/blob/{version}/CHANGELOG",
        note="Run in the `user-scheduler` pod(s)",
    ),
]


@lru_cache
def read_file(path: Path | str, revision: str = "HEAD"):
    """Read a specific git version of a file"""
    path = Path(path)
    if revision == "HEAD":
        return path.read_text()
    else:
        return check_output(
            ["git", "show", f"{revision}:{path}"],
            cwd=repo_root,
            text=True,
        )


def parse_requirements_txt(requirements_txt: str) -> dict[str, str]:
    """
    return dict of {"pkg":"version"}

    assumes frozen requirements file with only `pkg==version`,
    but that's what we have.
    """

    requirements = {}
    for line in requirements_txt.splitlines():
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        req = Requirement(line)
        requirements[req.name] = str(req.specifier).strip("=")
    return requirements


@lru_cache
def load_requirements(path: Path | str, revision: str = "HEAD"):
    """Load a requirements.txt as a dict of {pkg: version} for a specific git revision"""
    return parse_requirements_txt(read_file(path, revision))


@lru_cache
def load_values(path: Path | str, revision: str = "HEAD"):
    """Load a values.yaml for a specific git revision"""
    return yaml.safe_load(read_file(path, revision))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", type=str, default=None)
    parser.add_argument("--after", type=str, default="HEAD")
    opts = parser.parse_args()
    before_rev = opts.before
    next_rev = opts.after
    if before_rev is None:
        before_rev = check_output(
            ["git", "describe", "--tags", "--abbrev=0"], cwd=repo_root, text=True
        ).strip()

    print(f"Highlighting some package updates from chart {before_rev} to {next_rev}:")
    print()
    print(
        f"| Dependency | Version in {before_rev} | Version in {next_rev} | Changelog link | Note |"
    )
    print("| --- | --- | --- | --- |--- |")
    for package in packages:
        before = package.get_version(before_rev)
        after = package.get_version()
        changelog_url = package.changelog_template.format(version=after)
        url = package.url or f"https://github.com/jupyterhub/{package.name}"
        line = f"| [{package.name}]({url}) | {before} | {after} | [Changelog]({changelog_url}) | {package.note} |"
        if after == before:
            # exclude unchanged packages from the table
            print("UNCHANGED:", line, file=sys.stderr)
        else:
            print(line)

    print()
    print("For a detailed list of Python dependencies in the `hub` pod's image,")
    print(
        "inspect the [images/hub/requirements.txt] file and use its git history to see what changes between tagged versions."
    )


if __name__ == "__main__":
    main()
