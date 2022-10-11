from os import path

from gedcom import printer, validator
from gedcom.parser import Parser

from gedcom import Tests

INPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "input.gedcom")
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

        print("INDIVIDUALS")
        print(individuals_table)
        print("FAMILIES")
        print(family_table)
        print("MARRIAGE BEFORE DEATH")
        print(marriage_before_death)
        print("DIVORCE BEFORE DEATH")
        print(divorce_before_death)
        print("VALIDATIONS")
        print(validations)

        outfile.write("INDIVIDUALS\n")
        outfile.write(individuals_table)
        outfile.write("\nFAMILIES\n")
        outfile.write(family_table)
        outfile.write("\nMARRIAGE BEFORE DEATH\n")
        outfile.write(marriage_before_death)
        outfile.write("\nDIVORCE BEFORE DEATH\n")
        outfile.write(divorce_before_death)
        outfile.write("\nVALIDATIONS\n")
        outfile.write(validations)
        outfile.write("\n")

    Run_Tests(parser)


def Run_Tests(hParser):
    Tests.US03.Execute(hParser);
    Tests.US04.Execute(hParser);
    Tests.US05.Execute(hParser);
    Tests.US06.Execute(hParser);

if __name__ == "__main__":
    main()
