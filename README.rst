.. image:: https://badge.fury.io/py/datafactory.svg
  :target: https://badge.fury.io/py/datafactory

.. image:: https://github.com/walkframe/datafactory/workflows/master/badge.svg
  :target: https://github.com/walkframe/datafactory/actions

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :target: https://github.com/python/black

.. image:: https://codecov.io/gh/walkframe/datafactory/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/walkframe/datafactory

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
  :target: https://opensource.org/licenses/Apache-2.0


Overview
===========
`datafactory` makes **flexible** data according to the given rules.

The features are divided into `field`, `model`, `container`, and `formatter`.
If you compare it to a DB, fields are columns, models are records, and containers are tables.

The great thing about the `datafactory` is its flexibility in type specification. 
Containers can also be nested.

`formatter` supports data formatting and file output.

Requirements
============

- Python 3.5 or later.


Install
=======

.. code-block:: sh

  $ pip install datafactory


Usage
=====

Basic Example
-------------

.. code-block:: python3

  In [1]: import datafactory
 
  In [2]: model = datafactory.Model({
     ...:     'id': datafactory.IncrementField(),
     ...:     'x': datafactory.CycleField(['a', 'b', 'c']),
     ...:     # BLANK will be omit.
     ...:     'option': datafactory.ChoiceField([True, False, datafactory.BLANK]),
     ...: })
 
  In [3]: container = datafactory.Container(model, 5, render=True)
 
  In [4]: container
  Out[4]:
  [{'id': 1, 'x': 'a'},
   {'id': 2, 'x': 'b', 'option': False},
   {'id': 3, 'x': 'c', 'option': True},
   {'id': 4, 'x': 'a'},
   {'id': 5, 'x': 'b'}]
 
  # specify rewrite=True, if file already exists.
  In [5]: datafactory.JsonFormatter(container).write('/tmp/test.json', rewrite=True)
 
  In [6]: !cat /tmp/test.json
  [
   {
    "x": "a",
    "id": 1
   },
   {
    "x": "b",
    "id": 2,
    "option": false
   },
   {
    "x": "c",
    "id": 3,
    "option": true
   },
   {
    "x": "a",
    "id": 4
   },
   {
    "x": "b",
    "id": 5
   }
  ]

TSV Example
-----------

.. code-block:: python3

  In [1]: import datafactory
 
  In [2]: model = datafactory.ListModel([
     ...:     datafactory.IncrementField(start=10, step=5),
     ...:     datafactory.HashOfField(2, 'md5'),  # hashing value of the third column.
     ...:     datafactory.ChoiceField(['foo', 'bar', 'baz']),
     ...:     datafactory.CycleField(range(0, 30, 10)),
     ...: ]).ordering(2)  # render at first index:2(third column)
 
  # IterContainer is saving memory, because generating an element each time.
  In [3]: container = datafactory.IterContainer(model, 10)  # repeat 10 times.
 
  In [4]: datafactory.CsvFormatter(
     ...:     container,
     ...:     delimiter='\t',
     ...:     header=['id', 'hash-of-name', 'name', 'value']
     ...: ).write('/tmp/test.csv', rewrite=True)
 
  In [5]: !cat /tmp/test.csv
  id	hash-of-name	name	value
  10	acbd18db4cc2f85cedef654fccc4a4d8	foo	0
  15	acbd18db4cc2f85cedef654fccc4a4d8	foo	10
  20	73feffa4b7f6bb68e44cf984c85f6e88	baz	20
  25	acbd18db4cc2f85cedef654fccc4a4d8	foo	0
  30	acbd18db4cc2f85cedef654fccc4a4d8	foo	10
  35	73feffa4b7f6bb68e44cf984c85f6e88	baz	20
  40	73feffa4b7f6bb68e44cf984c85f6e88	baz	0
  45	73feffa4b7f6bb68e44cf984c85f6e88	baz	10
  50	37b51d194a7513e45b56f6524f2d51f2	bar	20
  55	37b51d194a7513e45b56f6524f2d51f2	bar	0

Custom Example
--------------
If object is callable, it stores execution result.

Model
~~~~~

.. code-block:: python3

 In [1]: import datafactory

 In [2]: def square(k, i):
    ...:     return k * i
    ...:

 In [3]: container = datafactory.DictContainer(square)

 In [4]: container(['a', 'b', 'c', 'd', 'e'])
 Out[4]: {'a': '', 'b': 'b', 'c': 'cc', 'd': 'ddd', 'e': 'eeee'}


