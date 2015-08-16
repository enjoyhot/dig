from __future__ import unicode_literals
from __future__ import print_function


import re
from functools import wraps
from settings import TOOL_FILENAME

def ensure_decode(func):
    def gbk_decoder(text):        
        GBK = "GBK"
        try:
            decoded = text.decode(GBK)
        except:
            # both decoded text and result(a dictionary variable contains
            # decoded information) would trigger exception. In this case, just
            # return the argument.
            decoded = text
        return decoded
    
    def utf8_decoder(text):
        UTF8 = 'UTF-8'
        try:
            decoded = text.decode(UTF8)
        except:
            # both decoded text and result(a dictionary variable contains
            # decoded information) would trigger exception. In this case, just
            # return the argument.
            decoded = text
        return decoded

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        decoded_args = map(gbk_decoder, args)
        decoded_kwargs = {k: gbk_decoder(v) for k, v in kwargs.items()}
        return func(self, *decoded_args, **decoded_kwargs)
    return wrapper



def LOAD_TRANS_DATA(src_lang, tgt_lang, src_text):
    
    with open(TOOL_FILENAME, 'rb+') as f:
        content = f.read()
    content = eval(content)

    if content["TOOL"] == "google":        
        data={'q': src_text,'sl':src_lang,'tl':tgt_lang,'h1': tgt_lang}    
    elif content["TOOL"] == "youdao":
        type = src_lang + "2" + tgt_lang        
        data={'i': src_text,'type': type}
    return data

def LOAD_TTS_DATA(from_lang, src_text):
    
    with open(TOOL_FILENAME, 'rb+') as f:
        content = f.read()
    content = eval(content)

    if content["TOOL"] == "google":
        data = {'q': src_text,'tl': from_lang,'textlen': str(len(src_text))}
    elif content["TOOL"] == "youdao":
        data = {'word' : src_text}
    return data


def STR_RESULT(hello,is_simple):

    with open(TOOL_FILENAME, 'rb+') as f:
        content = f.read()
    content = eval(content)

    if content["TOOL"] == "google":
        return googleStr2Result(hello,is_simple)
    elif content["TOOL"] == "youdao":
        return youdaoStr2Result(hello,is_simple)
    

def googleStr2Result(hello,is_simple):
       
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

    
def youdaoStr2Result(hello,is_simple):
    
    sentences = ""
    map_result = eval(hello)
    result_list = map_result["translateResult"]
    #k=re.compile(r',,,,|,,,|,,')     
    #hello = k.sub(r',None,',hello) 
    sentences = sentences + result_list[0][0]["tgt"]
    if not is_simple:
        return sentences
    if map_result.has_key("smartResult"):            
        for i in map_result["smartResult"]["entries"]:
            sentences = sentences + i + '\n'
    return sentences
