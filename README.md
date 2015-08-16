#Dig 

Version 0.1.2

#Overview

Dig is a command-line program which now communicates with google/youdao
translation server. It can be used for look up the words or sentences through
google/youdao translation server.

#Requirement

##Python 3.+

* [Docopt](https://github.com/docopt/docopt) v0.6.2 is adopt for parsing arguments. 
* Works on Linux, Windows

##Python 2.7

* [futures](https://pypi.python.org/pypi/futures/) v3.0.3 is adopt for concurrence and compatibility. See .
* [Docopt](https://github.com/docopt/docopt) v0.6.2 is adopt for parsing arguments. 
* Works on Linux, Windows

# Install

## The quick way:
```python
$ pip install dig
```
See https://pypi.python.org/pypi/dig

## Another way:
download [the whole package](https://github.com/enjoyhot/dig/archive/master.zip) and input as follows:
```python
$ python setup.py install
```

# Command-line usage
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

# Important points

<<<<<<< HEAD
1. If you use "pip install dig", because [dig/mpg123.exe](https://github.com/enjoyhot/dig/blob/master/dig/mpg123.exe) doesn't exist,so add it in case of error when using text to speech.
2. Now only support google and youdao translation, make sure your computer can connect to google.com or youdao.com.
4. Text to speech function is effective only in win7/xp platform. 

=======
1. Now only support google translation.
2. Make sure your computer can connect to google.com.
3. Text to speech function is effective only in win7/xp platform. 

# Uncompleted problems

* Mix with other translation tools
* Decoupling, adapt change 
* Support pip download
* Bugs undiscovered
>>>>>>> origin/master
