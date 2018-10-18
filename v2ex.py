#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from workflow import Workflow3, web


logger = None


subtitle = '{username} • {time} • {} • '


class KeyRegister:
    """
    指令处理函数装饰器
    """
    handles = dict()

    def __init__(self, key):
        self.key = key

    def __call__(self, func):
        """
        注册指令处理函数
        :param func:
        :return:
        """
        KeyRegister.handles.update({self.key: func})
        return func


@KeyRegister('hot')
def get_hot(workflow):
    data = web.get('https://www.v2ex.com/api/topics/hot.json').json()
    for item in data:
        workflow.add_item(title=item['title'], subtitle=item['content'], arg=item['url'], valid=True)
    return len(data)


@KeyRegister('new')
def get_new(workflow):
    data = web.get('https://www.v2ex.com/api/topics/latest.json').json()
    for item in data:
        workflow.add_item(title=item['title'], subtitle=item['content'], arg=item['url'], valid=True)
    return len(data)


def main(workflow):
    key = workflow.args[0]
    func = KeyRegister.handles.get(key, lambda x: 0)

    data_len = func(workflow)

    # 如果没有items，添加默认items
    if data_len == 0:
        workflow.add_item(title=key, subtitle=key, arg=key, valid=True)

    workflow.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    logger = wf.logger
    sys.exit(wf.run(main))


