#!/usr/bin/env python2
'''
  @Author: Josh Snider
'''
import argparse
import getpass
from github import Github
import os
import subprocess

parser = argparse.ArgumentParser(
  description="Clone all of your GitHub repos. Including private repos.");
parser.add_argument('--user', help="Your github username")
parser.add_argument('--dest',
  help="Repository to clone your repos into. (default: current directory)")
args = parser.parse_args()
user = args.user
if not user:
  user = raw_input('User:')
if args.dest:
  os.chdir(args.dest)
passw = getpass.getpass('Password:')
g = Github(user, passw)
for repo in g.get_user().get_repos():
  if repo.full_name.startswith(user):
    if not os.path.exists(repo.name): #Check directory doesn't exist.
      print(repo.full_name)
      subprocess.call(["git", "clone",
                     "https://github.com/" + repo.full_name])
    else:
      print("Skipping " + repo.name)
