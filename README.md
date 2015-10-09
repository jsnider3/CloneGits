# CloneGits
[![Build Status](https://travis-ci.org/jsnider3/CloneGits.svg?branch=master)](https://travis-ci.org/jsnider3/CloneGits)
[![License](https://img.shields.io/github/license/jsnider3/CloneGits.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

A tool to clone all of a user's GitHub repos to the local
machine.

## Usage

Run `python2 clonegits.py` either run it in the target directory
or use `--dest` to supply it with a directory to download into.

It will ask for your github username and password and then proceed
to clone all of your repos on GitHub.

## Requirements

This only requires PyGithub, which can be installed with
`pip install pygithub`.
