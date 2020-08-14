#ecoding=utf-8
# author:herui
# time:2020/8/6 15:37
# function:
import pytest
import unittest
from pytest_dependency import depends

data1 = [(1,2,3),(2,3,6)]
data2 = [3,5]
data_1 = (
        {
            'user': 1,
            'pwd': 2
        },
        {
            'user': 3,
            'pwd': 4
        })

# @pytest.mark.parametrize("dic", data_1)
class TestCases():

    # def get_data(self):
    #     self.file = open("data.json", "r", encoding="utf-8")
    #     self.lines = self.file.readlines()
    #     # data_list = ["ID","name","CardNo","name2","pwd2","phoneNum"]
    #     self.data_list = []
    #     for line in self.lines:
    #         for i in range(0,len(self.data_list)):
    #             self.data_list[i] = line[i]
    #     print(self.data_list)
    #     self.file.close()
    #     return self.data_list


    # @pytest.mark.parametrize(get_data())
    # def reg(self,ID,name,CardNo,name2,pwd2,phoneNum):
    #     print(ID,name,CardNo,name2,pwd2,phoneNum)

    @pytest.mark.dependency(name="a")
    @pytest.mark.parametrize("dic",data_1)
    def test_a(self,dic):
        print("user:",dic["user"])
        assert dic["user"] == 3

    @pytest.mark.dependency(depends=["TestCases::test_a"])
    @pytest.mark.parametrize("a", [1])
    # def test_b(self,dic):
    #     print(dic["pwd"],"*"*20)
    #     return dic["pwd"] == 2
    def test_b(self,a):
        pass
