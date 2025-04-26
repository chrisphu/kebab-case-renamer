import argparse
import os
from pathlib import Path


rename_count = 0


def add_and_parse_args(parser):
    parser.add_argument(
        "directory_path",
        type=Path,
        help="Path of the directory hosting the files and directories to be renamed."
    )
    parser.add_argument(
        "-r",
        "--recur",
        action="store_true",
        help="If renaming should be recursive and affect all descendants instead of only direct children."
    )
    args = parser.parse_args()
    return args


def verify_path_is_a_directory(path):
    if not path.is_dir():
        raise Exception('Argument is not a directory path.')


def query_yes_no(question):
    answer = input("\n" + question + " [(y)es] [ENTER] ")
    try:
        answer = str(answer)
        # Can't be answer.lower() in "yes" because then "e", "es", and "s" would all be valid.
        if answer.lower() in ["yes", "ye", "y"]:
            return
        raise Exception("Answer must be 'yes'.")
    except ValueError:
        raise Exception("Answer must be a string.")


def snakecase_rename(path, depth):
    current_name = os.path.basename(path)
    new_name = current_name.lower().replace(' ', '-').replace('_', '-')
    if new_name == current_name:
        return 0
    current_path = path.absolute()
    new_path = os.path.join(current_path.parent, new_name)
    os.rename(current_path, new_path)
    print("Depth " + str(depth) + ": '" + str(current_path) + "' renamed to '" + str(new_path) + "'")
    return 1


def rename_children(recur, path, depth):
    # rename_count = 0
    global rename_count
    for path_child_i in path.iterdir():
        if recur and path_child_i.is_dir():
            rename_children(True, path_child_i, depth + 1)
        rename_count += snakecase_rename(path_child_i, depth)
        # TODO: Add 'rename files only' and 'rename directories only' option.
        # if path_child_i.is_file():
        #     snakecase_rename(path_child_i)
        #     continue
    if depth == 0:
        print("\nDone. " + str(rename_count) + " files/directories renamed.")


def main():
    parser = argparse.ArgumentParser()
    args = add_and_parse_args(parser)
    verify_path_is_a_directory(args.directory_path)
    query_yes_no("Are you sure you want to rename files and directories in the '"
                 + str(args.directory_path) + "' directory? THIS CANNOT BE UNDONE.")
    rename_children(args.recur, args.directory_path, 0)


if __name__ == '__main__':
    main()
