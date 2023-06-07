# -*- coding: UTF-8 -*-
import pandas as pd
def read_file(filename):
    text = b""
    with open(filename, "rb") as f:
        for line in f:
            line = line.strip(b"\r\t")
            text += line
        text = text.decode()
        # text = text.replace('\\', '')
        # text = text.replace('"', '')
    return text


head_row = pd.read_csv('/tmp/res_php_1.csv', nrows=0)
head_row_list = list(head_row)
csv_result = pd.read_csv('/tmp/res_php_1.csv', usecols=head_row_list)
row_list = csv_result.values.tolist()
res_list = []

for line in row_list:
    templist = {}

    #################
    # data = read_file('/tcdata/test/'+str(line[0]))
    # black_list = [r'INCLUDE_OR_EVAL(eval):',r'ZVAL:"php_uname"',r'ZVAL:"_FILES"']
    # black_c = 0
    # for i in black_list:
    #         black_c = black_c+data.count(i)
    #         # print(black_c)
    #         # print(i)
    # if black_c>0:
    #         # print(data)
    #         # exit()
    #         print(line[0])
    #################
    if line[1] == "white":
        data = read_file('/tcdata/test/'+str(line[0]))
        # black_list = [r'INCLUDE_OR_EVAL(eval):',r'ZVAL:\"phpinfo\"',r'ZVAL:\"Yandex\"',r'ZVAL:\"wormscan\"',r'ZVAL:\"whoami\"']#提升,0.7左右
        black_list = [r'INCLUDE_OR_EVAL(eval):']#提升,0.7左右
        # black_list = [r'ZVAL:\"disk_total_space\"',r'ZVAL:\"\\/etc\\/passwd\"',r'ZVAL:\" GB\"',r'ZVAL:\"openbasedir\"',r'ZVAL:\"Disabled PHP Functions\"',r'ZVAL:\"uploadFile\"',r'ZVAL:\"uploadfile\"']#下降，hongkongs
        # black_list = [r'ZVAL:\"ob_clean\"',r'ZVAL:\"gr\"',r'ZVAL:\"eregi\"',r'ZVAL:24576',r'ZVAL:\"mysql_error\"']#下降 red123s，2.30跑的；服务器时间6:34
        # black_list = [r'ZVAL:\"\\/etc\\/passwd\"',r'ZVAL:\" GB\"',r'ZVAL:\"safe_mode\"']#下降，hongkongs
        # black_list = [r'ZVAL:\"htmlspecialchars\"']#待定 aliyun8895165333

        black_c = 0
        for i in black_list:
            black_c = black_c+data.count(i)
        if black_c>0:
            print(line[0])
            templist['prediction'] = 'black'
        else:
            templist['prediction'] = 'white'
        templist['file_id'] = int(line[0])
    else:
        templist['file_id'] = int(line[0])
        templist['prediction'] = 'black'
    res_list.append(templist)

df = pd.DataFrame(res_list, columns=['file_id', 'prediction'])
df.to_csv("/tmp/res_php.csv", index=False)