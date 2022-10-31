import random
from datetime import datetime, timedelta
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import pytest
from os import path
from gedcom.Tests import US09
from gedcom.parser import Parser


def get_parser(filename):
        INPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), filename)

        parser = None

        with open(INPUT_FILE_PATH) as infile:
                parser = Parser(infile)
                parser.parse()
        return parser






class TestUS09:
    #TODO
    def test_alive_younger(self):
        toParse = get_parser("us09test1.gedcom")
        errors = US09.ExecuteTests(toParse)
        assert len(errors) == 1
    def test_alive_mom(self):
        toParse = get_parser("us09test1.gedcom")
        errors = US09.ExecuteTests(toParse)
        assert len(errors) == 1
