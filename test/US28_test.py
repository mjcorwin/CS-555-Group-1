from gedcom.parser import Parser
from gedcom.Tests.US28 import *
import pytest

class TestUS28:
    def test_good_birth_order(self, individual, make_individual_with_birth_dates):
        parser = Parser(None)
        ex_birth_date = make_individual_with_birth_dates(["1980-01-07","1990-01-07", "2001-01-10"],[""])
        parser.individuals = {
            individual.birth: ex_birth_date
        }
        US28_Test(parser)
        assert len(US28_Problems) == 0
    def test_bad_birth_order(self, individual, make_individual_with_birth_dates):
        parser = Parser(None)
        ex_birth_date = make_individual_with_birth_dates(["2001-01-10", "1980-01-07", "2001-01-10"],[""])
        parser.individuals = {
            individual.birth: ex_birth_date
        }