Field
~~~~~~~

.. code-block:: python3

 In [1]: import datafactory

 In [2]: model = datafactory.Model({
    ...:    'col1': (lambda r, i: i),
    ...:    'col2': (lambda r: r['col1'] + 1),
    ...:    'col3': (lambda r: r['col2'] * 2),
    ...:    'col4': 100,  # fixed value
    ...: }).ordering('col1', 'col2', 'col3')

 In [3]: container = datafactory.ListContainer(model)

 In [4]: container(4)
 Out[4]:
 [{'col1': 0, 'col2': 1, 'col3': 2, 'col4': 100},
  {'col1': 1, 'col2': 2, 'col3': 4, 'col4': 100},
  {'col1': 2, 'col2': 3, 'col3': 6, 'col4': 100},
  {'col1': 3, 'col2': 4, 'col3': 8, 'col4': 100}]


Limited number of element Example
---------------------------------

.. code-block:: python3

 In [1]: import datafactory

 In [2]: model = datafactory.Model({
    ...:     # x: a is 1times limited. / b is 2times limited. / c is 3times limited.
    ...:     'x': datafactory.PickoutField({'a': 1, 'b': 2, 'c': 3}, missing=None),
    ...:     # y: a is 2times limited. / b and c is 1times limited.
    ...:     'y': datafactory.PickoutField(['a', 'a', 'b', 'c'], missing='*'),
    ...:     # z: a and b can't be selected. / c is 5times limited.
    ...:     'z': datafactory.PickoutField(['c']*5, missing=None),
    ...: })

 In [3]: container = datafactory.ListContainer(model)

 In [4]: container(6)
 Out[4]:
 [{'x': 'a', 'y': 'a', 'z': 'c'},
  {'x': 'c', 'y': 'b', 'z': 'c'},
  {'x': 'c', 'y': 'a', 'z': 'c'},
  {'x': 'b', 'y': 'c', 'z': 'c'},
  {'x': 'c', 'y': '*', 'z': 'c'},
  {'x': 'b', 'y': '*', 'z': None}]


Combination Example
-------------------
To generate the testdata that combines multiple elements
can be achieved by using the repeat-argument of `CycleField` and `SequenceField`.

.. code-block:: python3

 In [1]: import datafactory

 In [2]: l0 = ['a', 'b']

 In [3]: l1 = ['a', 'b', 'c']

 In [4]: l2 = ['a', 'b', 'c', 'd']

 In [5]: model = datafactory.ListModel([
    ...:     datafactory.SequenceField(l0, repeat=len(l1)*len(l2), missing=datafactory.ESCAPE),
    ...:     datafactory.CycleField(l1, repeat=len(l2)),
    ...:     datafactory.CycleField(l2),
    ...: ])

 In [6]: container = datafactory.Container(model)

 # by specifying the ESCAPE to missing-argument
 # automatically detect end of elements and escape before reaching 10000.
 In [7]: container(10000)
 Out[7]:
 [['a', 'a', 'a'],
  ['a', 'a', 'b'],
  ['a', 'a', 'c'],
  ['a', 'a', 'd'],
  ['a', 'b', 'a'],
  ['a', 'b', 'b'],
  ['a', 'b', 'c'],
  ['a', 'b', 'd'],
  ['a', 'c', 'a'],
  ['a', 'c', 'b'],
  ['a', 'c', 'c'],
  ['a', 'c', 'd'],
  ['b', 'a', 'a'],
  ['b', 'a', 'b'],
  ['b', 'a', 'c'],
  ['b', 'a', 'd'],
  ['b', 'b', 'a'],
  ['b', 'b', 'b'],
  ['b', 'b', 'c'],
  ['b', 'b', 'd'],
  ['b', 'c', 'a'],
  ['b', 'c', 'b'],
  ['b', 'c', 'c'],
  ['b', 'c', 'd']]

nested example
--------------

