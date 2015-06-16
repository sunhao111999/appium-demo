#!/usr/bin/env python
# -*- coding:utf8 -*-


import sys
import lxml.etree
import re

reload(sys)
sys.setdefaultencoding('utf-8')

# 如果某个节点当前没有name或id，得到该节点的index并查找该节点的父节点，依次类推直到找到有name或id的节点


def get_index_parent(element, current_index):
    parent = element.getparent()

    if not parent.attrib['resource-id'] and not parent.attrib['text']:
        current_index.append(parent.attrib['index'])
        get_index_parent(parent, current_index)
    else:
        resouce = 'id: ' + parent.attrib['resource-id'] if parent.attrib[
            'resource-id'] else 'text: ' + parent.attrib['text']
        current_index.append(resouce)

    return current_index


def get_att(element_root, dom_dic):
    for child in element_root:
        if child.attrib['clickable'] == 'true':
            resource_id = child.attrib['resource-id']
            name = child.attrib['text'] if child.attrib['text'] else child.attrib['content-desc']
            # 暂时不考虑index的情况
            # if not resource_id and not name:
            #     index_list = [child.attrib['index']]
            #     dom_dic[str(get_index_parent(child, index_list))] = 'index'
            # elif resource_id:
            #     dom_dic[resource_id] = 'id'
            # elif name:
            #     dom_dic[name] = 'name'

            if resource_id:
                dom_dic[resource_id] = 'id:' + conv_bounds_to_point(child.attrib['bounds'])
            elif name:
                dom_dic[name] = 'name:' + conv_bounds_to_point(child.attrib['bounds'])

        get_att(child, dom_dic)

    return dom_dic


def if_has_list(element_root, list_dic):
    # 当前xml中若有listview或gridview，这个activity是可以需要上下滑动重新搜索的, 有scrollview是可以左右滑动的

    for child in element_root:
        if child.attrib['class'] == 'android.widget.ListView':
            list_dic['list_view'] = True
        elif child.attrib['class'] == 'android.widget.GridView':
            list_dic['grid_view'] = True
        elif child.attrib['class'] == 'android.widget.HorizontalScrollView':
            list_dic['scroll_view'] = True

        if_has_list(child, list_dic)

    return list_dic


def conv_bounds_to_point(bounds):
    x1 = int(get_any_from_str('[', ',', bounds))
    y1 = int(get_any_from_str(',', '][', bounds))
    x2 = int(get_any_from_str('][', ',', bounds))
    y2 = int(get_any_from_str(',', ']', bounds))
    return str((x1, y1, x2, y2))


def get_any_from_str(begin, end, your_str):
    return your_str.split(begin)[1].split(end)[0]


if __name__ == '__main__':

    root = lxml.etree.parse('log.xml').getroot()
    list_dic = get_att(root, {})
    for k, v in list_dic.items():
        print k, v
