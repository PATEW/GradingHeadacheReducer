''' This is the main file for our GHR-ing Machine! '''

import tomllib
from pathlib import Path


def check_valid_file():
    file_choice = input("Enter a filename:\n")
    path = Path(file_choice)
    if path.is_file():
        print(f'The file {file_choice} exists!!')
    else:
        print(f'The {file_choice} does not exist :(\nPlease try again...')
        check_valid_file()


# preliminary
print("\n\nGHR-ing Machine V0.1")
print("(Input the data in a 'questions_HWx.toml' file, where x = the homework number)\n\n")


# ask file
check_valid_file()

val = input("Enter student name to grade:\n")
print(val)


with open("./input_data/tic_tac_toe.toml", mode="rb") as fp:
    config = tomllib.load(fp)

print(config["user"]["player_o"])

with open("./input_data/test_data_HW3.toml", mode="rb") as fp:
    config1 = tomllib.load(fp)

print(config1["questions"]["2_1_1"])
print(config["user"]["player_o"])  # both files can stay open
