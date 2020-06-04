# coding: utf-8
from copy import copy

from ..containers.base import BaseContainer
from ..models.base import BaseModel
from ..fields.base import BaseField
from .. import compat


def _initcontainer(obj):
    copied = copy(obj)
    obj.clear()
    return copied


def apply(blueprint, args, args_suffix=[]):
    """Adjusts Rendering arguments.

    :param blueprint: field/model/container/function
    :param args: render arguments
    :param args_prefix: args_prefix
    :return: rendered record
    """
    # num arguments adjustment for custom function
    args = args + args_suffix  # warning: don't use +=
    if isinstance(blueprint, BaseField):
        return blueprint(*args)

    if isinstance(blueprint, BaseModel):
        return blueprint(args[1], args[0])

    if isinstance(blueprint, BaseContainer):
        return blueprint(callback=_initcontainer)

    if callable(blueprint):
        argcount = blueprint.__code__.co_argcount
        return blueprint(*args[:argcount])

    if hasattr(blueprint, "__iter__") and hasattr(blueprint, compat.nextmethod):
        return next(blueprint)

    return blueprint
