# ecoding=utf-8
# author:herui
# time:2020/7/29 11:21
# function:
import csv
import unittest
import pytest
import allure
import pytest_dependency

from langfangBank.driver.appium import Appium
from langfangBank.page.home_page import HomePage


class TestLogin(object):

    @classmethod
    def setup_class(cls):
        # todo:数据初始化
        Appium.initDriver()
        cls.home = HomePage()
        cls.mine = cls.home.to_mine()
        # cls.reg = cls.mine.to_register()
        # cls.log = cls.home.to_mine().to_login()


    @pytest.mark.parametrize("ID,name", [
        pytest.param("51072519580307706X","强帅楠", marks=pytest.mark.dependency(name="a1")),
        pytest.param("152921198308197711", "有俊", marks=pytest.mark.dependency(name="a2"))
    ])
    def test_reg_authentication(self,ID,name):
        self.mine.to_register().authentication(ID, name)
        assert 1==1

    @pytest.mark.parametrize("CardNo,name2,pwd2", [
        pytest.param("6221409000674898","qiangshuainan","ll1111",
                     marks=pytest.mark.dependency(name="b1",depends=["a1"])),
        pytest.param("6230730030796495", "youjun1", "ll1111",
                     marks=pytest.mark.dependency(name="b2",depends=["a2"]))
    ])
    def test_reg_info(self,CardNo,name2,pwd2):
        self.reg_info(CardNo,name2,pwd2)
        assert 1==1

    @pytest.mark.parametrize("phoneNum", [
        pytest.param("15809306466",
                     marks=pytest.mark.dependency(depends=["a1","b1"])),
        pytest.param("17602282811",
                     marks=pytest.mark.dependency(depends=["a2","b2"]))
    ])
    def test_reg_sec_question(self,phoneNum):
        assert self.mine.to_register().sec_question(phoneNum).get_reg_result() == "注册成功"



    # @pytest.mark.parametrize("usrName,pwd",[("lianyanggui","111111")])
    # def test_login(self,usrName,pwd):
    #     self.mine.to_login().input_info(usrName,pwd)

