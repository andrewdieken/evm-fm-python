
# evm-fm-python
Environment variable manager for Mac, written in Python

*__NOTE__: This project is still in the alpha phase of development*

## Objectives
This project is a configuration management tool for Mac aimed at keeping a local environment variable file up-to-date with values stored in external secret/key management systems.

## Supported Secret/Key Management Systems
- AWS Parameter Store

## Overview
This project takes advantage of the launchd daemon on Mac operating systems to continually monitor external secret/key management systems to keep a local environment variable file up-to-date. This project allows users to create/load/unload a launchd LaunchAgent that accomplishes just that. All you need to do is provide a configuration file and specify an action and  `evm-fm-python` takes care of the rest.

## Basic Usage
Available actions:
1. Create
    This action creates the LaunchAgent
    ```bash
    $ evm-fm --config-file <path_to_configuration_file>
    ```
2. Load
This action creates, loads, and starts the LaunchAgent
    ```bash
    $ evm-fm --config-file <path_to_configuration_file> --load
    ```
3. Unload
This action unloads and stops the LaunchAgent
    ```bash
    $ evm-fm --config-file <path_to_configuration_file> --unload
    ```
### Arguments
| Command Line  | Metadata | Required | Description |
| ------------- | ------------- | ------------- | ------------- |
| -f, --config-file | file path | True | Location of configuration file |
| -l, --load | | False | Whether the LaunchAgent should be loaded |
| -u, --unload | | False | Whether the evm LaunchAgent should be unloaded |

### Configuration File
This file contains all necessary configurations for `evm-fm-python` to perform the available actions. The configuration file can be located anywhere that can be accessed by the `evm-fm-python` project.

*__NOTE__: The configuration file *needs* to be a `.toml` file. See [https://github.com/toml-lang/toml](https://github.com/toml-lang/toml) for additional information about this file type*

| Key | Value Type | Required |  Default | Children | Parent | Description |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| env_file_path | String | True | - | - | - | File path of the environment variable file you wish `evm-fm-python` to update |
| param_store_prefixes | List of Strings | True | - | - | - | Prefixes you want `evm-fm-python` to use when pulling secret/key values from the supported secret/key management systems |
| config_file_loc | String | True | - | - | - | Path of the configuration file |
| launchd_std_out_log_loc | String | False | /usr/local/bin/log/env_var_manager.log | - | - | Path of the stdout log file you want the LaunchAgent to write to |
| launchd_python_path | String | False | /usr/bin/python | - | - | Path of the Python executable you want the LaunchAgent to use |
| launchd_std_err_log_loc | String | False | /usr/local/bin/log/env_var_manager.log | - | - | Path of the stderr log file you want the LaunchAgent to write to |
| launchd_start_interval | Integer | False | 120 | - | - | Time interval you want the LaunchAgent to run on in Seconds |
| post_commands | List of Dictionaries | False | - | command, shell | - | List of commands you want to be executed after the local environment file has been updated |
| command | String | True | - | - | post_commands | The post command you wish to be executed |
| shell | String | True | - | - | post_commands | Whether you wish the post command to be executed in a shell environment |

#### Example Configuration File
```
env_file_path = "/Users/user/example/envs/.env"
param_store_prefixes = ["/Development/Test/", "/Production/Test/"]
launchd_python_path = "/Users/user/.virtualenvs/example/bin/python"
config_file_loc = '/Users/user/example/configuration_file.toml'
launchd_std_out_log_loc = "/Users/user/example/logs/env_var_manager.log"
launchd_std_err_log_loc = "/Users/user/example/logs/env_var_manager.log"
launchd_start_interval = 340

[[post_commands]]
command = "source /Users/user/example/envs/.env"
shell = true
```
