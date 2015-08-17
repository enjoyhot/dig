#! /usr/bin/env python
#coding=utf-8

from __future__ import unicode_literals
from __future__ import print_function

# standrad packages
import unicodedata
import requests
import re
import os
from os.path import dirname,join
from subprocess import call
import json
# third-part dependencies
from concurrent.futures import ThreadPoolExecutor
from share import STR_RESULT,LOAD_TRANS_DATA,LOAD_TTS_DATA
from settings import *

import sys
reload(sys)
sys.setdefaultencoding('gb18030')


_RECONNECT_TIMES = 5
_TIMEOUT = 30

global _TRANS_URL
_MAX_TRANS_LENGTH = 100

global  _TTS_URL
_MAX_TTS_LENGTH = 99

global  _TRANS_PARAMS
global  _TTS_PARAMS


class _BaseRequestMinix(object):    
    """
    Description:
        request and handdle
        monitor thread until works finish.
    """

    def _request_with_reconnect(self, callback):        
        reconnect_times = _RECONNECT_TIMES        
        while True:            
            try:
                # request using callback function
                response = callback()                
                break
            except Exception as e:
                if reconnect_times == 0:            
                    # has already tried _RECONNECT_TIMES times, request failed.
                    # if so, just let it crash.                    
                    raise e
                else:                    
                    reconnect_times -= 1
        return response

    def _check_threads(self, threads):
        for future in threads:            
            if future.exception(_TIMEOUT) is None:                
                continue
            else:
                # let it crash.
                raise future.exception()

class _SplitTextMinix(object):    
    

    def _check_split_point(self, character, unicode_category):
        """
        Description:
            Accept a character and judge whether it is a unicode punctuation or
            not.
        Return Value:
            True for unicode punctuation and False for everything else.
        """

        if unicodedata.category(character) == unicode_category:
            return True
        else:
            return False

    def _find_split_point(self, text, start, end,
                          unicode_category, reverse=True):
        """
        Description:
            Try to find a split point in a range of some text. Be clear that
            the search range of text is [start, end-1].
        Return Value:
            int value in the range of [start, end].
        """
        # generate indices in range [start, end-1].
        indices = range(start, end)
        if reverse:
            indices = reversed(indices)
        # find split point
        modify_flag = False
        for index in indices:
            if self._check_split_point(text[index], unicode_category):
                # (index + 1) means that the punctuation is included in the
                # sentence(s) to be split. Reason of doing that is based on
                # the observation of google TTS HTTP request header.
                modify_flag = True
                end = index + 1
                break
        return modify_flag, end

    def _split_text(self, text, max_length):
        """
        Description:
            Receive unicode text, split it based on max_length(maximum
            number of characters). Unicode punctuations are the 'split points'
            of text. If there's no punctuations for split, unicode spaces are
            treated as split points. Otherwise, max_length is adopt for
            splitting text.
        Return Value:
            List cotains split text.
        """

        split_text = []
        start = 0
        end = max_length
        # reverse flag is for the case that a sentence is split in the middle.
        reverse_flag = True

        while end < len(text):
            split_po, end_po = self._find_split_point(text, start, end,
                                                      'Po', reverse_flag)
            split_zs, end_zs = self._find_split_point(text, start, end,
                                                      'Zs', reverse_flag)
            if split_po:
                end = end_po
                reverse_flag = True
            elif split_zs:
                end = end_zs
                reverse_flag = False

            split_text.append(text[start: end])
            # update indices
            start = end
            end = start + end
        split_text.append(text[start:])
        return split_text


class _TranslateMinix(_BaseRequestMinix):    
    """
    Description:
        Low-level method for HTTP communication with google translation service.
        wrap and resolve data received.
    """

    global _TRANS_URL,_TRANS_PARAMS
    
    def _basic_request(self, src_lang, tgt_lang, src_text):        
        """
        Description:
            POST request to translate.google.com. If connection failed,
            _basic_request would try to reconnect the server.
        Return Value:
            string data.
        """          

        request_data = LOAD_TRANS_DATA(src_lang, tgt_lang, src_text)

        def callback():
            # POST request
            headers = {'content-type': 'application/json'}
            response = requests.post(
                _TRANS_URL,
                data=request_data,
                params=_TRANS_PARAMS,                
            ) 
                   
            return response
        
        response = self._request_with_reconnect(callback) 
        return response.text    
    

    def _merge_text(self, text):
        """
        Description:
            Receive requests data for map/json... format data, returned by 
            _basic_request. With the observation of different result from 
            different translation tool, using the function STR_RESULT can
            help to create a string object.
        Return Value:
            String object.
        """
                
        if len(text) == 1: 
            return STR_RESULT(text[0],True)

        merged_text = ""
        
        for textItem in text:
            merged_text = merged_text + STR_RESULT(textItem,False)

        return merged_text

        

    def _request(self, src_lang, tgt_lang, src_texts):        
        """
        Description:
            Receive src_texts, which should be a list of texts to be
            translated. _request method calls _basic_request method for http
            request, and assembles the JSON dictionary returned by
            _basic_request. For case that _basic_request needs to be called
            multiple times, concurrent.futures package is adopt for the usage
            of threads concurrency.
        Return Value:
            String object.
        """                 
        executor = ThreadPoolExecutor(max_workers=len(src_texts))
        threads = []        
        for src_text in src_texts:                   
            future = executor.submit(
                self._basic_request,
                src_lang,
                tgt_lang,
                src_text,
            )            
            threads.append(future)
        
        # check whether all threads finished or not.
        self._check_threads(threads)      
        merged_text = self._merge_text(
            [future.result() for future in threads],
        )   
            
        return merged_text


