import argparse
import getpass
import os
import re
import subprocess

import constants


def update_environment_variable_file(s3_environment_variable_mappings, file_path):
    """Util method to either update to set local environment variables for a given env file

    Takes a dictionary, mapping environment variable names to values, and...

    Inputs:
        - s3_environment_variable_mappings (Dict): Mappings of environment variable names to values
        - file_path (String): Environment variable file path

    Returns:
        - Boolean: Whether or not the environment variable file was updated
    """
    REGEX_SEARCH_STRING = r'{}=.*\n'
    REPLACE_STRING = '{}="{}"\n'

    # Read file
    with open(file_path, 'r') as file:
        file_string = file.read()

    # Iterate over s3 params and either update value in file or append
    # the param to the end of the file
    file_updated = False
    for s3_key, s3_value in s3_environment_variable_mappings.items():
        formatted_replace_string = REPLACE_STRING.format(s3_key, s3_value)

        # Check to see if the s3 param already exists in the env var file
        is_existing_env_var = re.search(str(s3_key), file_string)
        if is_existing_env_var:
            formatted_regex_string = REGEX_SEARCH_STRING.format(s3_key)
            existing_value = get_existing_value(key_value_regex_string=formatted_regex_string, string_to_search=file_string)

            # s3 param does *not* match value in env var file, update value with s3 param
            if existing_value != s3_value:
                file_updated = True
                file_string = re.sub(formatted_regex_string, formatted_replace_string, file_string)

        # Param doesn't exist in file, add it to end of file
        else:
            file_updated = True
            formatted_replace_string = 'export {}'.format(formatted_replace_string)
            file_string += formatted_replace_string

    # Write file
    with open(file_path, 'w') as file:
        file.write(file_string)

    # Return whether the file has been updated
    return file_updated


def get_existing_value(key_value_regex_string, string_to_search):
    """Helper method to get the value of an existing environment variable

    Inputs:
        - key_value_regex_string (String): A regex string consisting of the existing key to search for
        - string_to_search (String): String used to search for the key_value_regex_string in

    Returns:
        - The existing keys value
        - None if the existing key does not exist
    """
    existing_value = None
    search_object = re.search(key_value_regex_string, string_to_search)
    if search_object:
        existing_key_value_string = string_to_search[search_object.start():search_object.end()].rstrip()
        existing_value = existing_key_value_string.split('=')[1].strip('"')

    return existing_value


def parse_args(cli_args):
    """Parse CLI args

    Inputs:
        - cli_args (List): List of command line arguments

    Returns:
        - ArgumentParser instance with namespaced arguments
    """
    parser = argparse.ArgumentParser(description='Parse CLI arguments.')
    parser.add_argument(
        '-f', '--config-file', dest='config_file', help='Location of configuration file', required=True
    )
    parser.add_argument(
        '-l', '--load', dest='load', action='store_true', help='Whether the evm LaunchAgent should be loaded'
    )
    parser.add_argument(
        '-u', '--unload', dest='unload', action='store_true', help='Whether the evm LaunchAgent should be unloaded'
    )

    parsed_args = parser.parse_args(cli_args)

    return parsed_args


def create_launch_agent(configurations):
    """Helper method to create the LaunchAgent file

    Steps:
        1) Reads LaunchAgent template file
        2) Formats template file with user configurations
        3) Write formatted template file to LaunchAgent directory

    Inputs:
        - configurations (Dict): User configurations used to format LaunchAgent file
    """

    # Parse launchd template
    current_directory = get_current_working_directory()
    template_file_path = os.path.join(current_directory, 'templates/evm_temp_launchd.plist')
    with open(template_file_path, 'r') as launchd_template:
        # ensure we are reading from beginning of file
        launchd_template.seek(0)
        parsed_launchd_template = launchd_template.read()

    # Format launchd template with user configurations
    refresh_env_var_script_loc = os.path.join(current_directory, 'refresh_environment_variables.py')
    formatted_launchd_file = parsed_launchd_template.format(launchd_python_path=configurations.get('launchd_python_path', constants.DEFAULT_PYTHON_PATH),
                                                            refresh_env_var_script_loc=refresh_env_var_script_loc,
                                                            config_file_loc=configurations['config_file_loc'],
                                                            launchd_std_out_log_loc=configurations.get('launchd_std_out_log_loc', constants.DEFAULT_STD_OUT_LOG_LOC),
                                                            launchd_std_err_log_loc=configurations.get('launchd_std_err_log_loc', constants.DEFAULT_STSD_ERR_LOG_LOC),
                                                            launchd_start_interval=configurations.get('launchd_start_interval', constants.DEFAULT_START_INTERVAL),)

    # Create LaunchAgent
    launch_agent_file_path = get_launch_agent_file_path()
    with open(launch_agent_file_path, 'w') as launch_agent_file:
        launch_agent_file.write(formatted_launchd_file)

    print('LaunchAgent created at {}'.format(launch_agent_file_path))


