# -*- coding: utf-8 -*-
from .variables import *


class CorpusReader:
    def __init__(self):
        self.__corpus_list = [name for name in PATH_OF_CORPUS]

        """
        corpus_dict = {
            "ETRI": {
                "dial_id": list of dialogs          ex) [1, 2, ..., n]
                "dial_1": {
                    "utt_id": list of utterances    ex) [1, 2, ..., k]
                    "utt_1": {
                        "spk": 'agent' or 'user'
                        "snt": string of sentence
                        "mor": list of morphemes of sentence
                        "sa" : speech act of utterance
                        
                    }
                }
                
                .
                .
                .
                
                "dial_k" : {
                }
            }
            
            "CONV": {
            }
            
            .
            .
            .
                        
            "EMERG": {
            }
        }
        
        """
        self.corpus_dict = {name: dict() for name in PATH_OF_CORPUS}

    @property
    def corpus_list(self):
        return self.__corpus_list

    @staticmethod
    def __read_corpus(_path):
        with open(_path, 'r') as r_file:
            return r_file.readlines()

    def set_dictionary(self):
        etri_train = self.__read_corpus(PATH_OF_CORPUS[ETRI] + "train")
        etri_test = self.__read_corpus(PATH_OF_CORPUS[ETRI] + "test")

        parser = DialogueParser(target=ETRI)

        for dial_id, utt in parser.generator(etri_train + etri_test):
            print(dial_id, utt)


class DialogueParser:
    def __init__(self, target):
        self.__target = target

    @property
    def target(self):
        return self.__target

    @staticmethod
    def __init_dialog_dict():
        dialog_dict = {
            KEY_UTT_ID: list()
        }

        return dialog_dict

    def __dialogue_generator(self, lines):
        start_index = 0
        dial_id = 0

        if self.target == ETRI:
            for i, line in enumerate(lines):
                if line.startswith('<dial>'):
                    start_index = i

                if line.startswith('</dial>'):
                    end_index = i + 1
                    dial_id += 1

                    yield dial_id, lines[start_index:end_index]

    def __utterance_generator(self, dialogue):
        start_index = 0
        utt_id = 0

        if self.target == ETRI:
            for i, line in enumerate(dialogue):
                if line.startswith('<utt>'):
                    start_index = i

                if line.startswith('</utt>'):
                    end_index = i + 1
                    utt_id += 1

                    yield utt_id, dialogue[start_index:end_index]

    def generator(self, corpus):

        """
        "dial_1": {
            "utt_id": list of utterances    ex) [1, 2, ..., k]
            "utt_1": {
                "spk": 'agent' or 'user'
                "snt": string of sentence
                "mor": list of morphemes of sentence
                "sa" : speech act of utterance

            }

            .
            .
            .

            "utt_k": {
                "spk": 'agent' or 'user'
                "snt": string of sentence
                "mor": list of morphemes of sentence
                "sa" : speech act of utterance

            }
        }
        """

        if self.target == ETRI:
            for dial_id, dialogue in self.__dialogue_generator(corpus):
                dialogue_dict = self.__init_dialog_dict()
                
                for utt_id, utt in self.__utterance_generator(dialogue):
                    utt = ' '.join(utt)

                    spk = utt[utt.index('<spk> ') + len('<spk> '):utt.index(' </spk>')]
                    snt = utt[utt.index('<snt> ') + len('<snt> '):utt.index(' </snt>')]
                    sa = utt[utt.index('<sa> ') + len('<sa> '):utt.index(' </sa>')]
                    # mor = utt[utt.index('<mor>') + len('<mor>'):utt.index('</mor>')]

                    if spk == "로봇":
                        spk = 'agent'
                    else:
                        spk = 'user'

                    dialogue_dict[KEY_UTT_ID].append(utt_id)
                    key = KEY_UTT + '_' + str(utt_id)
                    dialogue_dict[key] = {
                        KEY_SPK: spk,
                        KEY_SNT: snt,
                        KEY_SA: sa
                    }

                yield dial_id, dialogue_dict
        else:
            pass
