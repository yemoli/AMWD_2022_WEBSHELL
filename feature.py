# -*- coding: UTF-8 -*-
import re
import pandas as pd
import numpy as np
import joblib

jsp_list = []
f_input = ""

features_len = 13
def read_file(filename):
    text = b""
    with open(filename, "rb") as f:
        for line in f:
            line = line.strip(b"\r\t")
            text += line
        result = re.compile('\"name\":.*?\]', re.S)  # 正则匹配
        # val": 
        # result = re.compile('val\":\"(.*?)\"', re.S)
        theresult = re.findall(result, str(text))
        text = ''.join(theresult)
        text = text.replace('[', ' ')
        text = text.replace(']', ' ')
        text = text.replace('\\', ' ')
        text = text.replace(',', ' ')
        text = text.replace('"', ' ')
        text = text.replace('name :', ' ')
        text = re.sub('<(.*?)>','',text)
        text = re.sub('FROM `(.*?)`','',text)
        text = re.sub('INSERT INTO `(.*?)\)','',text)
        text = re.sub('UPDATE `(.*?)WHERE','',text)
        text = re.sub('REPLACE INTO `(.*?)\)','',text)
        text = re.sub('`(.*?)`=','',text)
        text = re.sub('SELECT `(.*?)`','',text)
        #INSERT INTO `
        text = text.replace(':', ' ')
        text = text.replace('STMT_LIST', ' ')
        text = text.replace('ZVAL', ' ')
        text = text.replace('NULL', ' ')
        # text = text.encode("utf-8")
        text = ' '.join(text.split()).encode("utf-8")
    return text

def autowrite(*features,line):
    global tmpcsv
    global f_input

    wtf = "%f"+",%f"*len(features)
    features = features + (line[0], )
    f_input.write(wtf % features+'\n')

def get_features(data,line):
    key_num=0#黑名单数量
    capital_len=0
    namespace_c = 0#namespace数量
    op_c = 0#BINARY_OP 数量
    class_c = 0#CLASS数,结合namespace数量，区分度高
    passw_c = 0#passw数量,区分度一般
    include_c = 0#include数量,区分度一般
    FUNC_DECL_c = 0#FUNC_DECL_c数量,较高
    unquote_c = 0#反引号`的数量
    eval_c = 0 #eval的数量
    shell_c = 0#shell 字符串的数量
    hack_c = 0#hack字符串的数量
    backdoor_c = 0#backdoor字符串数量
    arg_c = 0 
    post_c = 0#_POST字符串的数量
    file_c = 0#_FILE字符串数量
    get_c = 0 #_GET字符串数量
    b64dec_c = 0#base64decode字符串数量
    flate_c = 0 #flate字符串数量，区分频率低，但存在即是shell
    iua_c = 0 #ignore_user_abort字符串数量，区分频率低，但存在即是shell
    stl_c = 0 #set_time_limit字符串数量，区分频率低，
    smqr_c = 0 #set_magic_quotes_runtime 高
    muf_c = 0 #move_uploaded_file 高
    sys_c = 0 #system 中
    curl_c = 0#curl_exec 高
    funexit_c = 0#function_exists 高
    call_c = 0 #CALL 
    oppoint_c = 0#(.)

    key_num=data.count('str_rot13')+data.count('serialize')+data.count('eval')+data.count('base64_decode')+data.count('strrev')
    +data.count('assert')+data.count('file_put_contents')+data.count('fwrite')+data.count('curl_exec')+data.count('passthru')+data.count('exec')
    +data.count('dl')+data.count('readlink')+data.count('popepassthru')+data.count('preg_replace')+data.count('create_function')+data.count('array_map')
    +data.count('call_user_func')+data.count('array_filter')+data.count('usort')+data.count('stream_socket_server')+data.count('pcntl_exec')+data.count('system')
    +data.count('chroot')+data.count('scandir')+data.count('chgrp')+data.count('shell_exec')+data.count('proc_open')+data.count('proc_get_status')
    +data.count('popen')+data.count('ini_alter')+data.count('ini_restore')+data.count('ini_set')+data.count('LD_PRELOAD')+data.count('_GET')+data.count('_POST')+data.count('_COOKIE')
    +data.count('_FILE')+data.count("phpinfo")+data.count("_SERVER")
    namespace_c = data.count("NAMESPACE")
    op_c = data.count("BINARY_OP")
    class_c = data.count("CLASS")
    passw_c = data.count("passw")
    #ASSIGN_REF
    include_c = data.count("INCLUDE_OR_EVAL")
    FUNC_DECL_c = data.count("FUNC_DECL")
    unquote_c = data.count("`")
    eval_c = data.count(" eval ")
    shell_c = data.count("shell")
    hack_c = data.count("hack")
    backdoor_c = data.count("backdoor")
    capital_len=len(re.compile(r'[0-9]').findall(data))

    capital_f=capital_len/len(data)#大写字母频率
    post_c = data.count("_POST")
    file_c = data.count("_FILE")
    get_c = data.count("_GET")
    b64dec_c = data.count("base64_decode")
    flate_c =data.count("flate")
    iua_c = data.count("ignore_user_abort")
    stl_c = data.count("set_time_limit")
    smqr_c = data.count("set_magic_quotes_runtime")
    muf_c = data.count("move_uploaded_file")
    sys_c = data.count(" system ")
    curl_c = data.count(" curl_exec ")
    arg_c = data.count("ARG_LIST")
    content_list = re.split(r' ',data)
    max_length = 0
    for i in content_list:
        if len(i) > max_length:
            max_length = len(i)
        else:
            pass
    funexit_c = data.count(" function_exists ")
    call_c = data.count(" CALL ")
    oppoint_c = data.count("(.)")
    temp = data.count("passw")

    
    autowrite(
        len(data),
        # namespace_c,
        # class_c,
        op_c,
        arg_c,
        capital_f,
        key_num,
        passw_c,
        include_c,
        FUNC_DECL_c,
        max_length,
        unquote_c,
        eval_c,
        shell_c,
        # hack_c,
        # backdoor_c,
        call_c,
        line=line
    )

def generate():
    global f_input
    global features_len
    feat = "0.000000,"*features_len
    f_input=open("./data/temp.csv", 'w')
    f_input.write(feat+"1.000000\n")
    # head_row = pd.read_csv('/tcdata/test.csv', nrows=0)
    head_row = pd.read_csv('/tmp/temp.csv', nrows=0)
    head_row_list = list(head_row)
    # csv_result = pd.read_csv('/tcdata/test.csv', usecols=head_row_list)
    csv_result = pd.read_csv('/tmp/temp.csv', usecols=head_row_list)
    row_list = csv_result.values.tolist()
    for line in row_list:
        if line[1] == "white":
            
            f_input.write(feat+"%f\n"% line[0])
        else:
            data = read_file('/tcdata/test/'+str(line[0])).decode('utf-8')
            if(len(data)>0):
                get_features(data,line)
            else:
                f_input.write(feat+"%f\n"% line[0])


generate()
