# mergeGitRepos

`mergeGitRepos` is a simple Python script to merge several Git repositories into one, preserving history and mapping branches.

## Features
- Simple Yaml configuration
- Safe. It works on checkouts of the original repositories and creates a new local repository that has no remote defined. Nothing is ever pushed anywhere.
- Each source repository becomes a subfolder in the new repository, optionally renamed
- Explicit mapping of which source branches need to be merged into which destination branch

## Requirements
- Python 3
- git
- [git filter-repo](https://github.com/newren/git-filter-repo)

## Usage
- DO NOT use this script in a folder with your existing repos. Start in an empty folder.
- clone `mergeGitRepos` and move into it.
- copy `mergeGitRepos.conf.template` into `mergeGitRepos.conf`
- edit `mergeGitRepos.conf` (the template is pre-configured with a working example. You can run it as-is the first time and see what it produces).
- run `./mergeGitRepos.py` (`--help` for help)
- go into the new folder and explore content and history.
- if happy, define a git remote (none is defined by the script) and push

