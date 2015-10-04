#!/usr/bin/env python2
'''
  @Author: Josh Snider
'''
import argparse
import getpass
from github import Github
import os
import subprocess
import sys

def get_repos(gh_agent):
  ''' Get the repos to clone.'''
  user = gh_agent.get_user().login
  for repo in gh_agent.get_user().get_repos():
    if repo.full_name.startswith(user):
      yield repo
  #TODO Get org repos.

def make_args():
  ''' Make the parser for the command line.'''
  parser = argparse.ArgumentParser(
    description="Clone all of your GitHub repos. Including private repos.")
  parser.add_argument('--user', help="Your github username")
  parser.add_argument('--token',
    help="OAuth token. Alternative to password authentication.")
  parser.add_argument('--dest',
    help="Repository to clone your repos into. (default: current directory)")
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

def main():
  ''' Sync a user's GitHub repos with the current machine.'''
  parser = make_args()
  args = parser.parse_args()
  gh_agent = make_github_agent(args)
  if args.dest:
    if not os.path.exists(args.dest):
      os.makedirs(args.dest)
    os.chdir(args.dest)
  for repo in get_repos(gh_agent):
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
