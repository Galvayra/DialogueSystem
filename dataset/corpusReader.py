# -*- coding: utf-8 -*-
from .variables import *
from copy import deepcopy
from collections import OrderedDict
import json
import re
import sys
sys.path.append(CNUMA_PATH + PY_VER)

# Load CNU morpheme analyzer
from DialogueSystem.cnuma.py_ver.batch_mode import MAClient
mac = MAClient.create_from_args()


class CorpusReader:
    def __init__(self, is_test=False):
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
            
            .
            .
            .
                        
            "EMERG": {
            }
        }
        
        """
        self.corpus_dict = OrderedDict({
            name: OrderedDict({
                KEY_DIAL_ID: list()
            })
            for name in self.corpus_list
        })

        self.__is_test = is_test

    @property
    def corpus_list(self):
        return self.__corpus_list

    @staticmethod
    def __read_corpus(_path):
        with open(_path, 'r') as r_file:
            return r_file.readlines()

    @property
    def is_test(self):
        return self.__is_test

    def set_dictionary(self):
        if self.is_test:
            speech_test = self.__read_corpus(PATH_OF_CORPUS[SPEECH] + "test")
            parser = DialogueParser(corpus=speech_test, target=SPEECH)
            for dial_id, dialogue_dict in parser.dialogue_dict_generator():
                self.__copy_into_corpus_dict(dial_id, dialogue_dict, target=SPEECH)
                self.__print_progress(dial_id, parser.len_of_dialogue, prefix=SPEECH)
        else:
            etri_train = self.__read_corpus(PATH_OF_CORPUS[ETRI] + "train")
            etri_test = self.__read_corpus(PATH_OF_CORPUS[ETRI] + "test")
            speech_train = self.__read_corpus(PATH_OF_CORPUS[SPEECH] + "train")

            parser = DialogueParser(corpus=etri_train + etri_test, target=ETRI)
            for dial_id, dialogue_dict in parser.dialogue_dict_generator():
                self.__copy_into_corpus_dict(dial_id, dialogue_dict, target=ETRI)
                self.__print_progress(dial_id, parser.len_of_dialogue, prefix=ETRI)

            parser = DialogueParser(corpus=speech_train, target=SPEECH)
            for dial_id, dialogue_dict in parser.dialogue_dict_generator():
                self.__copy_into_corpus_dict(dial_id, dialogue_dict, target=SPEECH)
                self.__print_progress(dial_id, parser.len_of_dialogue, prefix=SPEECH)

    def __copy_into_corpus_dict(self, dial_id, dialogue_dict, target):
        if target == ETRI:
            key = ETRI
        elif target == CONV:
            key = CONV
        elif target == SPEECH:
            key = SPEECH
        else:
            key = EMERG

        self.corpus_dict[key][KEY_DIAL_ID].append(dial_id)
        self.corpus_dict[key][KEY_DIAL + '_' + str(dial_id)] = deepcopy(dialogue_dict)

    @staticmethod
    def __print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=50):
        format_str = "{0:." + str(decimals) + "f}"
        percent = format_str.format(100 * (iteration / float(total)))
        filled_length = int(round(bar_length * iteration / float(total)))
        bar = '#' * filled_length + '-' * (bar_length - filled_length)
        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix.ljust(7), bar, percent, '%', suffix)),
        if iteration == total:
            sys.stdout.write('\n')
        sys.stdout.flush()

    def dump(self):
        if self.is_test:
            path = SAVE_PATH + SAVE_TEST
        else:
            path = SAVE_PATH + SAVE_TRAIN

        with open(path, 'w') as outfile:
            json.dump(self.corpus_dict, outfile, indent=4)
            print " \nsuccess make dump file! - file name is" + path + "\n\n"


class DialogueParser:
    def __init__(self, corpus, target):
        self.__corpus_lines = corpus
        self.__target = target
        self.len_of_dialogue = self.__init_len_of_dialogue()

    @property
    def corpus_lines(self):
        return self.__corpus_lines

    @property
    def target(self):
        return self.__target

    def __init_len_of_dialogue(self):
        len_of_dialogue = int()

        for _, _ in self.__dialogue_generator():
            len_of_dialogue += 1

        return len_of_dialogue

    @staticmethod
    def __init_dialog_dict():
        dialogue_dict = OrderedDict({
            KEY_UTT_ID: list()
        })

        return dialogue_dict

    def __dialogue_generator(self):
        dial_id = 0

        if self.target == ETRI:
            start_index = 0

            for i, line in enumerate(self.corpus_lines):
                if line.startswith('<dial>'):
                    start_index = i

                if line.startswith('</dial>'):
                    end_index = i + 1
                    dial_id += 1

                    yield dial_id, self.corpus_lines[start_index:end_index]
        elif self.target == CONV or self.target == SPEECH:
            start_index = len('\n\n')

            for i, line in enumerate(self.corpus_lines):
                if i == 0:
                    continue

                if line.startswith('; '):
                    end_index = i - len('\n\n')
                    dial_id += 1

                    yield dial_id, self.corpus_lines[start_index:end_index]
                    start_index = i + len('\n\n')

            dial_id += 1
            yield dial_id, self.corpus_lines[start_index:]

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
        elif self.target == CONV or self.target == SPEECH:
            for i, line in enumerate(dialogue):
                if i == 0:
                    continue

                if line.startswith('\n'):
                    end_index = i
                    utt_id += 1

                    yield utt_id, dialogue[start_index:end_index]
                    start_index = end_index + 1

            utt_id += 1
            yield utt_id, dialogue[start_index:]

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
        for dial_id, dialogue in self.__dialogue_generator():
            dialogue_dict = self.__init_dialog_dict()

            for utt_id, utt in self.__utterance_generator(dialogue):
                spk, snt, sa = self.__get_slots(utt)

                # # line test
                # if spk and snt and sa:
                #     pass
                # else:
                #     print dial_id, utt_id

                dialogue_dict[KEY_UTT_ID].append(utt_id)
                key = KEY_UTT + '_' + str(utt_id)
                if USE_MA:
                    dialogue_dict[key] = {
                        KEY_SPK: spk,
                        KEY_SNT: snt,
                        KEY_MOR: mac.get_single_line(snt),
                        KEY_SA: sa
                    }
                else:
                    dialogue_dict[key] = {
                        KEY_SPK: spk,
                        KEY_SNT: snt,
                        KEY_SA: sa
                    }

            yield dial_id, dialogue_dict

    def __get_slots(self, utt):
        spk = str()
        snt = str()
        sa = str()

        if self.target == ETRI:
            utt = ' '.join(utt)

            spk = utt[utt.index('<spk> ') + len('<spk> '):utt.index(' </spk>')]
            snt = utt[utt.index('<snt> ') + len('<snt> '):utt.index(' </snt>')]
            sa = utt[utt.index('<sa> ') + len('<sa> '):utt.index(' </sa>')]

            if spk == "로봇":
                spk = 'agent'
            else:
                spk = 'user'
        elif self.target == CONV or self.target == SPEECH:
            for line in utt:
                if line.startswith('/SP/'):
                    spk = line[len('/SP/'):]
                    spk = spk.split()[0]

                if line.startswith('/KS/'):
                    snt = line[len('/KS/'):]
                    snt = snt.split()
                    snt = ' '.join(snt)
                    snt = re.sub('\([가-힣]+\) ', '', snt)

                if line.startswith('/SA/'):
                    sa = line[len('/SA/'):]
                    sa = sa.split()[0]

            if spk == "Agnt":
                spk = 'agent'
            else:
                spk = 'user'

        return spk, snt, sa
