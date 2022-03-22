'''
-: Copyright (C) 2021 Yunding Network Technology(Beijing) Co., Ltd
.: All Rights Reserved.
*: Confidential and Proprietary - Yunding Network Technology.
Description:python 3.8; 解析keypad日志信息,统计开锁成功次数,失败次数,开锁成功率
LastEditors: zhj
LastEditTime: 2022-03-22 18:04:35
'''

import re
import os
import datetime

IS_DEBUG = False # True or False

'''
截取字符串中的时间，字符串格式必须用'[]'中括号括住。例'[2022-03-21 18:07:31]'
'''
def getTimeStr(str) :
    rs = re.search(rb'\[.*\d\]', str)
    if rs:
        return rs.group()[1:rs.group().__len__() - 1]
    else:
        print("not found, %s" % str)
        return

def getParameters(current_path = ".\\"):
    '''
    %Y 表示2022年    %y 表示22年
    %f 表示毫秒
    '''
    # time_format = "%y/%m/%d %H:%M:%S %f" # 对应日志中时间的格式
    time_format = "%Y-%m-%d %H:%M:%S" # 对应日志中时间的格式
    file_name = "test_log2.txt" # 日志文件名
    key_work1 = "\[unlock\]".encode('utf-8')
    key_work2 = "unlock success".encode('utf-8')
    key_work3 = "unlock failed".encode('utf-8')

    f = open(current_path + file_name, "rb")
    lines = f.readlines()
    f.close()

    if 0 == len(lines) :
        print("========is empty========")
        return

    new_file = file_name + "-"
    nf = open(current_path + new_file, "w")
    success_count = 0
    fail_count = 0
    success_total_time = 0
    total_count = 0

    for line in lines:
        rs = re.search(key_work1, line) # 1.找到[unlock]目标
        if rs:
            time_str = getTimeStr(line)
            if IS_DEBUG:
                print("find--->%s, date: %s" %(line, time_str))

            nf.write(str(line, encoding="utf-8").replace('\r', '')) # 去掉行尾\r

            rs = re.search(key_work2, line) # 2.区分目标是否为开锁成功
            if rs:
                success_count += 1
                total_count += 1
                dd2 = datetime.datetime.strptime(str(time_str, encoding="utf-8"), time_format)
                dd3 = dd2 - dd1

                if IS_DEBUG:
                    print("success time: %s" %(dd3.total_seconds()))

                success_total_time += dd3.total_seconds()
                nf.write("[%d]success time: %s\r\n" %(total_count, dd3.total_seconds()))
            elif (re.search(key_work3, line)) : # 3.区分目标是否为开锁失败
                total_count += 1
                fail_count += 1
                dd2 = datetime.datetime.strptime(str(time_str, encoding="utf-8"), time_format)
                dd3 = dd2 - dd1

                if IS_DEBUG:
                    print("fail time: %s" %(dd3.total_seconds()))

                nf.write("[%d]fail time: %s\r\n" %(total_count, dd3.total_seconds()))
            else : # 启动开锁
                dd1 = datetime.datetime.strptime(str(time_str, encoding="utf-8"), time_format) # 记录启动开锁时间

    # total_count = success_count + fail_count

    nf.close()

    # 将统计结果放在文件头
    nf = open(current_path + new_file, "r+")
    old_data = nf.read()
    nf.seek(0)
    nf.write("tatal num %d, success num %d, fail num %d, avgr %.3f\r\n" \
             % (total_count, success_count, fail_count, success_total_time/success_count))
    nf.write("===========================================================\n")
    nf.write(old_data)
    nf.close

    if IS_DEBUG:
        print("tatal num %d, success num %d, fail num %d, avgr %.3f" \
                % (total_count, success_count, fail_count, success_total_time/success_count))

if __name__ == '__main__':
    current_path = os.path.split(os.path.realpath(__file__))[0] + "\\" # 当前脚本路径 + \
    if IS_DEBUG:
        print(current_path)

    getParameters(current_path)

    # nf = open(current_path + "ttt.txt", "w")
    # nf.write("1\n")
    # nf.write("2\n")
    # nf.write("3\n")
    # nf.close()

    # f = open(current_path + "ttt.txt", "r+")
    # old = f.read()
    # f.seek(0)
    # f.write("hello\n")
    # f.write(old)
    # f.close()

