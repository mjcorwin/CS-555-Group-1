from gedcom.parser import Parser
from gedcom.Tests.US23 import *


class TestUS23:
    def test_two_individuals_same_name_different_birth_date(
        self, make_individual, random_name, today, future_date
    ):
        a = make_individual()
        a.birth_date = today
        a.name = random_name

        b = make_individual()
        b.birth_date = future_date
        b.name = random_name

        parser = Parser(None)
        parser.individuals = {a.id: a, b.id: b}

        US23_Test(parser)
        assert len(US23_Problems) == 0

    def test_two_individuals_different_name_same_birth_date(
        self, make_individual, make_random_name, today
    ):
        a = make_individual()
        a.birth_date = today
        a.name = make_random_name()

        b = make_individual()
        b.birth_date = today
        b.name = make_random_name()

        parser = Parser(None)
        parser.individuals = {a.id: a, b.id: b}

        US23_Test(parser)
        assert len(US23_Problems) == 0

    def test_two_individuals_same_name_same_birth_date(
        self, make_individual, random_name, today
    ):
        a = make_individual()
        a.birth_date = today
        a.name = random_name

        b = make_individual()
        b.birth_date = today
        b.name = random_name

        parser = Parser(None)
        parser.individuals = {a.id: a, b.id: b}

        US23_Test(parser)
        assert len(US23_Problems) == 1

    def test_three_individuals_same_name_same_birth_date(
        self, make_individual, random_name, today
    ):
        a = make_individual()
        a.birth_date = today
        a.name = random_name

        b = make_individual()
        b.birth_date = today
        b.name = random_name

        c = make_individual()
        c.birth_date = today
        c.name = random_name

        parser = Parser(None)
        parser.individuals = {a.id: a, b.id: b, c.id: c}

        US23_Test(parser)
        assert len(US23_Problems) == 1

    def test_two_sets_two_individuals_same_name_same_birth_date(
        self, make_individual, make_random_name, today, future_date
    ):

        a = make_individual()
        a.birth_date = today
        a.name = make_random_name()

        b = make_individual()
        b.birth_date = today
        b.name = a.name

        c = make_individual()
        c.birth_date = future_date
        c.name = make_random_name()

        d = make_individual()
        d.birth_date = future_date
        d.name = c.name

        parser = Parser(None)
        parser.individuals = {a.id: a, b.id: b, c.id: c, d.id: d}

        US23_Test(parser)
        assert len(US23_Problems) == 2
