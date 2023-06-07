#!/usr/bin/env python
# coding=utf-8
import logging
import os
import numpy as np
import joblib

logging.basicConfig(level=logging.DEBUG,
                    filename='log/checklog.log',
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
import pandas as pd
check_list=[]
res_list = []
def csv_file_read():
    global check_list
    # 读取表头
    head_row = pd.read_csv('/tcdata/test.csv', nrows=0)
    head_row_list = list(head_row)
    # 读取
    csv_result = pd.read_csv('/tcdata/test.csv', usecols=head_row_list)
    row_list = csv_result.values.tolist()
    return row_list

class WebshellDec(object):
    def __init__(self, vs):
        super(WebshellDec, self).__init__()
        self.cv = joblib.load("model/jsp/countvectorizer_" + vs + ".pkl")
        self.transformer = joblib.load("model/jsp/tfidftransformer_" + vs + ".pkl")
        self.mlp = joblib.load("model/jsp/xgb_" + vs + ".pkl")

    @staticmethod
    def load_file(file_path):
        t = b''
        with open(file_path, "rb") as f:
            for line in f:
                line = line.strip(b'\r\t')
                t += line
        return t
    def check(self):
        global res_list
        cklist = csv_file_read()
        for shell in cklist:
            tmplist= {}
            if shell[1]=="php":
                continue
                # tmplist["prediction"] = "white"
                # tmplist["file_id"]=shell[0]
            else:
                file_path = "/tcdata/test/"+str(shell[0])
                t = self.load_file(file_path)
                t_list = list()
                t_list.append(t)
                x = self.cv.transform(t_list).toarray()
                x = self.transformer.transform(x).toarray()
                y_pred = self.mlp.predict(x)

                if y_pred[0] == 1:
                    # tmplist[1] = "black"
                    # tmplist[0] = shell[0]
                    tmplist["prediction"] = "black"
                    tmplist["file_id"] = shell[0]
                else:
                    # tmplist[1] = "white"
                    # tmplist[0] = shell[0]
                    tmplist["prediction"] = "white"
                    tmplist["file_id"] = shell[0]
                pdata = t.decode()
                # black_l = ['java.lang.Process','getRuntime','webshell','Cmd','password']
                black_l = ['java.lang.Process','getRuntime','webshell','Cmd','password','IDENTIFIER:defineClass','IDENTIFIER:processCmd','IDENTIFIER:MethodWebHell','IDENTIFIER:webhell','IDENTIFIER:URLClassLoader','IDENTIFIER:ReflectInvoker','IDENTIFIER:MyClassLoader']
                stack_c = 0
                for i in black_l:
                    stack_c = stack_c+pdata.count(i)
                if stack_c>0:
                    # print("======="+str(stack_c))
                    tmplist["prediction"] = "black"
                    tmplist["file_id"] = shell[0]
            res_list.append(tmplist)
        df = pd.DataFrame(res_list,columns=['file_id','prediction'])
        df.to_csv("/tmp/res_jsp.csv",index=False)



if __name__ == "__main__":
    webshelldc = WebshellDec("v0")
    webshelldc.check()
