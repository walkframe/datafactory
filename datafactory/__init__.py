# coding: utf-8

"""generate testdata.
"""

__author__ = "righ"
__author_email__ = "righ.m9@gmail.com"
__version__ = "1.0.0"
__license__ = "Apache License 2.0"

from .containers.dict import DictContainer
from .containers.list import ListContainer
from .containers.iter import IterContainer

from .models.list import ListModel
from .models.dict import DictModel

from .fields.choice import ChoiceField
from .fields.pickout import PickoutField
from .fields.cycle import CycleField
from .fields.hashof import HashOfField
from .fields.increment import IncrementField
from .fields.sequence import SequenceField

from .formatters.string import StringFormatter
from .formatters.json import JsonFormatter
from .formatters.pickle import PickleFormatter
from .formatters.csv import CsvFormatter

from .api.special import BLANK, ESCAPE

Model = DictModel
Container = ListContainer


CONTAINERS = {
    "list": ListContainer,
    "dict": DictContainer,
    "iter": IterContainer,
}

MODELS = {
    "list": ListModel,
    "dict": DictModel,
}

PATTERNS = {
    "choice": ChoiceField,
    "pickout": PickoutField,
    "cycle": CycleField,
    "hashof": HashOfField,
    "increment": IncrementField,
    "sequence": SequenceField,
}


FORMATTERS = {
    "string": StringFormatter,
    "json": JsonFormatter,
    "pickle": PickleFormatter,
    "csv": CsvFormatter,
}

IncField = IncrementField
SeqField = SequenceField

# Container is ListContainer
Container = ListContainer


try:
    del containers, models, fields, formatters, exceptions, api
except NameError:
    pass
