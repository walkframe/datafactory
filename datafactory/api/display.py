# coding: utf-8
import json


def ellipsis(s, limit):
    if limit is not None and len(s) > limit:
        limit -= 3
        s = s[: 0 if limit < 0 else limit] + "..."
    return s


def repr(obj, limit=None):
    try:
        try:
            repr_string = json.dumps(obj, ensure_ascii=False)
        except (UnicodeDecodeError, UnicodeEncodeError):
            repr_string = json.dumps(obj)
    except (TypeError, UnicodeDecodeError, UnicodeEncodeError):
        repr_string = str(obj)

    return ellipsis(repr_string, limit)
