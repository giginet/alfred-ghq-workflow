#!/usr/bin/python
# encoding: utf-8

import os
import sys
import subprocess

from workflow import Workflow


class Client(object):
    def _execute_ghq(self, *args):
        args = ['ghq',] + list(args)
        return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()

    def is_available(self):
        output, err = self._execute_ghq()
        return not err

    def fetch_repository_list(self):
        output, _ = self._execute_ghq('list')
        return output.split('\n')

    def execute_get_repository(self, url):
        self._execute_ghq('get', url)

    @property
    def root(self):
        output, _ = self._execute_ghq('root')
        return output.rstrip()

    def get_path(self, repo_name):
        return os.path.join(self.root, repo_name)

def main(wf):
    args = wf.args
    client = Client()

    if client.is_available():
        if len(args) == 0:
            pass
        else:
            command = args[0]
            if command == 'get':
                pass
            else:
                query = args[0]
                repositories = client.fetch_repository_list()
                filtered = filter(lambda name: query in name, repositories)
                for repository in filtered:
                    path = client.get_path(repository)
                    wf.add_item(repository, path, arg=path, valid=True)
    else:
        wf.add_item(u'ghq is not available', u'')

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'giginet/alfred-ghq-workflow',
        'version': open(os.path.join(os.path.dirname(__file__), 'version')).read(),
    })
    sys.exit(wf.run(main))
