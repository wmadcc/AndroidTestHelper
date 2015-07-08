#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import string

from script_utils import utils
from script_utils import static_variables

def take_screen_record(local_utils, phone_result_dir_path=None, 
                       result_dir_path=None, device_model=None, device_id=None):
    '''take a screen record from phone'''
    if phone_result_dir_path is None:
        phone_result_dir_path = '/sdcard'
    
    if result_dir_path is None:
        file_path = os.path.abspath(__file__)
        file_dir = os.path.dirname(file_path)
        root_dir = os.path.dirname(file_dir)
        result_dir_path = os.path.join(root_dir, static_variables.RESULT_DIR_NAME, 
                                       static_variables.SCREEN_RECORDS_DIR_NAME)
    if not os.path.exists(result_dir_path): 
        os.makedirs(result_dir_path)
        
    if device_model is not None:
        device_model = device_model.replace(' ', '_')
        device_model_dir_path = os.path.join(result_dir_path, device_model)
        screen_record_path = os.path.join(device_model_dir_path, '%s_%s.mp4' \
                                          % (device_model, local_utils.timestamp()))
    else:
        device_model_dir_path = result_dir_path
        screen_record_path = os.path.join(device_model_dir_path, 
                                          '%s.mp4' % local_utils.timestamp())
        
    if not os.path.exists(device_model_dir_path): 
        os.makedirs(device_model_dir_path)
    
    if device_id is not None:
        screenrecord_str = '-s %s shell /system/bin/screenrecord' % device_id
        pull_str = '-s %s pull' % device_id
        rm_str = '-s %s shell rm' % device_id
    else:
        screenrecord_str = 'shell /system/bin/screenrecord'
        pull_str = 'pull'
        rm_str = 'shell rm'
        
    local_utils.run_adb('%s %s/video.mp4' % (screenrecord_str, phone_result_dir_path))
    input_key = raw_input('Please press the Enter key to stop recording:\n')
    if input_key == '':
        local_utils.run_adb('kill-server').communicate()
        time.sleep(1)
        local_utils.start_and_check()

    print 'get video file ...'
    pull_process = local_utils.run_adb('%s %s/video.mp4 %s' 
                                       % (pull_str, phone_result_dir_path, screen_record_path))
    (pull_process_stdout, pull_process_stderr) = pull_process.communicate()
    print pull_process_stdout
    print pull_process_stderr
    
    print 'delete temp video file in phone ...'
    rm_process = local_utils.run_adb('%s %s/video.mp4'
                                      % (rm_str, phone_result_dir_path))
    (rm_process_stdout, rm_process_stderr) = rm_process.communicate()
    print rm_process_stdout
    print rm_process_stderr
        
    return screen_record_path
        
if __name__ == '__main__':
    try:
        local_utils = utils.Utils()
        local_utils.start_and_check()
        
#         sdk = string.atoi(local_utils.run_adb_shell('getprop ro.build.version.sdk').stdout.read())
#         if sdk < 19:
#             print 'SDK version is %s, less than 19!' % sdk
#         else:
#             result_path = take_screen_record(local_utils)
#             print 'refer screen record to %s\n' % result_path
            
        devices_list = local_utils.get_devices_list()
        print devices_list
        for each_device in devices_list:
            device_id = each_device.get('device_id')
            device_model = each_device.get('device_model') 
            print 'device_model: %s; device_id: %s' % (device_model, device_id)
            sdk = string.atoi(local_utils.run_adb_shell('getprop ro.build.version.sdk').stdout.read())
            if sdk < 19:
                print 'SDK version is %s, less than 19!' % sdk
            else:
                print 'take a screen record at %s ...' % device_model
                result_path = take_screen_record(local_utils, 
                                                 phone_result_dir_path=None, 
                                                 result_dir_path=None, 
                                                 device_model=device_model, 
                                                 device_id=device_id)
                print 'refer screen record to %s\n' % result_path

    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)
        
    finally:
        raw_input('press enter to exit ...\n')