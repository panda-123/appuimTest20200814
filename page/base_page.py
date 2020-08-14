#ecoding=utf-8
# author:herui
# time:2020/7/29 10:37
# function:
from appium.webdriver import WebElement
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from langfangBank.driver.appium import Appium
from lxml import etree

import cv2
import os
import numpy as np
import time
import logging

class BasePage(object):
    # 黑名单，处理随时可能的弹窗
    _blank_words = [
        (By.XPATH, "//*[text='好的']"),
        (By.XPATH, "//*[@text='下次再说']"),
        (By.XPATH, "//*[@text='同意']"),
        (By.XPATH, "//*[@text='取消']")
    ]
    @classmethod
    def byAttr(cls, text=None, id=None):
        text_selector = ""
        if text is not None:
            text_selector = "@text='" + text + "'"

        if id is not None:
            id_selector = "contains(@resource-id, '" + id + "')"
            return "//*[" + text_selector + " and " + id_selector + "]"
        else:
            return "//*[" + text_selector + "]"

    @classmethod
    def byUiSel(cls, text=None, id=None):
        text_selector = ""
        if text is not None:
            text_selector = "@text='" + text + "'"

        if id is not None:
            id_selector = "contains(@resource-id, '" + id + "')"
            # return "//*[" + text_selector + " and " + id_selector + "]"
            return (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("'+id+'").text("'+text+'")')
        else:
            return (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("'+text+'")')

    def exception_handle(self):
        # 加todo，会提示相关内容
        #todo:优化
        for w in self._blank_words:
            logging.info(w)
            elements = Appium.driver.find_elements(w)
            if len(elements) > 0:
                elements[0].click()
                return Appium.driver.find_element(w)

    def exception_handle1(self):
        # todo:优化弹框处理逻辑，发现toast,自动发现兼容性问题等
        page_source = Appium.driver.page_source
        print(page_source)
        # xml = etree.XML(page_source)
        xml = etree.XML(str(page_source)).encode("utf-8")
        for w in self._blank_words:
            print(w)
            if len(xml.xpath(w))>0:
                Appium.driver.find_element(w).click()

    def findBy(self,by=By.ID, value = None):
        try:
            return Appium.driver.find_element(by, value)
        except:
            # 以下为比较粗暴的处理方式，后续需要优化
            self.exception_handle1()
            return Appium.driver.find_element(by, value)

    def find(self,locate)->WebElement:
        # ->表示指定返回类型
        # 返回的内容若无类型，则无法自动识别其特性,比如 click等
        return self.findBy(*locate)

    def findAll(self,locate) -> []:
        # 返回列表类型
        return Appium.driver.find_elements(*locate)

    def longPress(self, el, duration=1):

        center_x = el.location.get('x') *1.05
        center_y = el.location.get('y') *1.05
        duration = duration * 3000
        # center = (center_x, center_y)
        # TouchAction(Appium.driver).tap(center_x,center_y).perform()
        Appium.driver.swipe(center_x,center_y,center_x,center_y,duration)
        return self

    def get_pwd_pos(self,im,pwd):
        numbers = set(list(pwd))
        print(numbers)
        templates = {}
        positions = {}
        nimgpath = "./image/"  # 数字图片不在同目录时使用
        for i in numbers:
            templates[i] = os.path.join(nimgpath, "n{}.png".format(i))

        start = time.time()
        # 读源图片
        img_rgb = cv2.imread(im)
        print("原图尺寸：", img_rgb.shape)
        for teNum, tepath in templates.items():
            print("teNum: ", teNum)
            # print("tepath: ", tepath)
            # 读取模板图片
            template = cv2.imread(tepath)
            # print('图片尺寸:', template.shape)
            res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
            # 匹配度参数，1为完全匹配
            threshold = .80
            # 匹配程度大于%80的坐标y,x
            loc = np.where(res >= threshold)
            if len(loc) > 0:
                positions[teNum] = list(zip(*loc[::-1]))[0]
                # print("positions[%d]:--"%teNum,positions[teNum])
            else:
                print("Can not found number: [{}] in image: [{}].".format(tepath, im))

        end = time.time()
        print(end - start)
        return [positions[n] for n in pwd]
    def click_pwd(self,pwd,im="../screen/pwd.png"):
        pwd = self.get_pwd_pos(im,pwd)
        for e in pwd:
            Appium.driver.tap(e)
        return self

    def wait_input(self,element,text=""):
        while True:
            if element.text != text and element.text != "":
                break
            else:
                time.sleep(5)
                continue
        return self

    def find_toast(self, message):
        message = "//*[contains(@text, '" + message + "')]"
        ele = WebDriverWait(Appium.driver, 5, 0.1).until(lambda x: x.find_element(By.XPATH, message))
        return ele.text

