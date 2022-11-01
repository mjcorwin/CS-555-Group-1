import random
from datetime import datetime, timedelta

import pytest
from family import Family
from individual import Individual
from os import path

from parser import Parser

import US07

def get_parser(filename):
        INPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), filename)

        parser = None

        with open(INPUT_FILE_PATH) as infile:
                parser = Parser(infile)
                parser.parse()
        return parser






class TestUS07:
    def test_alive_younger(self):
        toParse = get_parser("test1.gedcom")
        errors = US07.ExecuteTests(toParse)
        assert len(errors) == 1

    def test_dead_150(self):
        toParse = get_parser("test2.gedcom")
        errors = US07.ExecuteTests(toParse)
        assert len(errors) == 1

    def test_150_exactly(self):
        toParse = get_parser("test3.gedcom")
        errors = US07.ExecuteTests(toParse)
        assert len(errors) == 1

    def test_good_alive(self):
        toParse = get_parser("test4.gedcom")
        errors = US07.ExecuteTests(toParse)
        assert len(errors) == 0

    def test_good_dead(self):
        toParse = get_parser("test5.gedcom")
        errors = US07.ExecuteTests(toParse)
        assert len(errors) == 0