#! /usr/bin/env python
#coding=utf-8

"""
Usage: dig [-f <from_lang>] [-t <to_lang>]
           [-v|--reverse] [-s|--speak] <data>...
       dig [-n <num>] -r|--record
       dig -c|--configure <tool>
       dig -h|--help 

Options:
    -f <from_lang>  input language [default: {default_from_lang}]
    -t <to_lang>    ouput language [default: {default_to_lang}]
    -v --reverse    reverse -f and -t
    -s --speak      speak out the result
    -n <num>        display n records [default: {default_num}]
    -r --record     display search record
    -c --configure  set current translation tool [google,youdao]
    -h --help       Ask for detailed help
    
Additional information:
    Now you has type 'dig -h|--help'. 
    You can get more in https://github.com/enjoyhot/dig/.
"""

from __future__ import unicode_literals
from __future__ import print_function
from os.path import dirname,join
from docopt import docopt
from dig.data_io import set_up_doc
from dig.translate import Translator,Speaker
from dig.record import Record
import os
from translate_api import Global_settings
from settings import *

def _assemble_data(raw_data):
    if len(raw_data) == 1:
        # single word
        return raw_data[0]
    elif len(raw_data) > 1:
        # multi-word sentence.
        return ' '.join(raw_data)


def _extract(arguments,has_data):
    """
    Description:
      extract input command args
    """
    from_lang = arguments['-f']
    to_lang = arguments['-t']
    data = _assemble_data(arguments['<data>'])
    reverse = arguments['--reverse']
    record_num = arguments['-n']
    # reverse langs
    from_lang, to_lang = (to_lang, from_lang)\
        if reverse else (from_lang, to_lang)
    if has_data:
        return from_lang, to_lang, data
    else:
        return record_num


def main():
        
    # save setting.TOOL to file
    if not os.path.exists(TOOL_FILENAME):
        tool_save = "{'TOOL':'" + CURRENT_TOOL + "'}"
        with open(TOOL_FILENAME, "wb+") as f:
            f.write(tool_save)    
    with open("dig/VERSION", "rb+") as f:
        VERSION = f.read()  
    
    arguments = docopt(
        set_up_doc(__doc__),
        version = VERSION
    )

    record = Record()
    
    if arguments['<data>']:
        
        tool = Global_settings()
        
        # extract 
        from_lang, to_lang, data = _extract(arguments,True)      
        
        # translate data, get the result, show the result
        translator = Translator(from_lang, to_lang, data)
        result = translator.translate()
        translator.display_result(from_lang,to_lang,result)
        
        # add record
        record.add(from_lang, to_lang,
                   data, result)

        # Text to Speech，be making sure data belongs to from_lang
        if arguments['--speak']:

            if (tool == "youdao")and(from_lang == "zh_CN"):
                print(tool + r" service doesn't support text2speech for " + from_lang)
            else:                
                speaker = Speaker(from_lang, data)
                speaker.speak()
                    
        
    elif arguments['--record']:
        '''
        display record_num records if there are so many record_num records
        '''
        record_num = _extract(arguments,False)    
        record.display(record_num)
        
    elif arguments['--configure']:
        
        with open(TOOL_FILENAME, 'rb+') as f:
            content = f.read()
        content = eval(content)
        tool = content["TOOL"]
        print("")
        print("----- Your current traslation tool: " + str(tool) + " -----")
        if arguments['<tool>'] not in OPTIONAL_TOOLS:  
            print("") 
            wrong_input = arguments['<tool>']        
            print("[WARNING] Wrong setting for " + str(wrong_input) + \
            "! Please choose one from " + str(OPTIONAL_TOOLS))
        else:
            """ 
            set current translation tool
            """             
            # save setting.TOOL to file
            tool_save = "{'TOOL':'" + arguments['<tool>'] + "'}"
            with open(TOOL_FILENAME, "wb+") as f:
                f.write(tool_save)            
                           
            print("")
            print("Change to " + arguments['<tool>'] + " successfully!")
            
    else:
        raise Exception('No Implemented Yet.')
    
    
    
