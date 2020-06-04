# coding: utf-8


class Special(object):
    """something special variable."""

    def __init__(self, name):
        self.__name = name

    def __repr__(self):
        return "${0}".format(self.__name)


# BLANK const
BLANK = Special("BLANK")

# ESCAPE const
ESCAPE = Special("ESCAPE")
