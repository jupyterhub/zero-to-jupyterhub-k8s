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
"""

import os
from github import Github
import dateutil
from dateutil.parser import parse

gh = Github(login_or_token=os.environ['GITHUB_API_TOKEN'].strip())


def get_all_contributors(repo, from_date, to_date):
    def include(date):
        return from_date < date.replace(tzinfo=dateutil.tz.tzlocal()) < to_date
    repo = gh.get_repo(repo)
    issues = repo.get_issues(state='all')
    pulls = repo.get_pulls(state='closed')

    users = set()


    for i in issues:
        if include(i.created_at):
            users.add((i.user.login, i.user.name))
        for c in i.get_comments():
            if include(c.created_at):
                users.add((c.user.login, c.user.name))


    for p in pulls:
        if include(p.created_at):
            users.add((p.user.login, p.user.name))

        # get_comments returns review comments too. use get_issue_comments.
        for c in p.get_issue_comments():
            if include(c.created_at):
                users.add((c.user.login, c.user.name))

        for rc in p.get_review_comments():
            if include(rc.created_at):
                users.add((rc.user.login, rc.user.name))
    return users


if __name__ == '__main__':
    # Dates below should be updated before releasing a new version of the helm chart
    #users = get_all_contributors('jupyterhub/zero-to-jupyterhub-k8s', parse('Mon Aug 13 13:37:51 2018 -0800'), parse('Sun Aug 19 08:00:00 2018 +0200'))
    users = get_all_contributors('jupyterhub/zero-to-jupyterhub-k8s', parse('Mon Jan 29 13:37:51 2018 -0800'), parse('Sun Aug 19 08:00:00 2018 +0200'))
    users |= get_all_contributors('jupyterhub/kubespawner', parse('Wed Jan 24 13:31:03 2018 +0100'), parse('Sun Aug 19 08:00:00 2018 +0200'))
    users |= get_all_contributors('jupyterhub/jupyterhub', parse('Tue Nov 07 13:40:00 2018 +0200'), parse('Sat Aug 11 14:53:00 2018 +0200'))
    users |= get_all_contributors('jupyterhub/oauthenticator', parse('Fri Oct 27 17:02:00 2017 +0200'), parse('Sat Aug 11 14:47:00 2018 +0200'))


    for login, name in sorted(users, key=lambda u: u[1].casefold() if u[1] else u[0].casefold()):
        if name is None:
            name = login
        print("[{name}](https://github.com/{login})".format(name=name, login=login))
