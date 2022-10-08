from os import path

from gedcom import printer
from gedcom.parser import Parser


INPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "gedcom_example.txt")
OUTPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "results.txt")


def main():
    parser = Parser(INPUT_FILE_PATH)
    parser.parse()

    with open("gedcom_results.txt", "w") as outfile:
        individuals_table = printer.print_individuals(parser.individuals.values())
        family_table = printer.print_families(
            parser.families.values(), parser.individuals
        )

        print(individuals_table)
        print(family_table)

        outfile.write("INDIVIDUALS\n")
        outfile.write(individuals_table)
        outfile.write("\nFAMILIES\n")
        outfile.write(family_table)


if __name__ == "__main__":
    main()
