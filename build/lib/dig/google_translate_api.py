#! /usr/bin/env python
#coding=utf-8

from __future__ import unicode_literals
from __future__ import print_function

# standrad packages
import unicodedata
import requests
import re
import os
from subprocess import call
# third-part dependencies
from concurrent.futures import ThreadPoolExecutor


import sys
reload(sys)
sys.setdefaultencoding('gb18030')


_UTF8 = 'UTF-8'
_RECONNECT_TIMES = 5
_TIMEOUT = 30

_GOOGLE_TRANS_URL = 'http://translate.google.com/translate_a/single'
_MAX_TRANS_LENGTH = 2000

_GOOGLE_TTS_URL = 'http://translate.google.cn/translate_tts'
_MAX_TTS_LENGTH = 99


# keys in json data.
SENTENCES = 'sentences'
TRANS = 'trans'

DICT = 'dict'
POS = 'pos'
TERMS = 'terms'

SRC = 'src'



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
    Low-level method for HTTP communication with google translation service.
    包装数据和解析接收到数据
    """

    def _basic_request(self, src_lang, tgt_lang, src_text):        
        """
        Description:
            POST request to translate.google.com. If connection failed,
            _basic_request would try to reconnect the server.
        Return Value:
            Dictionary contains unicode JSON data.
        """


        params = {
            'client': 't',
            'sl': src_lang,
            'tl': tgt_lang,
            'h1': tgt_lang,
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

            'ie': _UTF8,
            'oe': _UTF8,     
            'srcrom': '0',
            'ssel': '0',
            'tsel': '0',
            'kc': '1',
            'tk': '522913|331595',
        }
        
                
        def callback():
            # POST request
            headers = {'content-type': 'application/json'}
            response = requests.post(
                _GOOGLE_TRANS_URL,
                data={'q': src_text},
                params=params,                
            ) 
            # data={'q': src_text,params}
            # response = post(_GOOGLE_TRANS_URL, params)                     
            return response
        
        response = self._request_with_reconnect(callback)              
        return response.text
    
    def _str2result(self,hello):
           
        hello = str(hello)
        k=re.compile(r',,,,|,,,|,,')     
        hello = k.sub(r',None,',hello)      
        k=re.compile(r'false|true')     
        hello = k.sub(r'None',hello)   
        k=re.compile(r'\[,') 
        hello = k.sub(r'[None,',hello)  
        k=re.compile(r',\]') 
        hello = k.sub(r',None]',hello)        
        a = list(eval(hello)) 
       
        # a = list(eval(b[0]))  
        if(len(a) < 5):
            return str("have no result.")
        slipSen = a[4]
        if(len(slipSen[0]) < 3):
            return str("have no result.")            
        total = []
        for word2 in slipSen:            
            i = 0    
            result = []                    
            for word1 in word2[2]:  
                #print str(word1[i][0])        
                result.append(str(word2[2][i][0]))
                i=i+1 
                #print (str(i) + str("34"))
            total.append(result)
        # if it is just a simple word or two.
        sentences = ""
        if len(total) != 1:            
            for words in total:
                sentences = sentences + words[0]
        else:
            for word in total[0]:
                sentences = sentences + word + " "
        return sentences
    

    def _merge_text(self, text):
        """
        Description:
            Receive JSON dictionaries returned by _basic_request. With the
            observation of JSON response of translate.google.com, we can see
            that:
                1. For single word translation, JSON dictionary contains more
                information compared to sentence translation.
                2. For multi-word sentence translation, there are three keys in
                JSON dictionary, 'sentences', 'server_time' and 'src'. The JSON
                dictionary returned by single word translation, on the other
                hand, has an extra key 'dict' whose value related to details
                of the meanings.
            Therefore, for jsons has the length greater than one, _merge_json
            would just merge the value of 'sentences' key in jsons. For the
            accuracy of language detectation, values of 'src' key in jsons
            would be analysed and stored as a dictionary, with language code as
            its key and the proportion as its value.
        Return Value:
            Dictionary contains unicode JSON data.
        """
        

        if len(text) == 1:   
            return self._str2result(text[0])

        merged_text = ""
    
        
        for textItem in text:
            merged_text = merged_text + self._str2result(textItem)

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
            Dictionary contains unicode JSON data.
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


    @classmethod
    def get_senteces_from_json(cls, json_data):
        """
        Return:
            Unicode strings.
        """

        sentences = map(
            lambda x: x[TRANS],
            json_data[SENTENCES],
        )
        return ''.join(sentences)

    @classmethod
    def has_pos_terms_pairs(cls, json_data):
        return DICT in json_data

    @classmethod
    def get_pos_terms_pairs_from_json(cls, json_data):
        assert DICT in json_data,\
            'pos-temrs pair not exist, try cls.has_pos_terms_pairs'
        for entity in json_data.get(DICT):
            pos = entity[POS] or 'error_pos'
            vals = entity[TERMS][:]
            yield pos, vals

    @classmethod
    def get_src_language_from_json(cls, json_data):
        return json_data[SRC]


class _TTSRequestMinix(_BaseRequestMinix):

    def _basic_request(self, from_lang, text):
        """
        Description:
            GET request for TTS of google translation service.
        Return Value:
            audio/mpeg response.
        """

        params = {
            'ie': 'UTF-8',
            'q' : text,
            'tl': from_lang,
            'total': '1',
            'idx': '0',
            'textlen': str(len(text)),
            'tk': '903567',
            'client': 't',
            'prev': 'input',
            'ttsspeed': '0.24',
        }                  

        def callback():
            # GET request
            response = requests.get(
                _GOOGLE_TTS_URL,    
                params=params, 
            )
            return response

        response = self._request_with_reconnect(callback)
        
        # save audio/mpeg to .mp3
        with open("text2speech.mp3", "wb+") as code:
             code.write(response.content)
        mpg123exeDir = os.getcwd() + os.sep + "dig" +  os.sep + "mpg123.exe"
        call([mpg123exeDir,"text2speech.mp3"])
        os.remove("text2speech.mp3")


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
    

    