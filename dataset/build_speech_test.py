import re

READ_PATH = "corpus/3_SPEECH/test_origin"


def read_corpus():
    with open(READ_PATH, 'r') as r_file:
        return r_file.readlines()


if __name__ == '__main__':
    corpus_lines = read_corpus()

    for line in corpus_lines:
        line = line.strip()

        # dialogue name  or  crlf
        if line.startswith(';') or not line:
            print(line)
            continue
        # /SP/
        if line.startswith("Agnt") or line.startswith("User"):
            print("/SP/" + line)
        else:
            regex = re.compile('^[a-zA-Z]')

            # /SA/
            if regex.match(line):
                print("/SA/" + line)
            else:
                # /KS/
                if not line.startswith('['):
                    print("/KS/" + line)
                else:
                    try:
                        is_ds = int(line[1])
                    # /ST/
                    except ValueError:
                        print("/ST/" + line)
                    # /DS/
                    else:
                        print("/DS/" + line)
