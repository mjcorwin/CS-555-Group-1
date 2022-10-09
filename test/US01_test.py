import pytest
from os import path
from gedcom.parser import Parser
from gedcom import validator


# TODO: Make random individual with date less than, equal to, or greater than today
@pytest.fixture(scope="class", autouse=True)
def parser():
    infile = path.join(path.dirname(path.realpath(__file__)), "fixtures", "US01.gedcom")
    file = open(infile)
    parser = Parser(file)
    parser.parse()

    return parser


# TODO: Date equal to today
# TODO: Test without dates
class TestUS01:
    def test_birth_date_less_than_today(self, parser):
        errors = validator.US01({"I01": parser.individuals["I01"]}, {})
        assert len(errors) == 0

    def test_death_date_less_than_today(self, parser):
        errors = validator.US01({"I01": parser.individuals["I01"]}, {})
        assert len(errors) == 0

    def test_marriage_date_less_than_today(self, parser):
        errors = validator.US01({}, {"F01": parser.families["F01"]})
        assert len(errors) == 0

    def test_divorce_date_less_than_today(self, parser):
        errors = validator.US01({}, {"F01": parser.families["F01"]})
        assert len(errors) == 0

    def test_birth_date_greater_than_today(self, parser):
        errors = validator.US01({"I02": parser.individuals["I02"]}, {})
        assert len(errors) >= 1

    def test_death_date_greater_than_today(self, parser):
        errors = validator.US01({"I02": parser.individuals["I02"]}, {})
        assert len(errors) >= 1

    def test_marriage_date_greater_than_today(self, parser):
        errors = validator.US01({}, {"F02": parser.families["F02"]})
        assert len(errors) >= 1

    def test_divorce_date_greater_than_today(self, parser):
        errors = validator.US01({}, {"F02": parser.families["F02"]})
        assert len(errors) >= 1
