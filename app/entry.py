import os
from datetime import datetime
from .setting import root_path

class Entry:
    """
    Entry class.
    """
    def __init__(self, entry):
        self.name = self._to_unicode(entry.name)
        self.path = self._to_unicode(entry.path)
        self.is_dir = entry.is_dir()
        self.is_file = entry.is_file()
        self.mtime = datetime.fromtimestamp(entry.stat().st_mtime).ctime()
        self.type = 'D' if self.is_dir else 'F'
        self.relpath = os.path.relpath(self.path, root_path)
        self.size = self._get_size(entry)

    def _get_size(self, entry):
        size = entry.stat().st_size
        unit = 'B'
        if size < 1024:
            unit = 'B'
        elif size < 1048576:
            size = size/1024
            unit = 'K'
        elif size < 1073741824:
            size = size/1048576
            unit = 'M'
        elif size < 1099511627776:
            size = size/1073741824
            unit = 'G'

        return '{0:.2f} {1}'.format(size, unit)

    def _to_unicode(self, string):
        return string.decode()


class Scaner:
    """
    Scaner class using os.scandir.
    """
    def __init__(self, path):
        self.entries = [Entry(entry) for entry in os.scandir(path.encode())]
