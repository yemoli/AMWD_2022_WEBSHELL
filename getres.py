# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
import joblib

features_len = 13


clf = joblib.load('./model/all.model')
feature_max = pd.read_csv('./data/temp.csv')
arr=feature_max.values
test_data = np.delete(arr, -1, axis=1) #删除最后一列
id=arr[:,features_len]

y_pred=clf.predict(test_data)
res_list = []
for i in range(0,len(id)):
    tmplist = {}
    if y_pred[i] == 0:
        tmplist["prediction"] = "white"
    else:
        tmplist["prediction"] = "black"
    tmplist["file_id"] = int(id[i])
    res_list.append(tmplist)
df = pd.DataFrame(res_list, columns=['file_id', 'prediction'])
df.to_csv("/tmp/res_php_1.csv", index=False)