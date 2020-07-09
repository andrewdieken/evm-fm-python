import os
import subprocess
import sys

import toml

import utils


def main():
    """Main method"""
    args = utils.parse_args(sys.argv[1:])

    # Parse config file
    config_file_loc = args.config_file
    with open(str(config_file_loc), 'r') as config_file:
        parsed_config_file = toml.loads(config_file.read())

    # Parse launchd template
    import ipdb; ipdb.set_trace()
    template_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates/evm_temp_launchd.plist')
    with open(template_file_path, 'r') as launchd_template:
        # ensure we are reading from beginning of file
        launchd_template.seek(0)
        parsed_launchd_template = launchd_template.read()

    # Format launchd template with user configurations
    formatted_launchd_file = parsed_launchd_template.format(launchd_python_path=parsed_config_file['launchd_python_path'],
                                                            config_file_loc=parsed_config_file['config_file_loc'],
                                                            launchd_std_out_log_loc=parsed_config_file['launchd_std_out_log_loc'],
                                                            launchd_std_err_log_loc=parsed_config_file['launchd_std_err_log_loc'],
                                                            launchd_start_interval=parsed_config_file['launchd_start_interval'],)

    # Create LaunchAgent
    home_dir = utils.get_users_home_directory()
    launch_agents_dir = 'Library/LaunchAgents'
    launch_agent_file_name = utils.get_launch_agent_file_name()
    launch_agent_file_path = os.path.join(home_dir, launch_agents_dir, launch_agent_file_name)
    import ipdb; ipdb.set_trace()
    with open(launch_agent_file_path, 'w') as launch_agent_file:
        launch_agent_file.write(formatted_launchd_file)

    # load LaunchAgent
    load_launch_agent_cmd = subprocess.Popen(['launchctl', 'load', launch_agent_file_path])
    load_launch_agent_cmd.wait()

    # Check status
    launch_agent_data = subprocess.check_output('launchctl list | grep {launch_agent_file_name}'.format(launch_agent_file_name=launch_agent_file_name), shell=True).decode()
    launch_agent_status = launch_agent_data.split('\t')[1]
    if status == 0:
        status_msg = 'LaunchAgent sucessfully loaded. You can view logs at {std_out_location}'.format(std_out_location=parsed_config_file['launchd_std_out_log_path'])
    else:
        status_msg = 'LaunchAgent failed to load. Check logs at {std_err_location}'.format(std_err_location=parsed_config_file['launchd_std_err_log_path'])

    return status_msg

if __name__ == '__main__':
    sys.exit(main())
