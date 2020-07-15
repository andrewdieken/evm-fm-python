import os
import sys

import toml

import utils


def main():
    """Main method
    """
    args = utils.parse_args(sys.argv[1:])

    # Parse config file
    config_file_loc = args.config_file
    with open(str(config_file_loc), 'r') as config_file:
        parsed_config_file = toml.loads(config_file.read())

    utils.verify_required_configurations(parsed_config_file)

    # Only create LaunchAgent if unload arg is *not* passed
    if not args.unload:
        utils.create_launch_agent(parsed_config_file)

    if args.load:
        utils.load_launch_agent()
    elif args.unload:
        utils.unload_launch_agent()

    print(utils.get_launch_agent_status(parsed_config_file))

if __name__ == '__main__':
    sys.exit(main())
