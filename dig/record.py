#! /usr/bin/env python
#coding=utf-8

from __future__ import unicode_literals
from __future__ import print_function

from datetime import datetime
import xml.etree.ElementTree as ET

from dig.share import ensure_decode
from dig.data_io import RecordIO


"""
two usage
    1.data.io record variable
    2.xml element name
"""
_RECORD = 'record'

_TAGLIST = ['time','from_lang','to_lang','data','result']


class Record:

    def __init__(self, debug=False):
        self._debug = debug
        self._record_io = RecordIO()

    def _load_xml(self, field_name):
        try:
            root = getattr(self._record_io, field_name)  
            
        except:
            # "The element name, attribute names, and attribute values can be
            # either bytestrings or Unicode strings." Thus, unicode should be
            # ok.
            root = ET.Element(_ROOT)
        return root

    def _write_xml(self, field_name):
        # Holly Shit, ASCII encoding works.
        # raw_xml = ET.tostring(xml)
        setattr(self._record_io, field_name,'')


    @ensure_decode
    def add(self,
            from_lang,
            to_lang,
            data,
            result):
        """
        Parameters:
            from_lang: data's language.
            to_lang: result's language.
            data: input text.
            result: translation of data.

            All parameters are decoded to unicode strings if they are whatever
            else.
        Return:
            None.
        """                

        # read root from xml record file
        
        root = self._load_xml(_RECORD)
        
        from settings import MAX_RECORD_NUM
        while len(root) >= MAX_RECORD_NUM:        
            topRecord = root.find(_RECORD)
            root.remove(topRecord)
            
        
        #extend(subelements)
        # "The element name, attribute names, and attribute values can be
        # either bytestrings or Unicode strings." Thus, unicode should be
        # ok.
    
        dt = datetime.now()
        dtStr = '%s' % dt.strftime('%c')
        
        textList = [dtStr,from_lang,to_lang,data,result]
        
        record = ET.SubElement(root, _RECORD)
        for index,tag in enumerate(_TAGLIST):
            temp = ET.Element(tag)  
            temp.text = textList[index]
            record.append(temp)
        
        
        self._write_xml(_RECORD)
        
    def display_record(self,root, from_index):

        if from_index == len(root):
            from_index = 0
            
        for index,record in enumerate(root):
            if index >= from_index:
                print('===========================================')
                for child in record:           
                    print(child.tag + ":" + child.text)         
            
        print('===========================================') 
        

    def display(self, record_num):
        
        # targeting on record file
        root = self._load_xml(_RECORD)
        record_num = int(record_num)
        self.display_record(root,len(root)-record_num)

