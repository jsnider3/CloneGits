import clonegits
from github import Github
import os
import subprocess
import unittest

class Tests(unittest.TestCase):
  ''' Testcases assume that my OAuth token is present in the environment
      as the environment variable OAuth.'''

  def delete_dirs(self, path):
    ''' Delete all directories in given path.'''
    for target in os.listdir(path):
      if os.path.isdir(target) and target != '.git':
        subprocess.call(['rm', '-rf', target])

  def tearDown(self):
    '''Clean up after ourselves.'''
    self.delete_dirs(os.getcwd())

  def test_basic(self):
    ''' Test we can run without crashing.'''
    token = os.environ['OAuth']
    assert len(token)
    subprocess.check_output(['python', 'clonegits.py', '--token', token])

  def test_public_repo(self):
    ''' Test we can get a public repo.'''
    token = os.environ['OAuth']
    subprocess.check_output(['python', 'clonegits.py', '--token', token])
    assert "CloneGits" in os.listdir(os.getcwd())

  def test_ruleset_fork(self):
    ''' Test we check if the original owner matches for forks. '''
    kwargs = {}
    kwargs["rules_file"] = "samplerules.json"
    rules = clonegits.Ruleset(**kwargs)
    gh_agent = Github()
    repo = gh_agent.get_repo('jsnider3/tarpon')
    assert rules.get_dest(repo) == '/tmp/gits/kunal'

  def test_ruleset_language(self):
    ''' Test we check if the language matches. '''
    kwargs = {}
    kwargs["rules_file"] = "samplerules.json"
    rules = clonegits.Ruleset(**kwargs)
    gh_agent = Github()
    repo = gh_agent.get_repo('jsnider3/Workspace')
    assert rules.get_dest(repo) == '/tmp/gits/java'

  def test_ruleset_owner(self):
    ''' Test we check if the owner matches. '''
    kwargs = {}
    kwargs["rules_file"] = "samplerules.json"
    rules = clonegits.Ruleset(**kwargs)
    gh_agent = Github()
    repo = gh_agent.get_repo('jsnider3/HoneyBadger')
    assert rules.get_dest(repo) == '/tmp/gits'

  def test_ruleset_default(self):
    ''' Test we work if noone matches. '''
    kwargs = {}
    kwargs["rules_file"] = "samplerules.json"
    rules = clonegits.Ruleset(**kwargs)
    gh_agent = Github()
    repo = gh_agent.get_repo('torvalds/linux')
    print(rules.get_dest(repo))
    assert rules.get_dest(repo) == os.getcwd()

  #def test_private_repo(self):
  #  ''' Test we can get a private repo.'''
  #  token = os.environ['OAuth']
  #  subprocess.check_output(['python', 'clonegits.py', '--token', token])
  #  assert "Resume" in os.listdir(os.getcwd())

if __name__ == '__main__':
  unittest.main()
