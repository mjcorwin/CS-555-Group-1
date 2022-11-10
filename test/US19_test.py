#'''
from os import path
from datetime import datetime, timedelta
import pytest
from gedcom.parser import Parser
from gedcom.Tests.US19 import *





class TestUS19:
    def test_individual_no_marr_cousins(self):
        INPUT_FILE_PATH = path.join(
            path.dirname(path.realpath(__file__)), "..", "input19.gedcom"
        )
        OUTPUT_FILE_PATH = path.join(
            path.dirname(path.realpath(__file__)), "..", "results19.txt"
        )

        with open(INPUT_FILE_PATH) as infile:
            parser = Parser(infile)
            parser.parse()
        

        errors = US19_Test(parser)
        assert len(errors) == 1
    def main():
        INPUT_FILE_PATH = path.join(
            path.dirname(path.realpath(__file__)), "..", "input19.gedcom"
        )
        OUTPUT_FILE_PATH = path.join(
            path.dirname(path.realpath(__file__)), "..", "results19.txt"
        )

        with open(INPUT_FILE_PATH) as infile:
            parser = Parser(infile)
            parser.parse()
        with open(OUTPUT_FILE_PATH) as outfile:
            print(Execute(parser))
            outfile.write


if __name__ == "__main__":
    main()

""" 
PLAYGROUND.py

from os import path

from gedcom import printer, validator
from gedcom.parser import Parser

from gedcom import Tests

INPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "input19.gedcom")
OUTPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "results.txt")


def main():
    with open(INPUT_FILE_PATH) as infile:
        parser = Parser(infile)
        parser.parse()

    with open(OUTPUT_FILE_PATH, "w") as outfile:

        us19 = Tests.gedcom.Tests.US19.Execute(parser);


if __name__ == "__main__":
    main()

"""