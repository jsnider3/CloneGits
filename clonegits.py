import getpass
from github import Github

user = raw_input('User:')
passw = getpass.getpass('Password:')
g = Github(user, passw)
for repo in g.get_user().get_repos():
  print(repo.full_name)
  # TODO Clone repos
