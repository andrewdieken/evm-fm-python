import shlex
import subprocess
import sys
from datetime import datetime

import toml
from ssm_parameter_store import EC2ParameterStore

from utils import parse_args, update_environment_variable_file

sys.tracebacklimit=0

def main():
    """Main method
    """
    args = parse_args(sys.argv[1:])

    # Parse config file
    config_file_loc = args.config_file
    with open(str(config_file_loc), 'r') as file:
        parsed_config_file = toml.loads(file.read())

    # Fetch AWS params
    ssm_store = EC2ParameterStore()
    param_store_parameters = ssm_store.get_parameters_by_path(path=parsed_config_file['param_store_prefix'])

    # Update env var file
    file_updated = update_environment_variable_file(s3_environment_variable_mappings=param_store_parameters, file_path=parsed_config_file['env_file_path'])

    # Run post commands if file was updated
    if file_updated:
        post_commands = parsed_config_file.get('post_commands', None)
        for command_args in post_commands:
            command = command_args.get('command', None)
            use_shell = command_args.get('shell', False)

            # The subprocess library handles the command argument differently whether the shell argument
            # is passed as True or not. TL;DR if the shell argument is True then the command argument
            # should be passed as a single String. See https://stackoverflow.com/a/15109975 for additional
            # reading.
            if not use_shell:
                command = shlex.split(command)
            try:
                completed_command = subprocess.run(command, shell=use_shell, check=True)
                print("{} - Command '{}' completed successfully with exit code {}".format(datetime.now(), command, completed_command.returncode))
            except subprocess.CalledProcessError as e:
                error_message = "{} - ERROR: {}".format(datetime.now(), str(e))
                raise Exception(error_message)


if __name__ == '__main__':
    main()
