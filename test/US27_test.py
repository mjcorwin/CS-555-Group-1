from gedcom.parser import Parser
from gedcom.Tests.US27 import *
import pytest

class TestUS27:
    def test_empty_birth_date(self, individual, make_individual_with_birth_dates):
        parser = Parser(None)
        ex_birth_date = make_individual_with_birth_dates([""], "")
        parser.individuals = {
            individual.birth: ex_birth_date
        }
        
        US27_Test(parser)
        assert len(US27_Problems) == 1
        


