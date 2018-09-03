#!/usr/bin/env python3
"""
Script to list *all* contributors to a given set of repos,
between a set of dates. This includes:

- Everyone who has made a commit merged between those dates
- Everyone who has opened or commented on an issue between those dates
- Everyone who has opened or commented on a PR between those dates

If you think this misses people who make contributions of a specific
form, feel free to add them here!

This script outputs a markdown formatted list of contributors
in casefolded name (username if name not specified) order.

Since we will be making a ton of requests to the GitHub API, you
need a GitHub API Token to use this script. The easiest way is to
just get a Personal Access Token (https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/).
Treat this token similar to how you would treat a password!
You can pass this token in with `GITHUB_API_TOKEN` environment
variable. For example,

  $  GITHUB_API_TOKEN="your-token" ./tools/contributors.py

Note that if you put a space before your command, it does not
get stored in your bash history (by default)!. Look up `HISTCONTROL`
to learn more about this feature of shells.

IMPORTANT:
You may need to run this script twice or so, utilizing the previous runs cached
results in order to handle the request limits by GitHub (5000 / hour).
"""

import os
import dateutil
import requests_cache
from github import Github
from dateutil.parser import parse


requests_cache.install_cache('github')
gh = Github(login_or_token=os.environ['GITHUB_API_TOKEN'].strip())


def get_all_contributors(repo, since):
    since = parse(since)
    def include(date):
        return since < date

    repo = gh.get_repo(repo)
    
    # get all issues created or updated since given date
    issues = repo.get_issues(state='all', since=since)
    pulls = repo.get_pulls(state='closed')

    users = set()

    # FIXME: Asking for c.user.name will invoke a request on top of requesting
    # c.user.login. We are currently doing it multiple times for each user. We
    # should do it only once, if c.user.login did not already exist in the set,
    # or at the end when we have added all users to a set.
    for i in issues:
        if include(i.created_at):
            users.add((i.user.login, i.user.name))
        for c in i.get_comments(since=since):
            users.add((c.user.login, c.user.name))


    for p in pulls:
        if include(p.created_at):
            users.add((p.user.login, p.user.name))

        for c in p.get_issue_comments():
            if include(c.created_at):
                users.add((c.user.login, c.user.name))

        for rc in p.get_review_comments():
            if include(rc.created_at):
                users.add((rc.user.login, rc.user.name))


    return users


if __name__ == '__main__':
    # Dates below should be updated before releasing a new version of the helm
    # chart.
    # NOTE: To save time, all contributions in the associated projects up until
    # the chart's release are considered, this means that if kubespawner got
    # something merged to master, but kubespawner wasn't bumped in this chart,
    # it would still be considered a contribution.
    users = get_all_contributors('jupyterhub/zero-to-jupyterhub-k8s', '2018-01-29')
    users |= get_all_contributors('jupyterhub/kubespawner', '2018-01-24')
    users |= get_all_contributors('jupyterhub/jupyterhub', '2017-11-07')
    users |= get_all_contributors('jupyterhub/oauthenticator', '2017-10-27')


    for login, name in sorted(users, key=lambda u: u[1].casefold() if u[1] else u[0].casefold()):
        if name is None:
            name = login
        print("[{name}](https://github.com/{login})".format(name=name, login=login))
