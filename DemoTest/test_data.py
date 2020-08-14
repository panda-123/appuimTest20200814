#ecoding=utf-8
# author:herui
# time:2020/8/6 16:07
# function:
import pytest
import csv

def test_get_data():
    datas = csv.reader(open("data.csv", "r", encoding="UTF-8"))
    # data_list = ["ID","name","CardNo","name2","pwd2","phoneNum"]
    data_list = []
    for data in datas:
        ID = data[0]
        name = data[1]
        CardNo = data[2]
        name2 = data[3]
        pwd2 = data[4]
        phoneNum = data[5]
        data_list.append(data)
        print(ID,name,CardNo,name2,pwd2,phoneNum)
    print(data_list)

