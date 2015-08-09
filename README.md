#Requirement

##PY 3.+
* [docopt](https://github.com/docopt/docopt) v0.6.2 is adopt for parsing arguments.

##PY 2.+
* [futures]https://pypi.python.org/pypi/futures/ v3.0.3 is adopt for concurrence and compatibility.
* [docopt](https://github.com/docopt/docopt) v0.6.2 is adopt for parsing arguments.
```python
python setup.py install
```
# Command line's usage
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
		

# Important
Now only support google translation, and the computer can connect to google.com yet.

# Not completed problems
* mix with other translation tools
* decoupling, adapt change 
* support pip download
* bugs undiscovered