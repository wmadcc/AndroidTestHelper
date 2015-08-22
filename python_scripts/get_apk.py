#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from script_utils import utils
from script_utils import static_variables

def get_match_apk(local_utils, package_name=None,
                  target_path=None, device_id=None, device_model=None):
    '''backup specific apk to target path'''
    if package_name is None:
        package_name = local_utils.get_current_package_name(device_id, device_model)

    if target_path is None:
        file_path = os.path.abspath(__file__)
        file_dir = os.path.dirname(file_path)
        root_dir = os.path.dirname(file_dir)
        result_dir_path = os.path.join(root_dir, static_variables.APKS_BACKUP_DIR_NAME)
        if device_model is None:
            target_path = os.path.join(result_dir_path, '%s_%s.apk'
                                       % (package_name, local_utils.timestamp()))
        else:
            target_path = os.path.join(result_dir_path, device_model, '%s_%s.apk'
                                       % (package_name, local_utils.timestamp()))

    if device_model is None:
        print 'get %s apk to %s' % (package_name, target_path)
    else:
        print 'get %s apk from %s to %s' % (package_name, device_model, target_path)

    packages_dict = local_utils.get_packages_dict(device_id=device_id, device_model=device_model)
    package_path_in_device = packages_dict.get(package_name)

    if package_path_in_device is None:
        print 'there is no package %s' % package_name
        return None
    else:
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        if device_id is None:
            pull_process = local_utils.run_adb('pull %s %s'
                                               % (package_path_in_device, target_path))
        else:
            pull_process = local_utils.run_adb('-s %s pull %s %s'
                                               % (device_id, package_path_in_device, target_path))
        (pull_process_stdout, pull_process_stderr) = pull_process.communicate()
        print pull_process_stdout
        print pull_process_stderr
        return target_path

if __name__ == '__main__':
    try:
        local_utils = utils.Utils()
        local_utils.start_and_check()

#         result_path = get_match_apk(local_utils)
#         print 'refer target apk to %s\n' % result_path

        devices_list = local_utils.get_devices_list();
        print devices_list
        for each_device in devices_list:
            device_id = each_device.get('device_id')
            device_model = each_device.get('device_model')
            print 'device_model: %s; device_id: %s' % (device_model, device_id)
            print 'get match apk from %s ...' % device_model
            result_path = get_match_apk(local_utils, device_id=device_id, device_model=device_model)
            print 'refer target apk to %s\n' % result_path

    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)

    finally:
        raw_input('press enter to exit ...\n')