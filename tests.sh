$!/usr/bin/env bash
git config --global credential.helper 'cache --timeout=3000'
pylint clonegits.py --disable=F0401 --disable=W0511 --disable=W0311;
python tests.py
