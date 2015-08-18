#! /usr/bin/env python
#coding=utf-8

from __future__ import unicode_literals
from __future__ import print_function

import os,sys
from os.path import join,dirname
import gzip
import xml.etree.ElementTree as ET
_ROOT = 'records'

try:
    import ConfigParser as configparser
except:
    import configparser

# __DATA_DIR hard coded the directory contains records and configuation
# file.
_DATA_DIR = join(dirname(__file__))
_CONFIG_FILENAME = 'config'
_RECORD_FILENAME = 'record.xml' 

# fields in configuration file.
_SECTION_NAME = 'Dict_DATA_IO'
_FROM_LANG = 'default_from_lang'
_TO_LANG = 'default_to_lang'
_AUDIO_PLAYBACK_COMMAND = 'audio_playback_command'
_RECORD_NUM = 'default_num'

_RAW_CONTENT = """
[{}]
{}: en
{}: zh-CN
{}: {}
{}: 0
"""


def _generate_default_config_content():
    import platform
    audio_player = 'afplay' if platform.system() == 'Darwin' else 'mpg123'

    content = _RAW_CONTENT.format(
        _SECTION_NAME,
        _FROM_LANG,
        _TO_LANG,
        _AUDIO_PLAYBACK_COMMAND, audio_player,
        _RECORD_NUM,
    )
    return content

_DEFAULT_CONFIG_CONTENT = _generate_default_config_content()


class RecordIO(object):

    def __init__(self):
        
        self._record_path = os.path.join(
            _DATA_DIR,
            _RECORD_FILENAME,
        )
                
        if os.path.exists(self._record_path) == False:
            xml_file = self._create_xml()
            xml_file.write(self._record_path)
            
    def _create_xml(self):
        xml_file = ET.ElementTree()
        purOrder = ET.Element(_ROOT)
        xml_file._setroot(purOrder)
        return xml_file
        
        
    
    def _read_file(self, path, gzip_enable=False):
        """
        Parameters:
            path: points to file to be read.
            gzip_enable: Ture for using gzip.open(), False for using built-in
                         open().
        Return:
            Content of file represented in bytes.
        """

        openfile = gzip.open if gzip_enable else open
        with openfile(path, 'rb+') as f:
            content = f.read()
        #import xml.etree.ElementTree as ET 
        self.tree = ET.parse(path)     
        root = self.tree.getroot()
        return root

    def _write_file(self, path, gzip_enable=False):
        """
        Parameters:
            path: record.xml path.
            others: equivalent to _read_file.
        Function:
            Commit and update xml tree.
        Return:
            None.
        """
        self.tree.write(path)
        
    #############
    # Record IO #
    #############

    def _read_record(self):        
        return self._read_file(self._record_path)

    def _write_record(self, content):
        self._write_file(self._record_path)

    # == record.py._RECORD
    record = property(_read_record, _write_record)


class ConfigIO(object):

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.readfp(self._open_config())

    def _init_config(self):
        # check existence of data dir.
        if not os.path.exists(_DATA_DIR):
            os.makedirs(_DATA_DIR)

        path = os.path.join(
            _DATA_DIR,
            _CONFIG_FILENAME,
        )
        # assure existence of configuration file
        if not os.path.exists(path):
            # generate default configuation file.
            # text mode is required, for writing unicode literals.
            with open(path, 'w') as f:
                f.write(_DEFAULT_CONFIG_CONTENT)
        # finally, return that path.
        return path

    def _open_config(self):
        path = self._init_config()
        # return file object, with default mode wt.
        return open(path)

    def set_up_doc(self, doc):
        return doc.format(
            default_from_lang=self._config.get(_SECTION_NAME,
                                               _FROM_LANG),
            default_to_lang=self._config.get(_SECTION_NAME,
                                             _TO_LANG),
            default_num=self._config.get(_SECTION_NAME,
                                            _RECORD_NUM),                                            
        )

def set_up_doc(doc):
    config_io = ConfigIO()
    return config_io.set_up_doc(doc)


