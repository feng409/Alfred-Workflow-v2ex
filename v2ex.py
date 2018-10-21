#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re

from workflow import Workflow3, web

logger = None

INPUT = ''  # 将输入作为全局变量，方便函数获取


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
    """
    获取 最热 tab节点的内容，v2ex开放API
    :param workflow:
    :return:
    """
    data = web.get('https://www.v2ex.com/api/topics/hot.json').json()
    for item in data:
        workflow.add_item(title=item['title'], subtitle=item['content'], arg=item['url'], valid=True)
    return len(data)


@KeyRegister('new')
def get_new(workflow):
    """
    获取 最新 tab节点的内容，v2ex开放API
    :param workflow:
    :return:
    """
    data = web.get('https://www.v2ex.com/api/topics/latest.json').json()
    for item in data:
        workflow.add_item(title=item['title'], subtitle=item['content'], arg=item['url'], valid=True)
    return len(data)


@KeyRegister('tab')
def get_tab(workflow):
    """
    提取tab节点内容
    :param tab: tab all
    :return:
    """
    url = 'https://www.v2ex.com/?tab=%s'
    tab = INPUT[4:]
    response = web.get(url % tab)
    data = parse_html(response.content)
    for item in data:
        workflow.add_item(title=item[1], arg=item[0], valid=True)
    return len(data)


def parse_html(content):
    """
    提取v2ex页面文章标题和链接
    :param content: 标题内容
    :return: [(url, title)]
    """
    data = re.compile(r'<span class="item_title"><a href="(.*)">(.*)</a></span>').findall(content)
    return data


def dispatch(input=''):
    """
    指令判断
    :param input:
    :return:
    """
    # 如果是主题节点
    logger.error(INPUT)
    if input.startswith('tab '):
        func = KeyRegister.handles.get('tab')
    else:
        func = KeyRegister.handles.get(input, lambda x: 0)
    return func


def main(workflow):
    global INPUT
    INPUT = workflow.args[0]

    func = dispatch(INPUT)
    data_len = func(workflow)

    # 如果没有items，添加默认items
    if data_len == 0:
        workflow.add_item(title=INPUT, subtitle=INPUT, arg=INPUT, valid=True)

    workflow.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    logger = wf.logger
    sys.exit(wf.run(main))
