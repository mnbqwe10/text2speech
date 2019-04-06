# -*- coding: utf-8 -*-
import os, sys
import time
from aip import AipSpeech

STR_LEN_LIMIT = 1000
INTERVAL = 0

def splitsmall(string):
    rlist = []
    if not string:
        return []
    elif len(string) < STR_LEN_LIMIT:
        return [string]
    else:
        sentences = string.split('。')
        for sentence in sentences:
            if len(sentence) > STR_LEN_LIMIT:
                div, mod = divmod(len(sentence), STR_LEN_LIMIT)
                for i in range(div):
                    rlist.append(sentence[i:i+STR_LEN_LIMIT])
                rlist.append(sentence[-mod:])
            else:
                rlist.append(sentence)
        return rlist


if __name__ == '__main__':
    # APP_ID = input("请输入百度APP ID：")
    # API_KEY = input("请输入百度API Key：")
    # SECRET_KEY = input("请输入百度Secret Key：")
    cwd = os.getcwd()
    print("Searching txt in {}".format(cwd))

    files = os.listdir(cwd)
    txtlist = []
    if 'config.ini' in files:
        with open('config.ini', 'r', encoding='utf-8') as reader:
            options = dict()
            for line in reader.readlines():
                if line.find('APP ID') != -1:
                    APP_ID = line.split("：")[-1]
                elif line.find('API Key') != -1:
                    API_KEY = line.split("：")[-1]
                elif line.find('Secret Key') != -1:
                    SECRET_KEY = line.split("：")[-1]
                elif line.find('Speed') != -1:
                    options.update({'spd': line.split("：")[-1]})
                elif line.find('Pit') != -1:
                    options.update({'pit': line.split("：")[-1]})
                elif line.find('Volume') != -1:
                    options.update({'vol': line.split("：")[-1]})
                elif line.find('Person') != -1:
                    options.update({'per': line.split("：")[-1]})
            if not (APP_ID and API_KEY and SECRET_KEY):
                sys.exit("Please confirm APP ID API KEY and SECRET KEY are not empty!")
        for filename in files:
            if filename.endswith(".txt"):
                txtlist.append(filename)
                print(filename)
    else:
        with open('config.ini', 'w', encoding='utf-8') as writer:
            string = """百度APP ID：
百度API Key：
百度Secret Key：
语速Speed(取值0-9，默认为5中语速)：5
音调Pit(取值0-9，默认为5中语调)：5
音量Volume(取值0-15，默认为5中音量)：5
发音人Person(0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女)：0
"""
            writer.write(string)
        sys.exit("'config.ini' is generated, please fill in!")


    try:
        print("Connecting client...")
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        print("Client connected...")
    except:
        print("Fail to connect Client...")
        sys.exit(-1)

    for file in txtlist:
        print("Start processing {}".format(file))
        audio_name = file.split('.')[0] + '.mp3'
        with open(audio_name, 'wb') as f:
            with open(file, 'r', encoding='utf-8') as reader:
                for line in reader.readlines():
                    for string in splitsmall(line):
                        result = client.synthesis(string, 'zh', 1, options)
                        print(string)
                        time.sleep(INTERVAL)
                        if not isinstance(result, dict):
                            f.write(result)
            print(audio_name+" is saved!\n")
