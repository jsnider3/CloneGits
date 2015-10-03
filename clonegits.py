#!/usr/bin/env python2
'''
  @Author: Josh Snider
'''
import argparse
import getpass
from github import Github
import os
import subprocess

def main():
  parser = argparse.ArgumentParser(
    description="Clone all of your GitHub repos. Including private repos.");
  parser.add_argument('--user', help="Your github username")
  parser.add_argument('--token',
    help="OAuth token. Alternative to password authentication.")
  parser.add_argument('--dest',
    help="Repository to clone your repos into. (default: current directory)")
  parser.add_argument('--nopull', action='store_true',
    help="Disables updating preexisting repos. (default: false)")
  args = parser.parse_args()
  g = None
  if args.token:
    g = Github(args.token)
  else:
    user = args.user
    if not user:
      user = raw_input('User:')
    if args.dest:
      os.chdir(args.dest)
    passw = getpass.getpass('Password:')
    g = Github(user, passw)
  user = g.get_user().login
  for repo in g.get_user().get_repos():
    if repo.full_name.startswith(user):
      if not os.path.exists(repo.name): #Check directory doesn't exist.
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
