# -*- coding: utf-8 -*-

from DialogueSystem.dataset.corpusReader import CorpusReader


if __name__ == '__main__':
    # dump dictionary for training set
    corpus_reader = CorpusReader()
    corpus_reader.set_dictionary()
    corpus_reader.dump()

    # dump dictionary for test set
    corpus_reader = CorpusReader(is_test=True)
    corpus_reader.set_dictionary()
    corpus_reader.dump()
