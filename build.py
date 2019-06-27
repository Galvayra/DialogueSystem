# -*- coding: utf-8 -*-

import sys
from os import path

try:
    import DialogueSystem
except ImportError:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from DialogueSystem.dataset.dataHandler import DataHandler


if __name__ == '__main__':
    dataHandler = DataHandler()
    dataHandler.load_corpus()
