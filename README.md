#Requirement

dig is a simple command-line program which Communicates with translation server such as [translate.google.com](http://translate.google.com/) for translation bussiness.

##python 3.+
* [docopt](https://github.com/docopt/docopt) v0.6.2 is adopt for parsing arguments.

##python 2.7
* [futures](https://pypi.python.org/pypi/futures/ v3.0.3 is adopt for concurrence and compatibility.
* [docopt](https://github.com/docopt/docopt) v0.6.2 is adopt for parsing arguments.
```python
$ python setup.py install
```
# Command-line usage
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
		

# Important points

1. Now only support google translation.
2. Make sure your computer can connect to google.com.
3. Text to speech function is effective only in win7/xp platform. 

# Uncompleted problems

* Mix with other translation tools
* Decoupling, adapt change 
* Support pip download
* Bugs undiscovered
