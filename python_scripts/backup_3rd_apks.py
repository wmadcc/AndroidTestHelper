#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from script_utils import utils
from script_utils import static_variables

def backup_3rd_apks_to(local_utils, backup_dir_path=None,
                     device_id=None, device_model=None):
    apks_dict = local_utils.get_3rd_packages_dict(device_id, device_model) 
    if len(apks_dict) == 0:
        raise Exception, 'there is no 3rd apk!'
    
    if backup_dir_path is None:
        file_path = os.path.abspath(__file__)
        file_dir = os.path.dirname(file_path)
        root_dir = os.path.dirname(file_dir)
        backup_root_dir_path = os.path.join(root_dir, static_variables.APKS_BACKUP_DIR_NAME)
        if device_model is None:
            backup_dir_path = os.path.join(backup_root_dir_path, '%s' % local_utils.timestamp())
        else:
            backup_dir_path = os.path.join(backup_root_dir_path, '%s_%s' 
                                           % (device_model, local_utils.timestamp()))
    if not os.path.exists(backup_dir_path):
        os.makedirs(backup_dir_path)
    
    if device_id is None:
        pull_str = 'pull'
    else:
        pull_str = '-s %s pull' % device_id
     
    for pkg_name, pkg_path in apks_dict.iteritems():
        pkg_backup_path = os.path.join(backup_dir_path, '%s.apk' % pkg_name)
        pull_process = local_utils.run_adb('%s %s %s' % (pull_str, pkg_path, pkg_backup_path))
        (pull_process_stdout, pull_process_stderr) = pull_process.communicate()
        print pull_process_stdout
        print pull_process_stderr
        
    return backup_dir_path

if __name__ == '__main__':
    try:
        local_utils = utils.Utils()
        local_utils.start_and_check()
        
#         result_path = back_3rd_apks_to(local_utils)
#         print 'refer apks to dir %s\n' % result_path
        
        devices_list = local_utils.get_devices_list()
        for each_device in devices_list:
            device_id = each_device.get('device_id')
            device_model = each_device.get('device_model')
            print 'backup apks for %s ...' % device_model
            result_path = backup_3rd_apks_to(local_utils=local_utils, backup_dir_path=None, 
                                           device_id=device_id, device_model=device_model)
            print 'refer apks to dir %s for %s\n' % (result_path, device_model)
        
    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)
        
    finally:
        raw_input('press enter to exit ...\n')