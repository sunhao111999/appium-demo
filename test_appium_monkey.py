#!/usr/bin/env python
# -*- coding:utf8 -*-

from base import DoubanTest
from util import get_att
from time import sleep, time
import lxml.etree
import re
import os


class TestApiDemo(DoubanTest):
    actvity_run_dict = {}

    def _check_activity(self, old):
        if self._get_activity_name() != old:
            self.driver.back()

    def _find_element_and_click(self, k, v):

        try:
            xy = str(v).split(':')[1]
            if re.search('id', v):
                self._find_by(self.by_id, k, element_xy=xy).click()
            elif re.search('name', v):
                self._find_by(self.by_name, k, element_xy=xy).click()
        except Exception:
            print 'cant click but still run'

    def _press_back_and_rerun(self, log):
        self.driver.back()
        print log
        sleep(2)
        self._run()

    def _login(self, dom_list):

        for k in dom_list.keys():
            if re.search('pass', k):
                edit_text = self.driver.find_elements_by_class_name("android.widget.EditText")

                edit_text[0].send_keys('uiautomator@163.com')
                edit_text[1].send_keys('uiautomator163')

                print 'enter user and passwd over'
                break

        print 'find login btn'
        login = self.driver.find_elements_by_name('登录')
        for element in login:
            if element.tag_name == 'android.widget.Button':
                element.click()

        sleep(2)
        self.driver.back()

    def _run(self):

        print 'current build times %s' % (time() - self.BEGIN_BUILD_TIME)

        if (time() - self.BEGIN_BUILD_TIME) > self.DURATION:
            return

        curr_act_name = self._get_activity_name()
        curr_dom_dict = get_att(lxml.etree.XML(str(self.driver.page_source).strip()), {})
        dom_keys = curr_dom_dict.keys()

        if str(self.driver.current_activity).startswith(self.APP_PACKAGE):
            print 'reopen app'
            os.popen('adb shell am start -n %s' % self.HOME_ACTIVITY)

        if not curr_dom_dict:
            self._press_back_and_rerun('Cant get dom list, will press back')

        if curr_act_name == 'WebActivity':
            self._press_back_and_rerun('This page is WebActivity, will press back')

        print '======'
        print 'curr_act_name ', curr_act_name
        print 'curr_dom_dict', curr_dom_dict

        for key in dom_keys:

            if (time() - self.BEGIN_BUILD_TIME) > self.DURATION:
                return

            if re.search('user', key):
                self._login(curr_dom_dict)
                self._run()

            if curr_act_name not in self.actvity_run_dict.keys() and curr_act_name != 'WebActivity':
                print 'dont have this actvity name', curr_act_name
                self.actvity_run_dict[curr_act_name] = {key: curr_dom_dict.get(key)}
                self._find_element_and_click(key, curr_dom_dict.get(key))
                sleep(2)
                self._run()
            else:

                if (time() - self.BEGIN_BUILD_TIME) > self.DURATION:
                    return

                dom_values_dict = self.actvity_run_dict.get(curr_act_name)
                dom_values_dict_keys = dom_values_dict.keys()
                key_diff = [a for a in dom_keys if a in dom_values_dict_keys]
                print 'dom_values_dict_keys', dom_values_dict_keys

                if len(key_diff) == 0:
                    self._press_back_and_rerun('A float window, will press back')

                if key in dom_values_dict_keys:
                    print 'this activity name already have this key', key
                    continue
                else:
                    print 'have this activity, dont have this key', key
                    dom_values_dict[key] = curr_dom_dict.get(key)
                    self.actvity_run_dict[curr_act_name] = dom_values_dict
                    self._find_element_and_click(key, curr_dom_dict.get(key))
                    sleep(2)
                    self._run()

        self._press_back_and_rerun('Find all in this activity, will press back')

    def test_ClickApp(self):
        self._find_by(self.by_id, 'com.douban.frodo:id/intro_button').click()
        self._find_by(self.by_name, '电影').click()
        self._find_by(self.by_id, 'com.douban.frodo:id/choose_button').click()
        self._find_by(self.by_name, '豆瓣').click()

        self._run()
