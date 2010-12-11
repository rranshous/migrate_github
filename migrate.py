#!/usr/bin/python

# we are going to go into each of the defined
# repo folders off of the repos root, use hg
# to update them (pull), than use hg-git to
# push them to their new home @ github

import os
from subprocess import call as sub_call
from ConfigParser import ConfigParser

HG_PULL = 'cd %s; hg pull;'
HG_COMMIT = 'cd %s; hg commit -m "pushing to github"'
HG_GIT_PUSH = 'cd %s; hg bookmark -r default master; hg push git+ssh://git@github.com:rranshous/%s.git'
HERE = os.path.dirname(os.path.abspath(__file__))
print 'HERE: %s' % HERE

def call(cmd_string):
    print 'CALLING: %s' % cmd_string
    r = sub_call(cmd_string,shell=True)

def migrate():
    config = ConfigParser()
    config.read(os.path.join(HERE,'repos.conf'))

    repo_root = config.get('config','repos_root')
    for repo_name, use in config.items('repos'):
        print 'repo_name: %s' % repo_name
        use = eval(use)
        if not use: continue
        call(HG_PULL % os.path.join(repo_root,repo_name))
        call(HG_COMMIT % os.path.join(repo_root,repo_name))
        call(HG_GIT_PUSH % (os.path.join(repo_root,repo_name),repo_name))

if __name__ == '__main__':
    migrate()
