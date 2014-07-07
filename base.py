#!/usr/bin/env python
# -*- coding:utf8 -*-


import unittest
import os
from time import sleep

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.common.exceptions import NoSuchElementException


PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
SLEEPY_TIME = 2
SCROLL_MAX_TIME = 3

class DoubanTest(unittest.TestCase):
    def setUp(self):
        os.system('adb shell am force-stop %s' % APP_PACKAGE)

        desired_caps = {'platformName': 'Android',
                        'platformVersion': '4.4',
                        'deviceName': 'Android Emulator',
                        'app': PATH('apps/' + 'ApiDemos-debug.apk'),
                        'appPackage': 'com.example.android.apis',
                        'appActivity': '.ApiDemos'}

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        sleep(5)

    def tearDown(self):
        self.driver.quit()
        os.system('adb shell am force-stop %s' % APP_PACKAGE)

    def _is_exits(self, name):
        result = True
        try:
            self.driver.find_element_by_name(name)
        except Exception, e:
            print e
            result = False

        return result

    def _scroll_find_element(self, name):
        for i in xrange(SCROLL_MAX_TIME):
            if self._is_exits(name):
                break
            else:
                try:
                    swipe_args = {'startX': 0.5, 'startY': 0.9, 'endX': 0.5, 'endY': 0.5, 'duration': 5}
                    self.driver.execute_script("mobile: swipe", swipe_args)
                    sleep(SLEEPY_TIME)
                except Exception, e:
                    print e

    def _scroll_from_beginning_to_end(self, times):
        for i in xrange(times):
            try:
                swipe_args = {'startX': 0.5, 'startY': 0.9, 'endX': 0.5, 'endY': 0.1, 'duration': 5}
                self.driver.execute_script("mobile: swipe", swipe_args)
                sleep(SLEEPY_TIME)
            except Exception, e:
                print e

    def _swipe_from_left_to_right(self, times):
        for i in xrange(times):
            try:
                swipe_args = {'startX': 0.9, 'startY': 0.5, 'endX': 0.1, 'endY': 0.5, 'duration': 5}
                self.driver.execute_script("mobile: swipe", swipe_args)
                sleep(SLEEPY_TIME)
            except Exception, e:
                print e


if __name__ == "__main__":
    unittest.main()
