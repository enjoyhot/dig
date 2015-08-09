#! /usr/bin/env python
#coding=utf-8

"""
Usage: dig [-f <from_lang>] [-t <to_lang>]
           [-v|--reverse] [-s|--speak] <data>...
       dig [-n <num>] -r|--record

Options:
    -f <from_lang>  input language [default: {default_from_lang}]
    -t <to_lang>    ouput language [default: {default_to_lang}]
    -v --reverse    reverse -f and -t
    -s --speak      speak out the result
    -n <num>        display n records [default: {default_num}]
    -r --record     display search record
"""


#from __future__ import print_function
from os.path import dirname, join
from docopt import docopt
from dig.data_io import set_up_doc
from dig.translate import Speaker
from dig.translate import Translator
from dig.record import Record

def _assemble_data(raw_data):
    if len(raw_data) == 1:
        # single word
        return raw_data[0]
    elif len(raw_data) > 1:
        # multi-word sentence.
        return ' '.join(raw_data)


def _extract(arguments,has_data):
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

    arguments = docopt(
        set_up_doc(__doc__),
        version='0.1.0'
    )

    record = Record()
    
    if arguments['<data>']:
        # extract 
        from_lang, to_lang, data = _extract(arguments,True)      
        
        # translate data
        translator = Translator(from_lang, to_lang, data)
        # result is a dictionary contains decoded infomation of the
        # trnaslation.
        result = translator.translate()
        translator.display_result(from_lang,to_lang,result)
        
        
        if arguments['--speak']:
            speaker = Speaker(from_lang, data)
            speaker.speak()
            
        
        # add record
        record.add(from_lang, to_lang,
                   data, result)
        
    elif arguments['--record']:
        '''
        display record_num records if there are so many record_num records
        '''
        record_num = _extract(arguments,False)    
        record.display(record_num)
    else:
        raise Exception('No Implemented Yet.')
    
    
    
