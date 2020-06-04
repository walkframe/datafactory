# coding: utf-8
import os
import codecs

from ..exceptions import OutputFileAlreadyExists


class BaseFormatter(object):
    _container = []

    def _write(self, path, rewrite, method, **openoption):
        if os.path.exists(path):
            if not rewrite:
                raise OutputFileAlreadyExists()

        openoption.setdefault("encoding", "utf-8")
        openoption.setdefault("mode", "wb")

        with codecs.open(path, **openoption) as f:
            method(f)

    def stringify(self):
        raise NotImplementedError()

    def write(self, path, rewrite=False, **openoption):
        """container object write to file.

        :param str path: output file path.
        :param bool rewrite: rewrite if file path is already exists.
        :param kwargs openoption: io.open argments.
        :return: None
        """
        self._write(path, rewrite, (lambda f: f.write(self.stringify())), **openoption)
