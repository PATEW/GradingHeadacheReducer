''' This is the main file for our GHR-ing Machine! '''

from pathlib import Path
import tomllib
import numpy as np
import pandas as pd

HOMEWORK_PREFIX = "_HW"

''' Currently, this function will ask the user to enter a file name and will
    first check if the input is a valid path and also that it contains "_HW"
    since that is the constant above. If not found, it will call itself again
    until a valid path is entered then will return the file_choice'''


def check_valid_file():
    file_choice = input("Enter a file name:\n")
    path = Path(file_choice)
    if path.is_file() and HOMEWORK_PREFIX in file_choice:
        print(f'The file {file_choice} exists!!')
        return file_choice
    else:
        print(
            f'The file "{file_choice}" either does not exist, or does not follow the naming convention :(\nPlease try again...\n')
        check_valid_file()


def input_grades(data_list, student_name):
    # create an empty df to hold all of the student's scores
    student_scores_df = pd.DataFrame(
        columns=['Question', 'Score', 'Max Score'])

    # iterate over each grade line in the list (originally from the file)
    for question_grade in data_list:  # q_g[0] = question, q_g[1] = max grade
        new_score = input(
            f"What was the score for question {question_grade[0]}? (Max value = {question_grade[1]})\n")

        # make new df for each line and append to final one
        new_line_df = pd.DataFrame({
            'Question': question_grade[0], 'Score': new_score, 'Max Score': question_grade[1]}, index=[0])
        student_scores_df = pd.concat(
            [student_scores_df, new_line_df], ignore_index=True, axis=0)

    return student_scores_df


# preliminary
print("\n\nThe GHR-ing Machine V0.1")
print("(Input the data in a 'questions_HWx.toml' file, where x = the homework number)\n\n")


# ask for file name (runs validation before saving)
final_file_choice = check_valid_file()

# Handle homework file and extract a list of questions (toml -> dict -> list)
with open("./input_data/test_data_HW3.toml", mode="rb") as fp:
    config = tomllib.load(fp)
data_list = list(config['questions'].items())

# ask for student name
student_name = input("Enter student name to grade:\n")
print(f"now grading {student_name}...\n\n\n")


# main I/O grading function, saves as a Dataframe -> (Question, Score, Max Score)
final_grade_df = input_grades(data_list, student_name)


# Data Export
print(final_grade_df)

# ---------------------------------------------------------------------------------------------------
# test stuff

# with open("./input_data/tic_tac_toe.toml", mode="rb") as fp:
#     config = tomllib.load(fp)

# print(config["user"]["player_o"])

# with open("./input_data/test_data_HW3.toml", mode="rb") as fp:
#     config1 = tomllib.load(fp)

# print(config1["questions"]["2_1_1"])
# print(config["user"]["player_o"])  # both files can stay open
