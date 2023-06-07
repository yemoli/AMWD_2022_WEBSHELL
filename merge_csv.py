#!/usr/bin/env python
# coding=utf-8

import pandas as pd
res_list=[]
jsp_list = []
php_list = []
def jsp_csv_file_read():
    # 读取表头
    head_row = pd.read_csv('/tmp/res_jsp.csv', nrows=0)
    head_row_list = list(head_row)
    # 读取
    csv_result = pd.read_csv('/tmp/res_jsp.csv', usecols=head_row_list)
    row_list = csv_result.values.tolist()
    return row_list
def php_csv_file_read():
    # 读取表头
    head_row = pd.read_csv('/tmp/res_php.csv', nrows=0)
    head_row_list = list(head_row)
    # 读取
    csv_result = pd.read_csv('/tmp/res_php.csv', usecols=head_row_list)
    row_list = csv_result.values.tolist()
    return row_list



if __name__ == "__main__":
    jsp_list = jsp_csv_file_read()
    php_list = php_csv_file_read()
    res_list = jsp_list+php_list
    df_jsp = pd.DataFrame(res_list,columns=['file_id','prediction'])
    df_jsp.to_csv("/result.csv",index=False)