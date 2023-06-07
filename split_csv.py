#!/usr/bin/env python
# coding=utf-8

import pandas as pd
check_list=[]

def csv_file_read():
    global check_list
    # 读取表头
    head_row = pd.read_csv('/tcdata/test.csv', nrows=0)
    head_row_list = list(head_row)
    # 读取
    csv_result = pd.read_csv('/tcdata/test.csv', usecols=head_row_list)
    row_list = csv_result.values.tolist()
    return row_list



if __name__ == "__main__":
    jsp_list = []
    php_list = []
    check_list = csv_file_read()

    for shell in check_list:
        templist = {}
        if shell[1]=='jsp':
            templist['file_id'] = shell[0]
            templist['type'] = shell[1]
            # templist['label'] = shell[2]
            jsp_list.append(templist)
        else:
            templist['file_id'] = shell[0]
            templist['type'] = shell[1]
            # templist['label'] = shell[2]
            php_list.append(templist)
    df_php = pd.DataFrame(php_list,columns=['file_id','type'])
    df_php.to_csv("/tmp/php.csv",index=False)
    df_jsp = pd.DataFrame(jsp_list,columns=['file_id','type'])
    df_jsp.to_csv("/tmp/jsp.csv",index=False)