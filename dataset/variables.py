# -*- coding: utf-8 -*-

CORPUS = "dataset/corpus/"
ETRI = "ETRI"
CONV = "CONV"
SPEECH = "SPEECH"
EMERG = "EMERG"

PATH_OF_CORPUS = {
    ETRI: CORPUS + "1_ETRI/",
    # CONV: CORPUS + "2_CONV/",
    SPEECH: CORPUS + "3_SPEECH/",
    EMERG: CORPUS + "4_EMERG/"
}

KEY_DIAL_ID = "dial_id"
KEY_DIAL = "dial"
KEY_UTT_ID = "utt_id"
KEY_UTT = "utt"
KEY_SPK = "spk"
KEY_SNT = "snt"
KEY_MOR = "mor"
KEY_SA = "sa"

SAVE_PATH = "dictionary/"
SAVE_TRAIN = "dict_train"
SAVE_TEST = "dict_test"

COMMAND = "cnuma/stdio.sh"
USE_MA = False
