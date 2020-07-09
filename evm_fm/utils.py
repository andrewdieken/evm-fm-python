import argparse
import getpass
import os
import re


def update_environment_variable_file(s3_environment_variable_mappings, file_path):
    """Util method to either update to set local environment variables for a given env file

    Takes a dictionary, mapping environment variable names to values, and...

    Inputs:
        - s3_environment_variable_mappings (Dict): Mappings of environment variable names to values
    """
    REGEX_SEARCH_STRING = r'{}=.*\n'
    REPLACE_STRING = '{}="{}"\n'

    # Read file
    with open(file_path, 'r') as file:
        file_string = file.read()

    # Iterate over s3 params and either update value in file or append
    # the param to the end of the file
    for key, value in s3_environment_variable_mappings.items():
        search_object = re.search(str(key), file_string)
        formatted_replace_string = REPLACE_STRING.format(key, value)

        # param exists in file
        if search_object:
            formatted_regex_string = REGEX_SEARCH_STRING.format(key)
            file_string = re.sub(formatted_regex_string, formatted_replace_string, file_string)

        # param doesn't exist in file, add it to end of file
        else:
            formatted_replace_string = 'export {}'.format(formatted_replace_string)
            file_string += formatted_replace_string

    # Write file
    with open(file_path, 'w') as file:
        file.write(file_string)


def parse_args(cli_args):
    """Parse CLI args

    Inputs:
        - cli_args (List): List of command line arguments
    """
    parser = argparse.ArgumentParser(description='Parse CLI arguments.')
    parser.add_argument(
        '-f', '--config-file', dest='config_file', help='Location of configuration file', required=True
    )

    parsed_args = parser.parse_args(cli_args)

    return parsed_args


def get_users_home_directory():
    """Return the users home directory path
    """
    return os.path.expanduser('~')


def get_launch_agent_file_name():
    """Return the name of the LaunchAgent file
    """
    file_name = 'com.{user_name}.evm.fm.plist'
    user_name = getpass.getuser()
    return file_name.format(user_name=user_name)
