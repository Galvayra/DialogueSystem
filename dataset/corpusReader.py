# -*- coding: utf-8 -*-
from .variables import *
from copy import deepcopy
from collections import OrderedDict
import json
import subprocess


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
        self.corpus_dict = {
            name: OrderedDict({
                KEY_DIAL_ID: list()
            })
            for name in PATH_OF_CORPUS
        }

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

        parser = DialogueParser(corpus=(etri_test), target=ETRI)

        for dial_id, dialogue_dict in parser.dialogue_dict_generator():
            self.__copy_into_corpus_dict(dial_id, dialogue_dict)

    def __copy_into_corpus_dict(self, dial_id, dialogue_dict):
        key = KEY_DIAL + '_' + str(dial_id)
        self.corpus_dict[ETRI][KEY_DIAL_ID].append(dial_id)
        self.corpus_dict[ETRI][key] = deepcopy(dialogue_dict)

    def dump(self):
        with open(SAVE_PATH + SAVE_NAME, 'w') as outfile:
            json.dump(self.corpus_dict, outfile, indent=4)
            print "\n=========================================================\n\n"
            print "success make dump file! - file name is", SAVE_PATH + SAVE_NAME


class DialogueParser:
    def __init__(self, corpus, target):
        self.__corpus_lines = corpus
        self.__target = target
        print "The Target is -", self.target, "\n\n"

    @property
    def corpus_lines(self):
        return self.__corpus_lines

    @property
    def target(self):
        return self.__target

    @staticmethod
    def __init_dialog_dict():
        dialog_dict = OrderedDict({
            KEY_UTT_ID: list()
        })

        return dialog_dict

    def __dialogue_generator(self):
        start_index = 0
        dial_id = 0

        if self.target == ETRI:
            for i, line in enumerate(self.corpus_lines):
                if line.startswith('<dial>'):
                    start_index = i

                if line.startswith('</dial>'):
                    end_index = i + 1
                    dial_id += 1

                    yield dial_id, self.corpus_lines[start_index:end_index]

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

    def dialogue_dict_generator(self):

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
            for dial_id, dialogue in self.__dialogue_generator():
                dialogue_dict = self.__init_dialog_dict()



                for utt_id, utt in self.__utterance_generator(dialogue):
                    utt = ' '.join(utt)

                    spk = utt[utt.index('<spk> ') + len('<spk> '):utt.index(' </spk>')]
                    snt = utt[utt.index('<snt> ') + len('<snt> '):utt.index(' </snt>')]
                    sa = utt[utt.index('<sa> ') + len('<sa> '):utt.index(' </sa>')]

                    if spk == "로봇":
                        spk = 'agent'
                    else:
                        spk = 'user'

                    dialogue_dict[KEY_UTT_ID].append(utt_id)
                    key = KEY_UTT + '_' + str(utt_id)
                    dialogue_dict[key] = {
                        KEY_SPK: spk,
                        KEY_SNT: snt,
                        # KEY_MOR: self.__get_morpheme(snt),
                        KEY_SA: sa
                    }

                yield dial_id, dialogue_dict
        else:
            pass

    @staticmethod
    def __get_morpheme(snt):
        mor = list()
        cmd = COMMAND + ' ' + '_'.join(snt.split())
        ma_result = subprocess.check_output(cmd, shell=True)
        ma_result = ma_result.decode('utf-8')

        for word in ma_result.split():
            if word != "None":
                word = word.split('|')[1:]
                word = '/'.join(word)
                mor.append(word)

        return mor
