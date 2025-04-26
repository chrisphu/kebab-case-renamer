import argparse
import os
from pathlib import Path


def add_and_parse_args(parser):
    parser.add_argument(
        'directory_path',
        type=Path,
        help="Path of the directory hosting the files and directories to be renamed.")
    args = parser.parse_args()
    return args


def verify_path_is_a_directory(path):
    if not path.is_dir():
        raise Exception('Argument is not a directory path.')


def query_yes_no(question):
    answer = input("\n" + question + " [(y)es] [ENTER] ")
    try:
        answer = str(answer)
        # Can't be answer.lower() in "yes" because then "e", "es", and "s" would both be valid.
        if answer.lower() in ["yes", "ye", "y"]:
            return
        raise Exception("Answer must be 'yes'.")
    except ValueError:
        raise Exception("Answer must be a string.")


def snakecase_rename(path):
    current_name = os.path.basename(path)
    new_name = current_name.lower().replace(' ', '-').replace('_', '-')
    if new_name == current_name:
        return 0
    current_path = path.absolute()
    new_path = os.path.join(current_path.parent, new_name)
    os.rename(current_path, new_path)
    print("'" + str(current_path) + "' renamed to '" + str(new_path) + "'")
    return 1


def rename_children(path):
    rename_count = 0
    for path_child_i in path.iterdir():
        rename_count += snakecase_rename(path_child_i)
        # TODO: Add 'rename files only' and 'rename directories only' option.
        # if path_child_i.is_file():
        #     snakecase_rename(path_child_i)
        #     continue
    print("\nDone. " + str(rename_count) + " files/directories renamed in '" + str(path) + "'.")


def main():
    parser = argparse.ArgumentParser()
    args = add_and_parse_args(parser)
    directory_path = args.directory_path
    verify_path_is_a_directory(directory_path)
    query_yes_no("Are you sure you want to rename files and directories in the '"
                 + str(directory_path) + "' directory? THIS CANNOT BE UNDONE.")
    rename_children(directory_path)


if __name__ == '__main__':
    main()
