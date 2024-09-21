#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# GitSnitch - A simple tool that finds a GitHub user's email address(es)
#
# Ansgar Grunseid, with credit to Eric Migicovsky for his insight to use
#   the GitHub API over git itself
# grunseid.com
# grunseid@gmail.com
#
# License: MIT
#

'''
GitSnitch - Find a GitHub user's email address(es)

Usage:
  gitsnitch <usernameOrProfileUrl>
  gitsnitch -h | --help

Arguments:
  <usernameOrProfileUrl>  GitHub username or profile URL, eg gruns or https://github.com/gruns

Options:
  -h --help     Show this screen.

Examples:
  gitsnitch gruns
  gitsnitch https://github.com/gruns
'''

import os
from datetime import datetime

import requests
from furl import furl
from docopt import docopt
try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)


# if you hit github rate limits, eg
#
#   Exception: Error fetching repositories: {"message":"API rate limit
#   exceeded for xxx.xxx.xxx.xxx. (But here's the good news:
#   Authenticated requests get a higher rate limit. Check out the
#   documentation for more details.)", "documentation_url":
#   "https://docs.github.com/rest/..."}
#
# you'll need a github API token. to create a token:
#
#   1. Go to https://github.com/ and log in to your account.
#   2. Click on your profile picture (top-right corner) and go to 'Settings'.
#   3. Click 'Developer settings' in the left-hand sidebar.
#   4. Under 'Developer settings', click 'Personal access
#      tokens'->'Tokens (classic)'.
#   5. Click 'Generate new token'. Then select at least 'read:user' and
#      'user:email' under 'user'.
#   6. Click 'Generate token'.
#   7. Copy the generated token. Be sure to save it; you won't be able
#      to view it again.
# 
# then add your new github api token for auth to your environment
#
#   export GITHUB_TOKEN=<your_api_token>
#
# and run gitsnitch again. voila 🕵️
#
HEADERS = {}
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if GITHUB_TOKEN:
    HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}

NUM_REPOS_TO_PARSE = 10
NUM_COMMITTERS_TO_PRINT_PER_REPO = 10


def getGithubUsername(usernameOrProfileUrl):
    f = furl(usernameOrProfileUrl)

    if f.path and not f.scheme:  # username, eg 'gruns'
        username = usernameOrProfileUrl
    else:  # profile url, eg 'https://github.com/gruns'
        username = f.path.segments[0] if f.path.segments else None

        if f.host != 'github.com' or not username:
            raise ValueError(
                f'Invalid profile URL: {usernameOrProfileUrl}.'
                'Ex: https://github.com/gruns')

    return username


def getRepoCommitters(username, repoName):
    url = f'https://api.github.com/repos/{username}/{repoName}/commits'
    resp = requests.get(url, headers=HEADERS)

    if resp.status_code != 200:
        return []

    committers = {} # email -> (name, numCommits, latestCommitDate)
    commits = resp.json()
    for commit in commits:
        author = commit.get('commit', {}).get('author')

        if not author:
            continue

        author = commit['commit']['author']
        email = author['email']
        name = author['name']
        dateStr = author['date']
        date = datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%SZ')

        # skip emails we don't care about, eg 'foo@users.noreply.github.com'
        # and user@@MacBook-Pro.local
        if email.endswith('noreply.github.com') or email.endswith('.local'):
            continue

        _, numCommits, latestCommitDate = committers.get(
            email, ('ignored', 0, None))

        numCommits += 1
        if latestCommitDate is None or date > latestCommitDate:
            latestCommitDate = date

        committers[email] = (name, numCommits, latestCommitDate)

    return committers


def printTopCommitters(username, repoName, committers):
    print(f'https://github.com/{username}/{repoName}')

    items = [
        (email, name, numCommits, date)
        for email, (name, numCommits, date) in committers.items()]
    committersByNumCommits = sorted(items, key=lambda comitr: comitr[2])[::-1]
    committersByNumCommits = committersByNumCommits[
        :NUM_COMMITTERS_TO_PRINT_PER_REPO]

    longestNameLen = max(len(name) for _, name, _, _ in committersByNumCommits)
    longestEmailLen = max(
        len(email) for email, _, _, _ in committersByNumCommits)
    longestCommitsLen = max(
        len(str(numCommits)) for _, _, numCommits, _ in committersByNumCommits)

    t = (longestNameLen, longestEmailLen, longestCommitsLen)
    fmt = u'{0:<%i}  {1:<%i}  {2:>%i} commits, latest on {3}' % t
    for email, name, numCommits, latestCommitDate in committersByNumCommits:
        dateStr = latestCommitDate.strftime('%b %d, %Y')
        print(fmt.format(name, email, numCommits, dateStr))


def getRepos(username):
    url = f'https://api.github.com/users/{username}/repos'
    resp = requests.get(url, headers=HEADERS)

    if resp.status_code != 200:
        raise Exception(f'Error fetching repositories: {resp.text}.')

    repos = resp.json()

    # only look through NUM_REPOS_TO_PARSE repos, prioritizing non-forked repos
    forkedRepos = [repo for repo in repos if repo['fork']]
    nonForkedRepos = [repo for repo in repos if not repo['fork']]
    repos = (nonForkedRepos + forkedRepos)[:NUM_REPOS_TO_PARSE]

    return repos


def main():
    arguments = docopt(__doc__)  # raises systemexit
    usernameOrProfileUrl = arguments['<usernameOrProfileUrl>']

    username = getGithubUsername(usernameOrProfileUrl) # raises ValueError on invalid url
    repos = getRepos(username)

    for i, repo in enumerate(repos):
        repoName = repo['name']
        committers = getRepoCommitters(username, repoName)
        if not committers:  # empty repo
            continue
        printTopCommitters(username, repoName, committers)

        if i < len(repos) - 1: # all repos but the last
            print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
