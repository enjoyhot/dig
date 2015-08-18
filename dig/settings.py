#! /usr/bin/env python
#coding=utf-8
"""
This module contains the global values for all settings used by dig.

For more information about these settings you can read the settings
documentation in https://github.com/enjoyhot/dig

"""
import os
from os.path import join,dirname

VERSION = "0.1.9"
TOOL_FILENAME = join(dirname(__file__)) + os.sep + "tool"
MAX_RECORD_NUM = 20

OPTIONAL_TOOLS = ["google","youdao"]
CURRENT_TOOL = "google"


"""
    google configuration 
"""
GOOGLE_TRANS_URL = 'http://translate.google.com/translate_a/single'
GOOGLE_TTS_URL = 'http://translate.google.cn/translate_tts'
GOOGLE_TRANS_PARAMS = {
    'client': 't',
    'dt': 'bd',
    'dt': 'ex',
    'dt': 'ld',
    'dt': 'md',
    'dt': 'qca',
    'dt': 'rw',
    'dt': 'rm',
    'dt': 'ss',
    'dt': 't',
    'dt': 'at',  
    'ie': 'UTF-8',
    'oe': 'UTF-8',      
    'srcrom': '0',
    'ssel': '0',
    'tsel': '0',
    'kc': '1',
    'tk': '522913|331595',
}
GOOGLE_TTS_PARAMS = {
    'ie': 'UTF-8',
    'total': '1',
    'idx': '0',
    'tk': '903567',
    'client': 't',
    'prev': 'input',
    'ttsspeed': '0.24',
}



"""
    youdao configuration 
"""
YOUDAO_TRANS_URL = 'http://fanyi.youdao.com/translate'
YOUDAO_TTS_URL = 'http://tts.youdao.com/fanyivoice'
YOUDAO_TRANS_PARAMS = {
    'doctype': 'json',
    'keyfrom': 'fanyi.web',
}
YOUDAO_TTS_PARAMS = {                        
    'keyfrom' : 'fanyi.web',
} 

