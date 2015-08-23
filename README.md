# Dig 

[![alt PyPI Version](https://img.shields.io/pypi/v/Scrapy.svg "pip version")](https://pypi.python.org/pypi/dig)


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
* ...

### Youdao

* English : EN
* Chinese : ZH_CN
* Japanese : JA
* ...

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

**Note:**

In the way "pkg_resources.distributionnotfound:requests" maybe happen, just remove site-packages/requests, download [requests](https://pypi.python.org/pypi/requests#downloads) and install.

### Another way:
download [the whole package](https://github.com/enjoyhot/dig/archive/master.zip) and input as follows:
```python
$ python setup.py install
```
## Releases History

You can download the latest stable and development releases from: https://github.com/enjoyhot/dig/releases

**v0.1.10**

Bugfixes
* TTS fits for Windows7 or Linux platform.

**v0.1.9**

Bugfixes
* Update the dig for global Environment in windows dos or linux shell.

## Important points

1. You should install mpg123 if your platform is Linux.
2. Now only support google and youdao translation, make sure your computer can connect to google.com or youdao.com. 


## Problems

Only for Win7: There was wrong when piping for [requests](https://pypi.python.org/pypi/requests#downloads) packages, so download it individually.


## Learn how to make your package support pip
see https://github.com/enjoyhot/dig/wiki