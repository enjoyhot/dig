#! /usr/bin/env python
#coding=utf-8

"""
Usage: dig [-f <from_lang>] [-t <to_lang>]
           [-v|--reverse] [-s|--speak] <data>...
       dig -r|--record

Options:
    -f <from_lang>  input language [default: {default_from_lang}]
    -t <to_lang>    ouput language [default: {default_to_lang}]
    -v --reverse    reverse -f and -t
    -s --speak      speak out the result
    -r --record     display search record
"""


#from __future__ import print_function
from os.path import dirname, join
from docopt import docopt
from dig.data_io import set_up_doc

def _assemble_data(raw_data):
    if len(raw_data) == 1:
        # single word
        return raw_data[0]
    elif len(raw_data) > 1:
        # multi-word sentence.
        return ' '.join(raw_data)


def _extract(arguements):
    from_lang = arguements['-f']
    to_lang = arguements['-t']
    data = _assemble_data(arguements['<data>'])
    reverse = arguements['--reverse']
    # reverse langs
    from_lang, to_lang = (to_lang, from_lang)\
        if reverse else (from_lang, to_lang)

    return from_lang, to_lang, data


def main():
    
    #返回字典
    arguments = docopt(
        set_up_doc(__doc__),
        version='0.1.0'
    )
    print(arguments)

    '''
    record = Record()
    '''
    if arguments['<data>']:
        # translation
        from_lang, to_lang, data = _extract(arguments)
        print from_lang,to_lang,data
        
        # translate data
        translator = Translator(from_lang, to_lang, data)
        # result is a dictionary contains decoded infomation of the
        # trnaslation.
        result = translator.translate()
        translator.display_result(result)

        if arguements['--speak']:
            speaker = Speaker(from_lang, data)
            speaker.speak()

        # add record
        record.add(from_lang, to_lang,
                   data, result)

    elif arguements['--record']:
        # display record
        record.display()
    else:
        raise Exception('No Implemented Yet.')
    '''
    
