# -*- coding: UTF-8 -*- 
import json

# 读取json文件
def read_json_file(file_path):
    json_file = open(file_path, "r", encoding='UTF-8')
    results_json=json.load(json_file)
    json_file.close
    return results_json