from ssm_parameter_store import EC2ParameterStore
from utils import update_environment_variable_file, parse_args
from botocore.exceptions import NoCredentialsError
import sys
import toml

sys.tracebacklimit=0

def main():
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

    # Run post command if file was updated
    if file_updated:
        pass


if __name__ == '__main__':
    main()