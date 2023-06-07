#!/usr/bin/env python
# coding=utf-8

import logging
import os
import numpy as np

# from sklearn.externals import joblib
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
        self.cv = joblib.load("model/php/countvectorizer_" + vs + ".pkl")
        self.transformer = joblib.load("model/php/tfidftransformer_" + vs + ".pkl")
        self.mlp = joblib.load("model/php/mlp_" + vs + ".pkl")

    @staticmethod
    def load_file(file_path):
        t = b''
        with open(file_path, "rb") as f:
            for line in f:
                line = line.strip(b'\r\t')
                t += line
        return t

    def checkdir(self, path):
        counter, webshell_number, normal_number = 0, 0, 0
        for r, d, files in os.walk(path):
            for file in files:
                file_path = r + '/' + file
                if os.path.splitext(file)[-1].lower() in ['.php', '.jsp', '.jspx', '.java', '.asp', '.aspx']:
                    t = self.load_file(file_path)
                    t_list = list()
                    t_list.append(t)
                    x = self.cv.transform(t_list).toarray()
                    x = self.transformer.transform(x).toarray()
                    y_pred = self.mlp.predict(x)
                    counter += 1
                    if y_pred[0] == 1:
                        logger.info("{} is webshell".format(file_path))
                        webshell_number += 1
                    else:
                        logger.info("{} is not webshell".format(file_path))
                        normal_number += 1
        logger.info("检测总量:%i, 检测出webshell:%i, 检测出正常文件:%i" % (counter, webshell_number, normal_number))


    def check(self):
        global res_list
        cklist = csv_file_read()
        for shell in cklist:
            tmplist= {}
            if shell[1]=="jsp":
                # tmplist["prediction"] = "white"
                # tmplist["file_id"]=shell[0]
                continue
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
            res_list.append(tmplist)
        df = pd.DataFrame(res_list,columns=['file_id','prediction'])
        df.to_csv("/tmp/temp.csv",index=False)



if __name__ == "__main__":
    webshelldc = WebshellDec("v0")
    webshelldc.check()
