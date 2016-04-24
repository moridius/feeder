# feeder
Yet another script to generate Atom feeds for web sites that don't provide a feed by themselves. Written in Python 3.
Just call the script with the URL as a parameter. If the site is not supported this will result in an error.

Currently supported sites:
- Twitter


Dependencies:
- lxml (https://pypi.python.org/pypi/lxml)
- feedgen (https://pypi.python.org/pypi/feedgen)
