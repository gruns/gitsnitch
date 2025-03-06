<div align="center">
  <img src="logo.svg" width="234px" height="300px" alt="GitSnitch">
</div>

# GitSnitch

`gitsnitch` is a simple tool that finds and prints a GitHub user's email
addresses.

Give `gitsnitch` a GitHub username or profile URL, like `gruns` or
https://github.com/gruns, and it finds and prints that user's email
addresses by examining commits across their GitHub repos.

### How GitSnitch Works

To use, provide `gitsnitch` with a GitHub username or profile URL and
let it go to work. `gitsnitch` will, in turn:

  1. Get a list of that user's repos via the GitHub API.
  2. Iterate through each of those repos, prioritizing non-forked repos
     are forked repos.
  3. For each repo, iterate through that repo's commits via the GitHub
     API and examine the committers' email addresses.
  4. Collate a list of each repo's committers and, notably, their
     email addresses.
  5. Output a nicely formatted summary of committers and their email
     addresses, sorted by number of commits.

Example:

```shell
$ gitsnitch https://github.com/gruns
https://github.com/gruns/autokey-to-espanso
Ansgar Grunseid  grunseid@gmail.com  2 commits, latest on Jan 07, 2023

https://github.com/gruns/furl
Ansgar Grunseid  grunseid@gmail.com   23 commits, latest on Jun 28, 2022
Ben Greiner      code@bnavigator.de    3 commits, latest on Mar 29, 2021
Tim Gates        tim.gates@iress.com   1 commits, latest on Jul 30, 2022

https://github.com/gruns/fallout-sonora-translation
Ansgar Grunseid  grunseid@gmail.com  7 commits, latest on Sep 22, 2023

...
```

That's it. Simple.

By default, this script does not need a GitHub API token because GitHub
API endpoints, like https://api.github.com/users/gruns/repos, can be
accessed without an API token at a low rate limit. However, if you
encounter API rate limits, like

```python
Exception: Error fetching repositories: {"message":"API rate limit exceeded for xxx.xxx.xxx.xxx. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)", "documentation_url": "https://docs.github.com/rest/..."}
```

you'll need to create an API token and add it your environment. To
create an API token for `gitsnitch`:

   1. Head to https://github.com/ and log in to your account.
   2. Open your profile picture in the top-right corner and click `Settings`.
   3. Click `Developer settings` in the left-hand sidebar.
   4. Under `Developer settings`, click `Personal access
      tokens`->`Tokens (classic)`.
   5. Click `Generate new token`. Then select at least `read:user` and
      `user:email` under `user`.
   6. Click `Generate token`.
   7. Copy the generated token. Be sure to save it; you won't be able
      to view it again.

Then add this token to your environment with

```shell
export GITHUB_TOKEN=<your_api_token>
```

Finally, re-run `gitsnitch` as normal. Boom.


### Installation

Installing GitSnitch with pip is easy.

```
$ pip3 install gitsnitch
```