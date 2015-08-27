#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from script_utils import utils
from script_utils import static_variables


def batch_install(local_utils, apks_to_install_dir_path=None,
                  device_id=None, device_model=None):
    if apks_to_install_dir_path is None:
        file_path = os.path.abspath(__file__)
        file_dir = os.path.dirname(file_path)
        root_dir = os.path.dirname(file_dir)
        apks_to_install_dir_path = os.path.join(root_dir,
                                                static_variables.APKS_TO_INSTALL_DIR_NAME)
        if not os.path.exists(apks_to_install_dir_path):
            os.makedirs(apks_to_install_dir_path)

    if device_id is None:
        install_str = 'install -r'
    else:
        install_str = '-s %s install -r' % device_id

    if device_model is None:
        into_device_str = ' '
    else:
        into_device_str = ' into %s ' % device_model

    apks_count = 0
    for dirpath, dirnames, filenames in os.walk(apks_to_install_dir_path):
        for file_name in filenames:
            if file_name.endswith('.apk'):
                print 'install %s%s...' % (file_name, into_device_str)
                apk_abs_path = os.path.join(apks_to_install_dir_path, dirpath, file_name)
                install_process = local_utils.run_adb('%s "%s"'
                                                      % (install_str, apk_abs_path))
                (install_process_stdout, install_process_stderr) = install_process.communicate()
                print install_process_stdout
                print install_process_stderr

                apks_count += 1

    if apks_count == 0:
        raise Exception('there is no apk in %s' % apks_to_install_dir_path)

if __name__ == '__main__':
    try:
        local_utils = utils.Utils()
        local_utils.start_and_check()

#         batch_install(local_utils)
#         print 'batch install apks completed!\n'

        devices_list = local_utils.get_devices_list()
        print devices_list
        for each_device in devices_list:
            device_id = each_device.get('device_id')
            device_model = each_device.get('device_model')
            batch_install(local_utils=local_utils,
                          apks_to_install_dir_path=None,
                          device_id=device_id,
                          device_model=device_model)
            print 'batch install apks into %s completed!\n' % device_model

    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)

    finally:
        raw_input('press enter to exit ...\n')