class TranslateService(_TranslateMinix, _SplitTextMinix):

    def _translate(self, src_lang, tgt_lang, src_text):
        """
        Description:
            Split text and request for JSON dictionary.
        Return Value:
            Dictionary contains information about the result of translation.
        """

        # split text        
        src_texts = self._split_text(src_text, _MAX_TRANS_LENGTH)       
        # request with concurrency
        return self._request(src_lang, tgt_lang, src_texts)

    def trans_details(self, src_lang, tgt_lang, src_text):        
        """
        Description:
            Accept both UTF-8 or decoded unicode strings. trans_details means
            'translate in details'. Different from trans_sentence,
            trans_details method would return a dictionary containing more
            related information.
        Return Value:
            Dictionary contains information about the result of translation.
            Type of Data in the dictionary is Unicode(String in Py3).
        """        
        return self._translate(src_lang, tgt_lang, src_text)


class _TTSRequestMinix(_BaseRequestMinix):
    
    def _basic_request(self, from_lang, text):

        """
        Description:
            GET request for TTS of google translation service.If connection 
            failed, _basic_request would try to reconnect the server.
            handle audio/mpeg response.
        """
        global _TTS_URL,_TTS_PARAMS
        # e.g. word=hello&keyfrom=fanyi.web
        request_data = LOAD_TTS_DATA(from_lang, text)
        #_TTS_PARAMS.update(request_data)
        _TTS_PARAMS = dict(_TTS_PARAMS,**request_data)
        
        #_TTS_PARAMS = {'word':'hello','keyfrom':'fanyi.web'}
        def callback():
            # GET request
            response = requests.get(
                _TTS_URL,    
                params=_TTS_PARAMS, 
            )
            return response

        response = self._request_with_reconnect(callback)
        
        # save audio/mpeg to .mp3        

        mp3_file = join(dirname(__file__)) + os.sep + "../text2speech.mp3"
        with open(mp3_file, "wb+") as code:
            code.write(response.content)
        mpg123exeDir = join(dirname(__file__)) + os.sep + "mpg123.exe"
        call([mpg123exeDir,mp3_file])
        os.remove(mp3_file)


    def _request(self, from_lang, text):
        """
        Description:
            Similar to _TranslateMinix._request. Text should be in from_lang.
        """

        self._basic_request(from_lang, text)

class TTSService(_TTSRequestMinix, _SplitTextMinix):


    def speak_details(self, from_lang, text):
        """
        Description:
            request the Text To Speech api
        """
        self._request(from_lang, text)


def Global_settings():
    
    global _TRANS_URL,_TRANS_PARAMS,_TTS_URL,_TTS_PARAMS

    with open(TOOL_FILENAME, 'rb+') as f:
        content = f.read()
    content = eval(content)
    tool = content["TOOL"]

    if tool == "google":                
        _TRANS_URL = GOOGLE_TRANS_URL             
        _TTS_URL = GOOGLE_TTS_URL
        _TRANS_PARAMS = GOOGLE_TRANS_PARAMS
        _TTS_PARAMS = GOOGLE_TTS_PARAMS
    elif tool == "youdao":
        _TRANS_URL = YOUDAO_TRANS_URL             
        _TTS_URL = YOUDAO_TTS_URL
        _TRANS_PARAMS = YOUDAO_TRANS_PARAMS
        _TTS_PARAMS = YOUDAO_TTS_PARAMS
    return tool

if __name__ == '__main__':
        
    """
    Description
        only development test 
        users could just ignore
    """
    import platform
    audio_player = 'afplay' if platform.system() == 'Darwin' else 'mpg123'
    
    _SECTION_NAME = 'MyGoogleDict'
    _FROM_LANG = 'default_from_lang'
    _TO_LANG = 'default_to_lang'
    _AUDIO_PLAYBACK_COMMAND = 'audio_playback_command'
    
    _RAW_CONTENT = """
    [{}]
    {}: en
    {}: zh-CN
    {}: {}
    """
    content = _RAW_CONTENT.format(
        _SECTION_NAME,
        _FROM_LANG,
        _TO_LANG,
        _AUDIO_PLAYBACK_COMMAND, audio_player,
    )
    print(content)
    

    