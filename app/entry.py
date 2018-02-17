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
        self.type = 'Directory' if self.is_dir else 'File'
        self.relpath = os.path.relpath(self.path, root_path)
        self.size = str(entry.stat().st_size)

    def _to_unicode(self, string):
        return string.decode()


class Scaner:
    """
    Scaner class using os.scandir.
    """
    def __init__(self, path):
        self.entries = [Entry(entry) for entry in os.scandir(path.encode())]
