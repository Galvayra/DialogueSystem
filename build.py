# -*- coding: utf-8 -*-

from DialogueSystem.dataset.corpusReader import CorpusReader

if __name__ == '__main__':
    corpus_reader = CorpusReader()
    corpus_reader.set_dictionary()
    corpus_reader.dump()
