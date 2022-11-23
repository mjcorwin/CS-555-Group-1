from os import path

import random
from datetime import datetime, timedelta

import pytest
from gedcom.parser import Parser
from gedcom import US26
from gedcom.family import Family
from gedcom.individual import Individual


@pytest.fixture
def individuals():
    INPUT_FILE_PATH = path.join(
        path.dirname(path.realpath(__file__)), "..", "input3.gedcom"
    );
    OUTPUT_FILE_PATH = path.join(
        path.dirname(path.realpath(__file__)), "..", "results.txt"
    );

    with open(INPUT_FILE_PATH) as infile:
        parser = Parser(infile);
        parser.parse();

    return parser.individuals;


@pytest.fixture
def families():
    INPUT_FILE_PATH = path.join(
        path.dirname(path.realpath(__file__)), "..", "input3.gedcom"
    );
    OUTPUT_FILE_PATH = path.join(
        path.dirname(path.realpath(__file__)), "..", "results.txt"
    );

    with open(INPUT_FILE_PATH) as infile:
        parser = Parser(infile);
        parser.parse();

    return parser.families;


# Corresponding entries
class TestUS26:
    def test_individual_family_records(self, individuals, families):
        errors = US26.US26_ex(individuals, families)
        assert len(errors) == 0
