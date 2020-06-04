# coding: utf-8

if hasattr(iter([]), "next"):
    nextmethod = "next"
else:
    nextmethod = "__next__"

try:
    basestring = basestring
except NameError:
    basestring = str

try:
    xrange = xrange
except NameError:
    xrange = range

try:
    inttype = (int, long)
except NameError:
    inttype = int

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        # for python3
        from io import StringIO
try:
    viewvalues = dict.viewvalues
except AttributeError:
    viewvalues = dict.values

try:
    from dateutil.relativedelta import relativedelta as timedelta
except ImportError:
    from datetime import timedelta

try:
    # python 3.x ?
    if bytes is not str:

        def stringify(something):
            return str(something).encode("utf8")

    else:
        # 2.7 or 2.6
        stringify = str
except NameError:
    # 2.5 or older
    stringify = str
