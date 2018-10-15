#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from workflow import Workflow3, web, Workflow


handles = dict()


def handle_key(key):
    def wrapper(func):
        handles.update({key: func})
        return func
    return wrapper


@handle_key('hot')
def get_hot():
    return web.get('https://www.v2ex.com/api/topics/hot.json').json()


def main(wf):
    args = wf.args[0]
    func = handles.get(args, None)
    data = list()
    if func:
        data = func()
        for post in data:
            wf.add_item(
                    title=post['title'], 
                    subtitle=post['content'],
                    arg=post['url'],
                    valid=True)

    if len(wf._items) == 0:
        wf.add_item(title='暂无内容', subtitle='正在查找...')

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))


