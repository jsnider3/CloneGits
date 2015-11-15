# CloneGits
[![Build Status](https://travis-ci.org/jsnider3/CloneGits.svg?branch=master)](https://travis-ci.org/jsnider3/CloneGits)
[![License](https://img.shields.io/github/license/jsnider3/CloneGits.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

A tool to clone all of a user's GitHub repos to the local
machine.

## Usage

Run `python2 clonegits.py` either run it in the target directory
or use `--dest` to supply it with a directory to download into.

## Requirements

This only requires PyGithub, which can be installed with
`pip install pygithub`.

### Authentication

You have the option to supply a GitHub OAuth token with `--token`,
otherwise authentication with be done with username/password. You may
supply a username as an arg with `--user`.

To ensure that private repos are downloaded correctly, you should
have a GitHub authentication stored with a git credential helper.

## Rulesets

As an advanced option, you can use json to create a ruleset specifying
in detail how you want repos to be placed, based on who you forked it
from, what language it is, and what the owning organization is. See
samplerules.json for an example.

Your json file should consist of an array of objects. Each object is
required to have a dest field which says what directory matching repos
should be stored in. It may have optional owner, language, and org fields.
These are python regexes, which if not supplied default to matching
everything. The language in a rule is matched against the most common
language in the repository, which can be seen on its GitHub page. The owner
in a rule is matched against the name of the repository's owner
(e.g. "Josh Snider"). If the repository is a fork, the owner is the name
of the owner of the repository you forked it from. The org is matched
against the organization that owns the repository, which is the empty
string if no organization does.
