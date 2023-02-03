''' This is the main file for our GHR-ing Machine! '''

from pathlib import Path
import os
import sys
import tomllib
import numpy as np
import pandas as pd

INPUT_DIRECTORY_PATH = r'./input_data/'
HOMEWORK_SUFFIX = "_HW_"
OUTPUT_DIRECTORY_PATH = r'./output_data/'
STUDENTS_FILE_NAME = "sample_students.toml"

''' Currently, this function will ask the user to enter a file name and will
    first check if the input is a valid path and also that it contains "_HW"
    since that is the constant above. If not found, it will call itself again
    until a valid path is entered then will return the full_input_fule'''


def check_valid_file():
    # get input
    current_dir = os.listdir(INPUT_DIRECTORY_PATH)
    input_file = input(f"Enter a file name with the following convention: {HOMEWORK_SUFFIX}\n")

    # look for a file with given suffix (forgive me string manipulation ancestors, for I am comitting sins)
    full_input_file = (str([
        path_string for path_string in current_dir if input_file in path_string])).replace('[\'', '').replace('\']', '')

    # set path and see if it actually exists
    path = Path(INPUT_DIRECTORY_PATH + full_input_file)
    if path.is_file() and HOMEWORK_SUFFIX in full_input_file:
        # if the file exists, we can pass it back to be opened
        print(f'\nFile {full_input_file} has been found.')
        user_validation = input("Is this the file that you want to grade? (y/n)  ")
        if user_validation.lower() == 'y':
            return full_input_file
        elif user_validation.lower() == 'n':
            print("\n\n")
            return check_valid_file()
        else:
            print("\nPlease input either y or n to validate the file\n")
            return check_valid_file()
    else:
        # if the file does not exist, we will recall the function until valid input is given
        print(
            'That file either does not exist, or does not follow the naming convention :(\nPlease try again...\n')
        return check_valid_file()


def validate_name(id_name_list):
    input_student_name = input("Enter student name to grade:\n")

    valid_id_name = ([
        name for name in id_name_list if input_student_name in name])

    if (not valid_id_name):
        print("Name not found, please try again")
        return validate_name(id_name_list)
    else:
        return str(valid_id_name[0][1])


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
    new_score = input(
        f"What was the score for question {input_question_grade[0]}? (Max value = {input_question_grade[1]})\n")

    new_comment = input("Comments?\n")

    # make new df for each line and append to final one
    next_line_df = pd.DataFrame({
        'Question': input_question_grade[0], 'Score': new_score, 'Max Score': input_question_grade[1], 'Comment': new_comment}, index=[0])

    return next_line_df

def sum_grades(input_edited_student_scores_df):

    #copy over the dataframe
    summed_scores_df = input_edited_student_scores_df

    try:

        #sum up the scores
        grade_sum = input_edited_student_scores_df['Score'].astype(float).sum()
        max_sum = input_edited_student_scores_df['Max Score'].sum()
        score_percent = float(grade_sum) / float(max_sum)

        #add calculations and name new column
        summed_scores_df = input_edited_student_scores_df
        sums_series = pd.Series(['Score Sum:', grade_sum, 'Max Score Sum:', max_sum, 'Final Percentage:', score_percent])
        summed_scores_df = pd.concat([summed_scores_df, sums_series], axis=1)
        summed_scores_df.columns = ['Question', 'Score', 'Max Score', 'Comment', 'Calculation']

    except:
        print("((Could not perform numerical calculations on inputted data, so the column is omitted))")

    return summed_scores_df

def add_comment_block(input_df):

    block = ""

    for comment in input_df['Comment']:
        if comment != "" and str(comment) != 'nan':
            block += str(comment) + '\n'

    blocked_df = input_df
    block_series = pd.Series([block])
    blocked_df = pd.concat([blocked_df, block_series], axis=1)
    blocked_df.columns = ['Question', 'Score', 'Max Score', 'Comment', 'Calculation', 'Copy/Paste Comment']

    return blocked_df

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


    #sum up the scores
    summed_student_scores_df = sum_grades(student_scores_df)

    # ask the user if they need to make changes, and
    # if the user wants to edit, it will also make all edits
    edited_student_scores_df = ask_for_edits(
        summed_student_scores_df, input_data_list)

    #Add all comments into one cell
    commented_and_summed_df = add_comment_block(edited_student_scores_df)

    return commented_and_summed_df  # return the copy with all edits, sums, comments


# MAIN ====================================================================================

# preliminary
print("\n\nThe GHR-ing Machine V1.0")
print(f"(Input the data in a 'questions{HOMEWORK_SUFFIX}x.toml' file, where x = the homework number)\n\n")


# ask for file name (runs validation before saving)
try:
    final_file_choice = check_valid_file()

    # Handle homework file and extract a list of questions (toml -> dict -> list)
    with open(f"{INPUT_DIRECTORY_PATH}{final_file_choice}", mode="rb") as fp:
        HW_config = tomllib.load(fp)
    data_list = list(HW_config['questions'].items())


# Handle student file and extract list of students
    with open(f"{INPUT_DIRECTORY_PATH}{STUDENTS_FILE_NAME}", mode="rb") as fp:
        STUDENT_config = tomllib.load(fp)
    id_name_list = list(STUDENT_config['id_name'].items())

    # ask for student name
    final_student_name = validate_name(id_name_list)

    print(f"now grading {final_student_name}...\n\n\n")
except Exception as e:
    print(f"\n\nCould not find a file named {STUDENTS_FILE_NAME} in directory {INPUT_DIRECTORY_PATH}.\nPlease check that the name in the config file matches your input.\n\n\n")
    sys.exit()



# main I/O grading function, saves as a Dataframe -> (Question, Score, Max Score)
final_grade_df = input_grades(data_list)



# Data Export
print("\n\n\nHere is the final output:\n")
print(final_grade_df)
final_grade_df.to_csv(
    f'{OUTPUT_DIRECTORY_PATH}{final_student_name}_{HW_config["title"]}_scores.csv', index=False)

