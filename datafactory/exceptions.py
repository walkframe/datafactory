# coding: utf-8


class BaseException(Exception):
    pass


class OutputFileAlreadyExists(BaseException):
    message = "path already exists. Try: rewrite=True"


class ModelTypeInvalid(BaseException):
    message = "expected list-type or dict-type as object type."


class CsvFormatterFieldsTypeInvalid(BaseException):
    messages = "expected list-type as object type."
