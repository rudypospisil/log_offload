# Log Offloading from Production Servers to Backup Server
# RP_20200122
 
import pdb
import os
import shutil
import time
import pathlib
from configparser import ConfigParser
 
# Set variables from config file.
config = ConfigParser()
config.read(‘config.py')
 
s1 = config.get('paths', 's1')
s2 = config.get('paths', 's2')
path_iis_logs = config.get('paths', 'iis_logs')
path_server_logs = config.get('paths', 'server_logs')
path_pantone_logs = config.get('paths', 'pantone_logs')
path_local_log_dir = config.get('paths', 'local_log_dir')
 
server_list = [s1, s2]
log_folders_list = [path_iis_logs, path_server_logs, path_pantone_logs]
 
now = int(time.time())
one_week_buffer = 604800
 
for server in server_list:
    for log_folder in log_folders_list:
        for root, dirs, files in os.walk(server + log_folder):
            local_dir = path_local_log_dir + '\\' + server[2:14] + root.split(server)[1]
                for file_name in files:
                    file = os.path.join(root, file_name)
                    file_date = int(os.path.getctime(file))
                    # Target files more than one week old.
                    if now - file_date > one_week_buffer:
                        print(f'Moving {file_name} to {local_dir}\n')
                        try:
                            shutil.move(file, local_dir)
                        except shutil.Error as err:
                            print(err)