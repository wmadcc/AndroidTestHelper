#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from script_utils import utils
from script_utils import static_variables


def get_log_burying_points(local_utils, phone_points_file_path=None, display_line_number=10,
                           result_dir_path=None, device_model=None, device_id=None, display_only=True):
    '''take a screen shot from phone'''

    if phone_points_file_path is None:
        phone_points_file_path = '/sdcard/Android/data/com.zhangdan.app/files/log/log.txt'

    if result_dir_path is None:
        file_path = os.path.abspath(__file__)
        file_dir = os.path.dirname(file_path)
        root_dir = os.path.dirname(file_dir)
        result_dir_path = os.path.join(root_dir, static_variables.RESULT_DIR_NAME,
                                       static_variables.BURNING_POINTS)

    if not os.path.exists(result_dir_path):
        os.makedirs(result_dir_path)

    if device_model is not None:
        device_model = device_model.replace(' ', '_')
        device_model_dir_path = os.path.join(result_dir_path, device_model)
        burying_points_path = os.path.join(device_model_dir_path, '%s_%s.txt'
                                        % (device_model, local_utils.timestamp()))
    else:
        device_model_dir_path = result_dir_path
        burying_points_path = os.path.join(device_model_dir_path, '%s.txt' % local_utils.timestamp())

    if not os.path.exists(device_model_dir_path):
        os.makedirs(device_model_dir_path)

    if device_id is not None:
        tail_str = '-s %s shell tail -n %s' % (device_id, display_line_number)
        pull_str = '-s %s pull' % device_id
        rm_str = '-s %s shell rm' % device_id
    else:
        tail_str = 'shell tail -n %s' % display_line_number
        pull_str = 'pull'
        rm_str = 'shell rm'

    display_points_process = local_utils.run_adb('%s %s'
                                              % (tail_str, phone_points_file_path))
    (screen_shot_process_stdout, screen_shot_process_stderr) = display_points_process.communicate()
    print screen_shot_process_stdout
    print screen_shot_process_stderr

    if not display_only:
        pull_process = local_utils.run_adb('%s %s %s'
                                           % (pull_str, phone_points_file_path, burying_points_path))
        (pull_process_stdout, pull_process_stderr) = pull_process.communicate()
        print pull_process_stdout
        print pull_process_stderr

    if display_only:
        return None
    else:
        return burying_points_path

if __name__ == '__main__':
    try:
        local_utils = utils.Utils()
        local_utils.start_and_check()

        #         result_path = get_log_burying_points(local_utils)
        #         print 'refer burying points to %s\n' % result_path

        devices_list = local_utils.get_devices_list()
        print devices_list

        command = None
        while True:
            command = raw_input('input command(p:pull log, q:quit, other:print log only):\n')

            if command == 'q':
                break

            if command == 'p':
                display_only = False
            else:
                display_only = True

            for each_device in devices_list:
                device_id = each_device.get('device_id')
                device_model = each_device.get('device_model')
                print 'device_model: %s; device_id: %s' % (device_model, device_id)
                print 'get log burying points at %s ...' % device_model
                result_path = get_log_burying_points(local_utils=local_utils,
                                                     phone_points_file_path=None,
                                                     display_line_number=10,
                                                     result_dir_path=None,
                                                     device_model=device_model,
                                                     device_id=device_id,
                                                     display_only=display_only)
                print 'refer burying points to %s\n' % result_path

    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)

    finally:
        raw_input('press enter to exit ...\n')
