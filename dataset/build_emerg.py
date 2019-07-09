import pandas as pd
import os
import shutil
from collections import OrderedDict

EMERG_PATH = "corpus/"
EMERG_CSV = "final_target.csv"
EMERG_CORPUS_SRC = "EMERG_ORIGIN/"
EMERG_CORPUS_DST = "EMERG_TARGET/"

KEY_CATEGORY = "Category"
KEY_FILENAME = "Filename"

# The list of filename of EMERGENCY CORPUS
EMERG_DICT = dict()

for origin_filename in os.listdir(EMERG_PATH + EMERG_CORPUS_SRC):
    names = origin_filename.split('_')
    names.pop(2)

    new_filename = '_'.join(names)
    EMERG_DICT[new_filename.split(".TEXT")[0]] = origin_filename


# read csv file
try:
    RAW_DATA = pd.read_csv(EMERG_PATH + EMERG_CSV)
    print("Read csv file -", EMERG_PATH + EMERG_CSV, "\n")
except FileNotFoundError:
    print("FileNotFoundError]", EMERG_PATH + EMERG_CSV, "\n")
    exit(-1)
else:
    FILENAME_LIST = RAW_DATA[KEY_FILENAME]
    CATEGORY_LIST = RAW_DATA[KEY_CATEGORY]


def set_file_dict():
    """
    {
        filename: [start_index, end_index]
    }
    :return: file_dict
    """
    _file_dict = OrderedDict()

    for i, _filename in enumerate(FILENAME_LIST):
        if type(_filename) is str:
            _file_dict[_filename] = [i]

    pre_filename = str()
    last_index = len(FILENAME_LIST) - 1

    for i, _filename in enumerate(_file_dict):
        if i == 0:
            pre_filename = _filename
            continue

        end_index = _file_dict[_filename][0] - 1
        _file_dict[pre_filename].append(end_index)
        pre_filename = _filename

        if i == len(_file_dict) - 1:
            _file_dict[_filename].append(last_index)

    return _file_dict


def category_generator(_file_dict):
    for _filename, index_list in _file_dict.items():
        category_dict = dict()

        # set category_dict
        for i in range(index_list[0], index_list[1]):
            category = CATEGORY_LIST[i]

            if type(category) is str:
                if category not in category_dict:
                    category_dict[category] = None

        # yield filename which has a category
        # if len(category_dict) >= 1:
        if len(category_dict) == 1:
            yield _filename


def copy_conversation(_filename):
    if _filename in EMERG_DICT:
        src = EMERG_PATH + EMERG_CORPUS_SRC + EMERG_DICT[_filename]
        dst = EMERG_PATH + EMERG_CORPUS_DST + _filename + ".TEXT"
        shutil.copy(src, dst)
        return True
    else:
        return False


if __name__ == '__main__':
    file_dict = set_file_dict()
    num_target = int()
    num_except = int()

    # copy conversation which has a category
    for filename in category_generator(file_dict):
        if copy_conversation(filename):
            num_target += 1
        else:
            num_except += 1

    print("# of conversations in dir    -", len(EMERG_DICT))
    print("# of conversations in csv    -", len(file_dict))
    print("# of target conversation     -", num_target)
    print("# of not exist conversation  -", num_except, "\n\n")
