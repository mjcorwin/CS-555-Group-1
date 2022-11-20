from gedcom.parser import Parser
from gedcom.Tests.US30 import *

class TestUS30:
    def test_empty_marriage(self, make_marriage_with_death):
        parser = Parser(None)

        make_marriage_with_death(None, None)
        
        US30_Test(parser)
        assert len(US30_Problems) == 0

    def test_single_marriage(self, make_marriage_with_death):
        parser = Parser(None)

        make_marriage_with_death(["2010-01-01"], "1965-01-01")

        US30_Test(parser)
        assert len(US30_Problems) == 0

    def test_second_marriage_without_death(self, make_marriage_with_death):
        parser = Parser(None)

        make_marriage_with_death(None, "1965-01-01")

        US30_Test(parser)
        assert len(US30_Problems) == 0
    