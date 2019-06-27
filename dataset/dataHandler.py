# -*- coding: utf-8 -*-
import sys
from .variables import *
from DialogueSystem.dataset.corpusReader import CorpusReader

# if sys.argv[0].split('/')[-1] == "build.py":


class DataHandler(CorpusReader):
    def __init__(self):
        super().__init__()

    def set_dictionary(self):
        super().set_dictionary()

    def dump(self):
        super().dump()
