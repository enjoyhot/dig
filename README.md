# Dig 

   ![image](https://img.shields.io/pypi/v/Scrapy.svg)
   :target: https://pypi.python.org/pypi/dig
   :alt: PyPI Version

## Overview

Dig is a command-line program which now communicates with google/youdao
translation server. It can be used for look up the words or sentences through
google/youdao translation server.

## Command-line usage
	Usage: dig [-f <from_lang>] [-t <to_lang>]
			   [-v|--reverse] [-s|--speak] <data>...
		   dig [-n <num>] -r|--record
		   dig -c|--configure <tool>
		   dig -h|--help 
		   
	Options:
		-f <from_lang>  input language [default: en]
		-t <to_lang>    ouput language [default: zh_CN]
		-v --reverse    reverse -f and -t
		-s --speak      speak out the result
		-n <num>        display n records [default: 0(That means all record)]
		-r --record     display search record
		-c --configure  set current translation tool [google,youdao]
		-h --help       ask for detailed help	
	
Examples:
 
		$ dig -c
		----- Your current translation tool: youdao -----
		[warning]...
		$ dig -c google
		----- Your current translation tool: youdao -----
		Change to google successfully!
		$ dig -f en -t zh_CN hello
		source lang: en ----> target lang: zh_CN
		您好 你好 打招呼 招呼 问好
		$ dig hello
		source lang: en ----> target lang: zh_CN
		您好 你好 打招呼 招呼 问好
		$ dig -v 你好
		source lang: zh_CN ----> target lang: en
		Hello
		$ dig Life is short,I use python.
		人生苦短，我使用Python。
		$ dig -t ja hello
		こんにちは ハロー のhello ようこそ 
		$ dig -r
		===========================================
		time:08/17/15 20:41:24
		from_lang:ento_lang:zh_CN
		data:hello
		result:您好 你好 打招呼 招呼 问好 
		===========================================
		$ dig -s hello
		source lang: en ----> target lang: zh_CN
		您好 你好 打招呼 招呼 问好
		Listening...
		
		More..........dig --help................
		


## Language format

### Google

* English : en
* Chinese : zh_CN
* Japanese : ja
...

### Youdao

* English : EN
* Chinese : ZH_CN
* Japanese : JA
...

## Requirements

### Python 3.+

* [Docopt](https://github.com/docopt/docopt) v0.6.2 is adopt for parsing arguments. 
* Works on Linux, Windows, BSD

### Python 2.7

* [futures](https://pypi.python.org/pypi/futures/) v3.0.3 is adopt for concurrence and compatibility. 
* [Docopt](https://github.com/docopt/docopt) v0.6.2 is adopt for parsing arguments. 
* Works on Linux, Windows, BSD

## Install

### The quick way:
```python
$ pip install dig
```
See https://pypi.python.org/pypi/dig
** Note:in the way "pkg_resources.distributionnotfound:requests" maybe happen, just remove site-packages/requests, download [requests](https://pypi.python.org/pypi/requests#downloads) and install.**

### Another way:
download [the whole package](https://github.com/enjoyhot/dig/archive/master.zip) and input as follows:
```python
$ python setup.py install
```
## Releases

You can download the latest stable and development releases from: https://github.com/enjoyhot/dig/releases

## Important points

1. If you use "pip install dig", because [dig/mpg123.exe](https://github.com/enjoyhot/dig/blob/master/dig/mpg123.exe) doesn't exist,so add it in case of error when using text to speech.
2. Now only support google and youdao translation, make sure your computer can connect to google.com or youdao.com.
3. Text to speech function is effective only in win7/xp platform. 

## Problems
pip for packages requests!!!