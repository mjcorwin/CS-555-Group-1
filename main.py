from os import path

from gedcom import printer, validator
from gedcom.parser import Parser

from gedcom import Tests;

INPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "input.gedcom")
OUTPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "results.txt")


def main():
    with open(INPUT_FILE_PATH) as infile:
        parser = Parser(infile)
        parser.parse()

    with open(OUTPUT_FILE_PATH, "w") as outfile:
        validations = "\n".join(validator.validate(parser.individuals, parser.families))

        individuals_table = printer.print_individuals(parser.individuals.values())
        family_table = printer.print_families(
            parser.families.values(), parser.individuals
        )

        print("INDIVIDUALS")
        print(individuals_table)
        print("FAMILIES")
        print(family_table)
        #print("VALIDATIONS")
        #print(validations)

        outfile.write("INDIVIDUALS\n")
        outfile.write(individuals_table)
        outfile.write("\nFAMILIES\n")
        outfile.write(family_table)
        #outfile.write("\nVALIDATIONS\n")
        #outfile.write(validations)
        #outfile.write("\n")

    Run_Tests(parser);

def Run_Tests(hParser):
    Tests.US03.Execute(hParser);
    Tests.US04.Execute(hParser);
    # Tests.US05.Execute(hParser);
    Tests.US06.Execute(hParser);

if __name__ == "__main__":
    main()
