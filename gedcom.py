from os import path

INPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "gedcom_example.txt")
OUTPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "results.txt")

GEDCOM_TAG_LEVEL_DICT = {
    "INDI": 0,
    "NAME": 1,
    "SEX": 1,
    "BIRT": 1,
    "DEAT": 1,
    "FAMC": 1,
    "FAMS": 1,
    "FAM": 0,
    "MARR": 1,
    "HUSB": 1,
    "WIFE": 1,
    "CHIL": 1,
    "DIV": 1,
    "DATE": 2,
    "HEAD": 0,
    "TRLR": 0,
    "NOTE": 0,
}


def is_valid(level, tag):
    return tag in GEDCOM_TAG_LEVEL_DICT and GEDCOM_TAG_LEVEL_DICT[tag] == level


def main():
    output = []

    with open(INPUT_FILE_PATH) as infile:
        for line in infile:
            line = line.strip()

            output.append(f"--> {line}")

            tokens = line.split(" ", 2)
            level = int(tokens[0])
            tag = tokens[1]
            args = tokens[2] if len(tokens) == 3 else ""

            if level == 0 and args in ["INDI", "FAM"]:
                tag, args = args, tag

            valid = "Y" if is_valid(level, tag) else "N"

            output.append("<-- " + "|".join([str(level), tag, valid, args]))

    with open("gedcom_results.txt", "w") as outfile:
        outfile.write("\n".join(output))
        outfile.write("\n")


if __name__ == "__main__":
    main()
