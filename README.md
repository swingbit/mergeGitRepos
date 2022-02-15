# mergeGitRepos

`mergeGitRepos` is a simple Python script to merge several Git repositories into one, preserving history and mapping branches.

## Features
- Simple Yaml configuration
- Safe. It works on checkouts of the original repositories and creates a new local repository. Nothing is ever pushed anywhere.
- Each source repository becomes a subfolder in the new repository, optionally renamed
- Explicit mapping of which source branches need to be merged into which destination branch

## Requirements
- Python 3
- git
- [git filter-repo](https://github.com/newren/git-filter-repo)

## Usage
- DO NOT use this scrpt in a folder with your existing repos. Start in an empty folder.
- check out `mergeGitRepos` and move into it.
- copy `mergeGitRepos.conf.template` into `mergeGitRepos.conf`
- edit `mergeGitRepos.conf`
- run `./mergeGitRepos.py` (`--help` for help)

