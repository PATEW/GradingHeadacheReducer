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


def make_the_edit(row_to_edit, input_student_scores_df, input_data_list):
    edited_student_scores_df = input_student_scores_df  # make a copy regardless
    if row_to_edit != -1:
        # delete selected row
        edited_student_scores_df = edited_student_scores_df.drop(
            edited_student_scores_df.index[int(row_to_edit)])

        # enter in new line
        edited_line = make_new_line(input_data_list[int(row_to_edit)])

        edited_student_scores_df = pd.concat([edited_student_scores_df.iloc[: (int(row_to_edit))],
                                             edited_line, edited_student_scores_df.iloc[(int(row_to_edit)):]]).reset_index(drop=True)

        # ask them to edit again recursively
        edited_student_scores_df = ask_for_edits(
            edited_student_scores_df, input_data_list)
    return edited_student_scores_df


def ask_for_edits(student_scores_df, original_data_list_df):
    # show the user what they have so far
    print("\n\nHere are the current scores:\n")
    print(student_scores_df)

    # ask to make edits (or break if they dont)
    while True:
        user_confirmation = input(
            "\n\nEnter row number to edit, otherwise press Enter to save.\n")
        if user_confirmation == '':
            return student_scores_df
        elif user_confirmation.isdigit():
            if int(user_confirmation) in range(0, len(student_scores_df.index)):
                final_score_df = make_the_edit(user_confirmation,
                                               student_scores_df, original_data_list_df)
                return final_score_df
        print("\nNot a valid input, please try again...\n")


def make_new_line(input_question_grade):
    print(
        f"the input_question grade is {input_question_grade} and is type {type(input_question_grade)}")
    new_score = input(
        f"What was the score for question {input_question_grade[0]}? (Max value = {input_question_grade[1]})\n")
    new_comment = input("Comments?\n")

    # make new df for each line and append to final one
    next_line_df = pd.DataFrame({
        'Question': input_question_grade[0], 'Score': new_score, 'Max Score': input_question_grade[1], 'Comment': new_comment}, index=[0])

    return next_line_df


def input_grades(input_data_list):
    # create an empty df to hold all of the student's scores
    student_scores_df = pd.DataFrame(
        columns=['Question', 'Score', 'Max Score', 'Comment'])

    # iterate over each grade line in the list (originally from the file)
    # q_g[0] = question, q_g[1] = max grade
    for question_grade in input_data_list:
        # make a new line
        new_line_df = make_new_line(question_grade)
        # append it to the existing df
        student_scores_df = pd.concat(
            [student_scores_df, new_line_df], ignore_index=True, axis=0)

    # ask the user if they need to make changes

    # if the user wants to edit, it will also make all edits
    edited_student_scores_df = ask_for_edits(
        student_scores_df, input_data_list)

    return edited_student_scores_df  # return the copy with edits


# MAIN ====================================================================================

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
final_grade_df = input_grades(data_list)


# Data Export
print("\n\n\nHere is the final output:\n")
print(final_grade_df)

# -----------------------------------------------------------------------------------------

# Things to do:
# export as toml or csv? (WITH STUDENT NAME ATTACHED)
# validate student name
# validate number is within range

# ------------------------------------------------------------------------------------------
# test stuff

# with open("./input_data/tic_tac_toe.toml", mode="rb") as fp:
#     config = tomllib.load(fp)

# print(config["user"]["player_o"])

# with open("./input_data/test_data_HW3.toml", mode="rb") as fp:
#     config1 = tomllib.load(fp)

# print(config1["questions"]["2_1_1"])
# print(config["user"]["player_o"])  # both files can stay open
