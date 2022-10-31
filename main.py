from os import path

from gedcom import printer, validator
from gedcom.parser import Parser

from gedcom import Tests

INPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "input3.gedcom")
OUTPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "results.txt")


def main():
    with open(INPUT_FILE_PATH) as infile:
        parser = Parser(infile)
        parser.parse()

    with open(OUTPUT_FILE_PATH, "w") as outfile:
        validations = "\n".join(validator.validate(parser.individuals, parser.families))

        marriage_before_death = Tests.gedcom.Tests.US05.Execute(parser)

        divorce_before_death = Tests.gedcom.Tests.US06.Execute(parser)

        individuals_table = printer.print_individuals(parser.individuals.values())
        family_table = printer.print_families(
            parser.families.values(), parser.individuals
        )

        LT_150 = Tests.gedcom.Tests.US07.Execute(parser)

        BIR_BF_MARR_AF_DIV = Tests.gedcom.Tests.US08.Execute(parser)
        # US09 - Can't be born after parents death
        US09 = Tests.gedcom.Tests.US09.Execute(parser)

        # US10 - No marrying before 14 for husb or wife
        US10 = Tests.gedcom.Tests.US10.Execute(parser)

        # US11 - No bigamy
        NO_BIGAMY = Tests.gedcom.Tests.US11.Execute(parser)

        # US12 - Parents not too old
        PARENTS_NOT_TOO_OLD = Tests.gedcom.Tests.US12.Execute(parser)

        # US13 - SIBLINGS SPACING
        US13 = Tests.gedcom.Tests.US13.Execute(parser);


        # US14 - MULTIPLE BIRTHS <= 5
        US14 = Tests.gedcom.Tests.US14.Execute(parser);

        # US15 - More than 15 siblings
        TOO_MANY_SIBLINGS = Tests.gedcom.Tests.US15.Execute(parser)

        # US16 - More than 15 siblings
        MALE_FAMILY_MEMBERS_DIFFERENT_LAST_NAME = Tests.gedcom.Tests.US16.Execute(
            parser
        )


        #US21 - Correct Gender for Role
        US21 = Tests.gedcom.Tests.US21.Execute(parser)

        print("INDIVIDUALS")
        print(individuals_table)
        print("FAMILIES")
        print(family_table)
        print("VALIDATIONS")
        print(validations)
        print("MARRIAGE BEFORE DEATH")
        print(marriage_before_death)
        print("DIVORCE BEFORE DEATH")
        print(divorce_before_death)

        print("LESS THAN 150 YEARS OLD")
        print(LT_150)

        print("Born before marriage or after divorce")
        print(BIR_BF_MARR_AF_DIV)

        print("Born after parents death")
        print(US09)

        print("No marrying before 14")
        print(US10)


        print("US13: Siblings Spacing")
        print(US13)

        print("US14: Multiple births <= 5")
        print(US14)

        print("US21: Correct gender for role")
        print(US21)

        outfile.write("INDIVIDUALS\n")
        outfile.write(individuals_table)
        outfile.write("\nFAMILIES\n")
        outfile.write(family_table)

        outfile.write("\nVALIDATIONS\n")
        outfile.write(validations)
        outfile.write("\n")
        outfile.write("\nMARRIAGE BEFORE DEATH\n")
        outfile.write(marriage_before_death)
        outfile.write("\nDIVORCE BEFORE DEATH\n")
        outfile.write(divorce_before_death)

        outfile.write("\nLESS THAN 150 YEARS OLD\n")
        outfile.write(LT_150)

        outfile.write("\nBorn before marriage or after divorce\n")
        outfile.write(BIR_BF_MARR_AF_DIV)

        outfile.write("\nBorn after death of parent(s)\n")
        outfile.write(US09)

        outfile.write("\nMarried before either spouse is 14\n")
        outfile.write(US10)

        outfile.write("\nNO BIGAMY\n")
        outfile.write(NO_BIGAMY)

        outfile.write("\nPARENTS NOT TOO OLD\n")
        outfile.write(PARENTS_NOT_TOO_OLD)

        outfile.write("\nPARENTS NOT TOO OLD\n")
        outfile.write(PARENTS_NOT_TOO_OLD)

        outfile.write("\nUS13: SIBLINGS SPACING\n")
        outfile.write(US13)

        outfile.write("\nUS14: Multiple Births > 5\n")
        outfile.write(US14)

        outfile.write("\nTOO MANY SIBLINGS\n")
        outfile.write(TOO_MANY_SIBLINGS)

        outfile.write("\nMALE FAMILY MEMBER DIFFERENT LAST NAMES\n")
        outfile.write(MALE_FAMILY_MEMBERS_DIFFERENT_LAST_NAME)

        outfile.write("\nUS21: Correct Gender for Role\n")
        outfile.write(US21)

    Run_Tests(parser)


def Run_Tests(hParser):
    Tests.US03.Execute(hParser)
    Tests.US04.Execute(hParser)
    Tests.US05.Execute(hParser)
    Tests.US06.Execute(hParser)
    Tests.US07.Execute(hParser)
    Tests.US08.Execute(hParser)
    Tests.US09.Execute(hParser)
    Tests.US10.Execute(hParser)
    Tests.US11.Execute(hParser)
    Tests.US12.Execute(hParser)
    Tests.US13.Execute(hParser)
    Tests.US14.Execute(hParser)
    Tests.US15.Execute(hParser)
    Tests.US16.Execute(hParser)
    Tests.US21.Execute(hParser)


if __name__ == "__main__":
    main()