.. code-block:: python3

 In [1]: import datafactory

 In [2]: model = datafactory.Model({
    ...:     'a': datafactory.ListModel([
    ...:         datafactory.CycleField(['b', 'c']),
    ...:         datafactory.CycleField(['d', 'e']),
    ...:     ]),
    ...:     datafactory.ChoiceField(['f', 'g', 'h']): datafactory.DictContainer(lambda x: x * 2, 5)
    ...: })

 In [3]: datafactory.Container(model, 10, render=True)
 Out[3]:
 [{'a': ['b', 'd'], 'h': {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}},
  {'a': ['c', 'e'], 'f': {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}},
  {'a': ['b', 'd'], 'f': {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}},
  {'a': ['c', 'e'], 'g': {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}},
  {'a': ['b', 'd'], 'f': {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}},
  {'a': ['c', 'e'], 'h': {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}},
  {'a': ['b', 'd'], 'g': {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}},
  {'a': ['c', 'e'], 'h': {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}},
  {'a': ['b', 'd'], 'h': {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}},
  {'a': ['c', 'e'], 'h': {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}}]

datetime Utility
----------------

choice
~~~~~~

random choice between start and end.

.. code-block:: python3

 In [1]: from datafactory.utils.datetime import choice


 In [2]: choice(1988, '2015-11-11T11:11:11.111111')
 Out[2]: datetime.datetime(2009, 11, 30, 23, 25, 43, 240031)

 # tuple: datetime(*tuple), dict: datetime(**dict)
 In [3]: choice((1988, 5, 22), {'year': 2015, 'month': 11, 'day': 11})
 Out[3]: datetime.datetime(1996, 7, 1, 11, 14, 59, 314809)

 In [4]: from datetime import datetime, date

 In [5]: choice(date(1988, 5, 22), datetime(2015, 11, 11, 11, 11, 11))
 Out[5]: datetime.datetime(2011, 3, 23, 19, 39, 14, 476901)

generator
~~~~~~~~~

generator that generate the datetime object at regular intervals.

.. code-block:: python3

 In [1]: from datetime import timedelta
 In [2]: from datafactory.utils.datetime import generator

 # if you omit end-argument, then it creates an object infinitely.
 In [3]: g = generator(start=2015, interval=timedelta(days=1, hours=12))

 In [4]: next(g)
 Out[4]: datetime.datetime(2015, 1, 1, 0, 0)

 In [5]: next(g)
 Out[5]: datetime.datetime(2015, 1, 2, 12, 0)

 In [6]: next(g)
 Out[6]: datetime.datetime(2015, 1, 4, 0, 0)

 In [7]: next(g)
 Out[7]: datetime.datetime(2015, 1, 5, 12, 0)

range
~~~~~

generate list object that includes regularly generated datetime objects element.