def load_launch_agent():
    """Helper method to load the LaunchAgent
    """
    launch_agent_file_path = get_launch_agent_file_path()
    load_launch_agent_cmd = subprocess.Popen(['launchctl', 'load', launch_agent_file_path])
    load_launch_agent_cmd.wait()


def unload_launch_agent():
    """Helper method to unload the LaunchAgent
    """
    launch_agent_file_path = get_launch_agent_file_path()
    load_launch_agent_cmd = subprocess.Popen(['launchctl', 'unload', launch_agent_file_path])
    load_launch_agent_cmd.wait()


def get_launch_agent_status(configurations):
    """Helper method to get the status of the LaunchAgent

    Inputs:
        - configurations (Dict): User configurations used to format LaunchAgent file

    Returns:
        - String: Status of the LaunchAgent
    """
    launch_agent_file_name = get_launch_agent_file_name()
    output = subprocess.run('launchctl list | grep {launch_agent_file_name}'.format(launch_agent_file_name=launch_agent_file_name.strip('.plist')), shell=True, capture_output=True)

    # Grep considers no matches to be a failure and returns a status code of 1. When this happens the subprocess library
    # returns a failure due to the grep command returning a non-zero exit code. This is not the behavior we want. When the
    # grep command returns no matches it means that the LaunchAgent has *not* been loaded and we want to inform the user.
    if output.returncode == 1:
        status_msg = 'LaunchAgent is not loaded. You can view logs at {std_out_location}'.format(std_out_location=configurations['launchd_std_out_log_loc'])
    else:
        launch_agent_status = int(output.stdout.decode().split('\t')[1])
        if launch_agent_status == 0:
            status_msg = 'LaunchAgent successfully loaded. You can view logs at {std_out_location}'.format(std_out_location=configurations['launchd_std_out_log_loc'])
        else:
            status_msg = 'LaunchAgent failed to load. Check logs at {std_err_location}'.format(std_err_location=configurations['launchd_std_err_log_loc'])

    return status_msg


def get_launch_agent_file_path():
    """Helper method to get the LaunchAgent file path

    Returns:
        - String: File path to the LaunchAgent
    """
    home_dir = get_users_home_directory()
    launch_agents_dir = 'Library/LaunchAgents'
    launch_agent_file_name = get_launch_agent_file_name()
    launch_agent_file_path = os.path.join(home_dir, launch_agents_dir, launch_agent_file_name)

    return launch_agent_file_path


def get_users_home_directory():
    """Return the users home directory path

    Return:
        - String: File path to the users home directory
    """
    return os.path.expanduser('~')


def get_launch_agent_file_name():
    """Return the name of the LaunchAgent file

    Return:
        - String: Name of the LaunchAgent
    """
    file_name = 'com.{user_name}.envvarmanager.plist'
    user_name = getpass.getuser()

    return file_name.format(user_name=user_name)


def get_current_working_directory():
    """Return the current working directory

    Return:
        - String: File path of the current working directory
    """
    return os.path.abspath(os.path.dirname(__file__))


def verify_required_configurations(user_configurations):
    """Helper method to verify the user has all the required configurations

    Inputs:
        - user_configurations (Dict): Users configurations

    Raises:
        - Exception: Which required configuration(s) is missing
    """
    required_configurations = [
        'env_file_path', 'param_store_prefix', 'config_file_loc',
    ]

    for config in required_configurations:
        if not user_configurations.get(config, None):
            error_message = 'Required configuration missing: {}'.format(config)
            raise Exception(error_message)
