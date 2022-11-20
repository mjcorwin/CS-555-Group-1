from gedcom.parser import Parser
from gedcom.Tests.US32 import *


class TestUS31:
    def test_no_families(self):
        parser = Parser(None)
        parser.individuals = {}
        parser.families = {}

        US32_Test(parser)
        assert len(MULTIPLE_BIRTHS) == 0

    def test_family_no_birth(self, family):
        parser = Parser(None)
        parser.individuals = {}
        parser.families = {family.id: family}

        US32_Test(parser)
        assert len(MULTIPLE_BIRTHS) == 0

    def test_family_one_birth(self, individual, family, today):
        individual.family_child = family.id
        individual.birth_date = today

        parser = Parser(None)
        parser.individuals = {individual.id: individual}
        parser.families = {family.id: family}

        US32_Test(parser)
        assert len(MULTIPLE_BIRTHS) == 0

    def test_two_families_one_birth_each(self, make_family, make_individual, today):
        f1 = make_family()
        f2 = make_family()

        i1 = make_individual()
        i1.birth_date = today
        i1.family_child = f1.id

        i2 = make_individual()
        i2.birth_date = today
        i2.family_child = f2.id

        parser = Parser(None)
        parser.individuals = {i1.id: i1, i2.id: i2}
        parser.families = {f1.id: f1, f2.id: f2}

        US32_Test(parser)
        assert len(MULTIPLE_BIRTHS) == 0

    def test_family_two_births_different_date(
        self, make_individual, family, today, future_date
    ):
        i1 = make_individual()
        i1.birth_date = future_date
        i1.family_child = family.id

        i2 = make_individual()
        i2.birth_date = today
        i2.family_child = family.id

        parser = Parser(None)
        parser.individuals = {i1.id: i1, i2.id: i2}
        parser.families = {family.id: family}

        US32_Test(parser)
        assert len(MULTIPLE_BIRTHS) == 0

    def test_family_two_births_same_date(self, make_individual, family, today):
        i1 = make_individual()
        i1.birth_date = today
        i1.family_child = family.id

        i2 = make_individual()
        i2.birth_date = today
        i2.family_child = family.id

        parser = Parser(None)
        parser.individuals = {i1.id: i1, i2.id: i2}
        parser.families = {family.id: family}

        US32_Test(parser)
        assert len(MULTIPLE_BIRTHS) == 1

    def test_family_three_births_two_same_date(
        self, make_individual, family, today, future_date
    ):
        i1 = make_individual()
        i1.birth_date = future_date
        i1.family_child = family.id

        i2 = make_individual()
        i2.birth_date = today
        i2.family_child = family.id

        i3 = make_individual()
        i3.birth_date = today
        i3.family_child = family.id

        parser = Parser(None)
        parser.individuals = {i1.id: i1, i2.id: i2, i3.id: i3}
        parser.families = {family.id: family}

        US32_Test(parser)
        assert len(MULTIPLE_BIRTHS) == 1
        assert len(MULTIPLE_BIRTHS[0]) == 2

    def test_two_families_each_two_births_same_date(
        self, make_individual, make_family, today
    ):
        f1 = make_family()
        f2 = make_family()

        i1 = make_individual()
        i1.birth_date = today
        i1.family_child = f1.id

        i2 = make_individual()
        i2.birth_date = today
        i2.family_child = f1.id

        i3 = make_individual()
        i3.birth_date = today
        i3.family_child = f2.id

        i4 = make_individual()
        i4.birth_date = today
        i4.family_child = f2.id

        parser = Parser(None)
        parser.individuals = {i1.id: i1, i2.id: i2, i3.id: i3, i4.id: i4}
        parser.families = {f1.id: f1, f2.id: f2}

        US32_Test(parser)
        assert len(MULTIPLE_BIRTHS) == 2
        assert len(MULTIPLE_BIRTHS[0]) == 2
        assert len(MULTIPLE_BIRTHS[1]) == 2
