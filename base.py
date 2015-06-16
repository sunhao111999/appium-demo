#!/usr/bin/env python
# -*- coding:utf8 -*-


import unittest
import os
from time import sleep, time

from appium import webdriver
from PIL import Image, ImageDraw

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
MAX_TIME = 8


class DoubanTest(unittest.TestCase):
    # swipe to
    TO_LEFT = [0.1, 0.5, 0.9, 0.5]
    TO_RIGHT = [0.9, 0.5, 0.1, 0.5]
    TO_BEGINNING = [0.5, 0.1, 0.5, 0.9]
    TO_END = [0.5, 0.9, 0.5, 0.1]

    # find type
    by_id = 'id'
    by_name = 'name'
    by_auia = 'android_uiautoamtor'
    by_desc = 'desc'

    # app packagename
    APP_PACKAGE = 'com.douban.frodo'
    HOME_ACTIVITY = 'com.douban.frodo/.MainActivity'

    # monkey run times
    DURATION = 2 * 60

    def setUp(self):
        self.BEGIN_BUILD_TIME = time()
        os.popen('rm -rf logcat_error.log')
        os.popen('adb logcat -c')
        os.popen('adb shell am force-stop %s' % self.APP_PACKAGE)

        desired_caps = {'platformName': 'Android',
                        'platformVersion': '4.4',
                        'deviceName': 'Android Emulator',
                        'app': PATH('apps/' + 'app-debug.apk'),
                        'appPackage': self.APP_PACKAGE,
                        'appActivity': '.activity.SplashActivity'}

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        sleep(5)

    def tearDown(self):
        self.driver.quit()
        os.popen('adb shell am force-stop %s' % self.APP_PACKAGE)
        os.popen('adb logcat -d | grep E/AndroidRuntime >> logcat_error.log')

    def _find_by(self, find_type, element, element_xy=0, wait_time=5):
        ui_object = ''

        wait = 1

        while wait < wait_time:
            try:
                if find_type == self.by_name:
                    ui_object = self.driver.find_element_by_name(element)
                elif find_type == self.by_id:
                    ui_object = self.driver.find_element_by_id(element)
                elif find_type == self.by_auia:
                    ui_object = self.driver.find_element_by_android_uiautomator(element)
            except Exception:
                print 'Wait to find %s again! Find count %s' % (element, wait)
                sleep(1)
                wait += 1
            else:
                break

        if wait >= wait_time:
            print 'cant find this element, will take screenshot'
            screenshot_name = self._testMethodName + '.png'
            self.driver.get_screenshot_as_file(screenshot_name)

            # 提供某个元素的坐标，会在截图上标注出该元素
            if element_xy != 0:
                self._draw_ellipse(screenshot_name, element_xy)

        return ui_object

    def _scroll_find_element(self, swipe_xy, find_type, element):
        for i in xrange(MAX_TIME):
            if self._find_by(find_type, element, 0):
                break
            else:
                self._swipe_activity(swipe_xy, 1)

    def _swipe_activity(self, swipe_xy, times):
        for i in xrange(times):
            try:
                self.driver.swipe(swipe_xy[0], swipe_xy[1], swipe_xy[2], swipe_xy[3], 600)
                sleep(1)
            except Exception, e:
                print e

    def _get_activity_name(self):
        return str(self.driver.current_activity).split('.')[-1]

    def _draw_ellipse(self, file_name, xy):
        im = Image.open(file_name)
        draw = ImageDraw.Draw(im)
        draw.ellipse(xy, outline=(255, 0, 0, 255))
        im.save(file_name)


if __name__ == "__main__":
    unittest.main()
