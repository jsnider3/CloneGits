# CloneGits
[![Build Status](https://travis-ci.org/jsnider3/CloneGits.svg?branch=master)](https://travis-ci.org/jsnider3/CloneGits)
[![License](https://img.shields.io/github/license/jsnider3/CloneGits.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

A tool to clone all of a user's GitHub repos to the local
machine.

## Usage

Run `python2 clonegits.py` either run it in the target directory
or use `--dest` to supply it with a directory to download into.

### Authentication
You have the option to supply a GitHub OAuth token with `--token`,
otherwise authentication with be done with username/password. You may
supply a username as an arg with `--user`.

To ensure that private repos are downloaded correctly, you should
have a GitHub authentication stored with a git credential helper.

## Requirements

This only requires PyGithub, which can be installed with
`pip install pygithub`.
