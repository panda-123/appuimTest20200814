#ecoding=utf-8
# author:herui
# time:2020/7/29 15:28
# function:
import time

import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from driver.appium import Appium
from langfangBank.page.base_page import BasePage


class RegisteUser(BasePage):

    _id_card = (By.ID, "et_id_card")
    _name = (By.ID, "et_name")
    _agree_selector = (By.ID, "cb_agree")
    _bt_next = (By.ID, "bt_next")
    _Card_No = (By.ID, "et_cardNO")
    _Card_pwd = (By.ID, "pge_password_regist")
    _set_name = (By.ID, "et_loginname")
    _set_pwd = (By.ID, "pge_loginpwd_regist")
    _config_pwd = (By.ID, "pge_confirmPwd")
    _input_ans = (By.XPATH, BasePage.byAttr("请输入答案"))
    _phone_num = (By.XPATH, BasePage.byAttr("请输入手机号码"))
    _get_code = (By.XPATH, BasePage.byAttr("获取验证码"))
    # _input_code = (By.XPATH, BasePage.byAttr("请输入验证码"))
    _input_code = (By.ID, "et_mobileVerCode")
    _ok_btn = (By.ID, "bt_ok")
    _result = (By.XPATH, BasePage.byAttr("注册成功"))
    _back = (By.ID, "iv_left")
    _success = (By.XPATH, "//*[@text='取消']")
    _txt_title = (By.ID, "txt_title")

    @allure.step("开始身份验证")
    def authentication(self, ID, Name):
        self.find(self._id_card).send_keys(ID)
        self.find(self._name).send_keys(Name)
        self.find(self._agree_selector).click()
        self.find(self._bt_next).click()
        if self.find(self._txt_title).text == "注册":
            return self
        else:
            self.find(self._back).click()

    def reg_info1(self, CardNo, name, pwd2, pwd=""):
        #todo:手动输入密码,强制等待
        self.find(self._Card_No).send_keys(CardNo)
        page_source = self.find(self._Card_pwd).send_keys(pwd)
        print(page_source)
        time.sleep(10)
        self.find(self._set_name).send_keys(name)
        self.find(self._set_pwd).send_keys(pwd2)
        time.sleep(10)
        self.find(self._config_pwd).send_keys(pwd2)
        time.sleep(10)
        self.find(self._bt_next).click()
        return self

    @allure.step("输入注册信息")
    def reg_info(self, CardNo, name, pwd2, pwd=""):
        #todo:手动输入密码，等待输入后，再进行下一步操作
        """
        :param CardNo:卡号
        :param name:账户昵称
        :param pwd2:登录密码
        :param pwd:取款密码，一般默认 808080
        :return:
        """
        self.find(self._Card_No).send_keys(CardNo)
        ele1 = self.find(self._Card_pwd)
        self.wait_input(ele1,"请输入账户取款密码")
        self.find(self._set_name).send_keys(name)
        el2 = self.find(self._set_pwd)
        self.wait_input(el2,"请输入登录密码")
        el3 = self.find(self._config_pwd)
        self.wait_input(el3,"请再次输入密码")
        self.find(self._bt_next).click()
        return self

    @allure.step("输入验证问题")
    def sec_question(self,phoneNum):
        elements= self.findAll(self._input_ans)
        if len(elements)>=1:
            elements[0].send_keys("爷爷")
            elements[1].send_keys("班主任")
            elements[2].send_keys("1001")
        self.find(self._phone_num).send_keys(phoneNum)
        self.find(self._get_code).click()
        time.sleep(3)
        el_code = self.find(self._input_code)
        # el_code.send_keys(code)
        self.wait_input(el_code,"请输入验证码")
        self.find(self._ok_btn).click()

    def get_reg_result(self):
        return self.find(self._result).text

    def goto_mine(self):
        self.find(self._success).click()
        self.find(self._back).click()

    def get_title(self):
        return self.find(self._txt_title).text

