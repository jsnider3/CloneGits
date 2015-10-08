import os
import subprocess
import unittest

class Tests(unittest.TestCase):

  def test_basic(self):
    ''' Test we can run without crashing.'''
    token = os.environ['OAuth']
    assert len(token)
    subprocess.check_output(['python', 'clonegits.py', '--token', token])

if __name__ == '__main__':
  unittest.main()
