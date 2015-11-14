#!/usr/bin/env python2
'''
  @Author: Josh Snider
'''
import argparse
import getpass
from github import Github
import json
import os
import re
import subprocess
import sys

class Rule(object):
  def __init__(self, src):
    self.owner = re.compile(".*")
    self.org = re.compile(".*")
    self.lang = re.compile(".*")
    if "owner" in src:
      self.owner = re.compile(src["owner"])
    if "org" in src:
      self.org = re.compile(src["org"])
    if "language" in src:
      self.lang = re.compile(src["language"])
    assert "dest" in src
    self.dest = src["dest"]

  def matches(self, repo):
    org_name = ""
    if repo.organization:
      org_name = repo.organization.name
    owner_name = repo.owner.name
    if repo.parent:
      owner_name = repo.parent.owner.name
    return (self.owner.match(owner_name) and
           (self.org.match(org_name)) and
           (self.lang.match(repo.language)))

class Ruleset(object):
  def __init__(self, **kwargs):
    if "default" in kwargs:
      self.default = kwargs["default"]
    else:
      self.default = os.getcwd()
    self.rules = []
    if "rules_file" in kwargs:
      with open(kwargs["rules_file"]) as src:
        json_data = src.read()
        for rule_src in json.loads(json_data):
          self.rules.append(Rule(rule_src))

  def get_dest(self, repo):
    ''' Get the destination to store the given repo.'''
    dest = None
    for rule in self.rules:
      if rule.matches(repo):
        dest = rule.dest
        break
    if dest == None:
      dest = self.default
    if not os.path.exists(dest):
      os.makedirs(dest)
    return dest

def get_repos(gh_agent):
  ''' Get the repos to clone.'''
  user = gh_agent.get_user().login
  for repo in gh_agent.get_user().get_repos():
    if repo.full_name.startswith(user):
      yield repo
  for org in gh_agent.get_user().get_orgs():
    for repo in org.get_repos():
      yield repo

def make_args():
  ''' Make the parser for the command line.'''
  parser = argparse.ArgumentParser(
    description="Clone all of your GitHub repos. Including private repos.")
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--user', help="Your github username")
  group.add_argument('--token',
    help="OAuth token. Alternative to password authentication.")
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--dest',
    help="Repository to clone your repos into. (default: current directory)")
  group.add_argument('--rules',
    help="Optional ruleset file specifying how to place files.")
  parser.add_argument('--nopull', action='store_true',
    help="Disables updating preexisting repos. (default: false)")
  return parser

def make_github_agent(cli_args):
  ''' Create the Github object used
      to access their API.'''
  gh_agent = None
  if cli_args.token:
    gh_agent = Github(cli_args.token)
  else:
    user = cli_args.user
    if not user:
      print 'User:',
      user = sys.stdin.readline().strip()
    passw = getpass.getpass('Password:')
    gh_agent = Github(user, passw)
  return gh_agent

def make_rules(cli_args):
  ''' Return the ruleset wanted by the user. '''
  kwargs = {}
  if cli_args.dest:
    kwargs["default"] = cli_args.dest
  if cli_args.rules:
    kwargs["rules_file"] = cli_args.rules
  return Ruleset(**kwargs)

def main():
  ''' Sync a user's GitHub repos with the current machine.'''
  parser = make_args()
  args = parser.parse_args()
  gh_agent = make_github_agent(args)
  rules = make_rules(args)
  for repo in get_repos(gh_agent):
    os.chdir(rules.get_dest(repo))
    if not os.path.exists(repo.name):
      print(repo.full_name)
      subprocess.call(["git", "clone",
                     "https://github.com/" + repo.full_name])
    elif not args.nopull:
      print("Updating " + repo.name)
      os.chdir(repo.name)
      subprocess.call(["git", "pull"])
      os.chdir(os.pardir)
    else:
      print("Skipping " + repo.name)

if __name__ == '__main__':
  main()