.. code-block:: python3

 In [1]: from datetime import timedelta
 In [2]: from datafactory.utils.datetime import range

 In [3]: range(2015, '2015/2/1')
 Out[3]:
 [datetime.datetime(2015, 1, 1, 0, 0),
  datetime.datetime(2015, 1, 2, 0, 0),
  datetime.datetime(2015, 1, 3, 0, 0),
  datetime.datetime(2015, 1, 4, 0, 0),
  datetime.datetime(2015, 1, 5, 0, 0),
  datetime.datetime(2015, 1, 6, 0, 0),
  datetime.datetime(2015, 1, 7, 0, 0),
  datetime.datetime(2015, 1, 8, 0, 0),
  datetime.datetime(2015, 1, 9, 0, 0),
  datetime.datetime(2015, 1, 10, 0, 0),
  datetime.datetime(2015, 1, 11, 0, 0),
  datetime.datetime(2015, 1, 12, 0, 0),
  datetime.datetime(2015, 1, 13, 0, 0),
  datetime.datetime(2015, 1, 14, 0, 0),
  datetime.datetime(2015, 1, 15, 0, 0),
  datetime.datetime(2015, 1, 16, 0, 0),
  datetime.datetime(2015, 1, 17, 0, 0),
  datetime.datetime(2015, 1, 18, 0, 0),
  datetime.datetime(2015, 1, 19, 0, 0),
  datetime.datetime(2015, 1, 20, 0, 0),
  datetime.datetime(2015, 1, 21, 0, 0),
  datetime.datetime(2015, 1, 22, 0, 0),
  datetime.datetime(2015, 1, 23, 0, 0),
  datetime.datetime(2015, 1, 24, 0, 0),
  datetime.datetime(2015, 1, 25, 0, 0),
  datetime.datetime(2015, 1, 26, 0, 0),
  datetime.datetime(2015, 1, 27, 0, 0),
  datetime.datetime(2015, 1, 28, 0, 0),
  datetime.datetime(2015, 1, 29, 0, 0),
  datetime.datetime(2015, 1, 30, 0, 0),
  datetime.datetime(2015, 1, 31, 0, 0),
  datetime.datetime(2015, 2, 1, 0, 0)]

 # +-3 hour noise, +5 minute noise
 In [4]: range(2015, '2015-01-15', hours=3, minutes=(0, 5))
 Out[4]:
 [datetime.datetime(2015, 1, 1, 3, 1),
  datetime.datetime(2015, 1, 2, 0, 3),
  datetime.datetime(2015, 1, 3, 2, 0),
  datetime.datetime(2015, 1, 3, 22, 2),
  datetime.datetime(2015, 1, 4, 22, 3),
  datetime.datetime(2015, 1, 6, 0, 2),
  datetime.datetime(2015, 1, 7, 0, 4),
  datetime.datetime(2015, 1, 8, 0, 4),
  datetime.datetime(2015, 1, 8, 21, 3),
  datetime.datetime(2015, 1, 9, 22, 0),
  datetime.datetime(2015, 1, 11, 0, 0),
  datetime.datetime(2015, 1, 11, 22, 1),
  datetime.datetime(2015, 1, 12, 22, 5),
  datetime.datetime(2015, 1, 14, 3, 0),
  datetime.datetime(2015, 1, 15, 2, 5)]

 # it is able to specify minus direction as interval.
 In [5]: range(start='2015-5-22', end='2015-04-22', interval=timedelta(days=-1))
 Out[5]:
 [datetime.datetime(2015, 5, 22, 0, 0),
  datetime.datetime(2015, 5, 21, 0, 0),
  datetime.datetime(2015, 5, 20, 0, 0),
  datetime.datetime(2015, 5, 19, 0, 0),
  datetime.datetime(2015, 5, 18, 0, 0),
  datetime.datetime(2015, 5, 17, 0, 0),
  datetime.datetime(2015, 5, 16, 0, 0),
  datetime.datetime(2015, 5, 15, 0, 0),
  datetime.datetime(2015, 5, 14, 0, 0),
  datetime.datetime(2015, 5, 13, 0, 0),
  datetime.datetime(2015, 5, 12, 0, 0),
  datetime.datetime(2015, 5, 11, 0, 0),
  datetime.datetime(2015, 5, 10, 0, 0),
  datetime.datetime(2015, 5, 9, 0, 0),
  datetime.datetime(2015, 5, 8, 0, 0),
  datetime.datetime(2015, 5, 7, 0, 0),
  datetime.datetime(2015, 5, 6, 0, 0),
  datetime.datetime(2015, 5, 5, 0, 0),
  datetime.datetime(2015, 5, 4, 0, 0),
  datetime.datetime(2015, 5, 3, 0, 0),
  datetime.datetime(2015, 5, 2, 0, 0),
  datetime.datetime(2015, 5, 1, 0, 0),
  datetime.datetime(2015, 4, 30, 0, 0),
  datetime.datetime(2015, 4, 29, 0, 0),
  datetime.datetime(2015, 4, 28, 0, 0),
  datetime.datetime(2015, 4, 27, 0, 0),
  datetime.datetime(2015, 4, 26, 0, 0),
  datetime.datetime(2015, 4, 25, 0, 0),
  datetime.datetime(2015, 4, 24, 0, 0),
  datetime.datetime(2015, 4, 23, 0, 0),
  datetime.datetime(2015, 4, 22, 0, 0)]

common
~~~~~~

**noise**

It is possible to specify the gap between the actual time as noise parameters.
allow to specify the noise parameters are “datetimes.generator” and “datetimes.range” functions.

`**noise` is specified in the kwargs format and they are not required.

The available keys are same with timedelta-args.

- days
- hours
- minute
- seconds
- microseconds

**argtype**

The acceptable arguments as the other than datetime type are the following.

:int: It is evaluated as a `year`.
:str: It is parsed as `datetime` from the numeric part of the string.
:tuple: It will be passed into `datetime` args.
:dict: It will be passed into `datetime` kwargs.
:date: It will be converted `datetime` type.

history
-------

1.0.x
~~~~~
Initialize.
