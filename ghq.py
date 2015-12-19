#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow


def main(wf):
    # Get args from Workflow, already in normalised Unicode
    args = wf.args

    # Do stuff here ...

    # Add an item to Alfred feedback
    wf.add_item(u'Item title', u'Item subtitle')

    # Send output to Alfred
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
