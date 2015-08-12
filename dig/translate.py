from __future__ import unicode_literals
from __future__ import print_function


from google_translate_api import TranslateService,TTSService
from dig.share import ensure_decode


class Translator:
    """
    Description:
        Translator Class, like top package
    """
    @ensure_decode
    def __init__(self, from_lang, to_lang, data, debug=False):
        self._debug = debug
        self._from_lang = from_lang
        self._to_lang = to_lang
        self._data = data

    def translate(self):
        translator = TranslateService()
        result = translator.trans_details(
            self._from_lang,
            self._to_lang,
            self._data,
        )
        return result

    @staticmethod
    def display_result(from_lang,to_lang,result):
        
        display_option = 'source lang: {0} ----> target lang: {1}'.format(from_lang,to_lang)
        print (display_option)
        print (result)


class Speaker:

    @ensure_decode
    def __init__(self, from_lang, text):
        self._from_lang = from_lang
        self._text = text

    def speak(self):
    
        tts = TTSService()
        tts.speak_details(self._from_lang,self._text)
