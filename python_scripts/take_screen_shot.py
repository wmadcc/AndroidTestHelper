#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from script_utils import utils
from script_utils import static_variables

def take_screen_shot(local_utils, phone_result_dir_path=None, 
                     result_dir_path=None, device_model=None, device_id=None):
    '''take a screen shot from phone'''
    if phone_result_dir_path is None:
        phone_result_dir_path = '/sdcard'
    
    if result_dir_path is None:
        file_path = os.path.abspath(__file__)
        file_dir = os.path.dirname(file_path)
        root_dir = os.path.dirname(file_dir)
        result_dir_path = os.path.join(root_dir, static_variables.RESULT_DIR_NAME, 
                                       static_variables.SCREEN_SHOTS_DIR_NAME)
    if not os.path.exists(result_dir_path): 
        os.makedirs(result_dir_path)
        
    if device_model is not None:
        device_model = device_model.replace(' ', '_')
        device_model_dir_path = os.path.join(result_dir_path, device_model)
        screen_shot_path = os.path.join(device_model_dir_path, '%s_%s.png' \
                                        % (device_model, local_utils.timestamp()))
    else:
        device_model_dir_path = result_dir_path
        screen_shot_path = os.path.join(device_model_dir_path, '%s.png' % local_utils.timestamp())
        
    if not os.path.exists(device_model_dir_path): 
        os.makedirs(device_model_dir_path)
    
    if device_id is not None:
        screencap_str = '-s %s shell /system/bin/screencap' % device_id
        pull_str = '-s %s pull' %  device_id
        rm_str = '-s %s shell rm' %  device_id
    else:
        screencap_str = 'shell /system/bin/screencap'
        pull_str = 'pull'
        rm_str = 'shell rm'
        
    screen_shot_process = local_utils.run_adb('%s -p %s/tmp.png' 
                                              % (screencap_str, phone_result_dir_path))
    (screen_shot_process_stdout, screen_shot_process_stderr) = \
                                                screen_shot_process.communicate()
    print screen_shot_process_stdout
    print screen_shot_process_stderr
    
    pull_process = local_utils.run_adb('%s %s/tmp.png %s' 
                                       % (pull_str, phone_result_dir_path, screen_shot_path))
    (pull_process_stdout, pull_process_stderr) = pull_process.communicate()
    print pull_process_stdout
    print pull_process_stderr
    
    rm_process = local_utils.run_adb('%s %s/tmp.png' 
                                     % (rm_str, phone_result_dir_path))
    (rm_process_stdout, rm_process_stderr) = rm_process.communicate()
    print rm_process_stdout
    print rm_process_stderr
    
    return screen_shot_path

if __name__ == '__main__':
    try:
        local_utils = utils.Utils()
        local_utils.start_and_check()
        
#         result_path = take_screen_shot(local_utils)
#         print 'refer screen shot to %s\n' % result_path
        
        devices_list = local_utils.get_devices_list();
        print devices_list
        for each_device in devices_list:
            device_id = each_device.get('device_id')
            device_model = each_device.get('device_model')
            print 'device_model: %s; device_id: %s' % (device_model, device_id)
            print 'take a screen shot at %s ...' % device_model
            result_path = take_screen_shot(local_utils=local_utils, 
                                          phone_result_dir_path=None, 
                                          result_dir_path=None, 
                                          device_model=device_model, 
                                          device_id=device_id)
            print 'refer screen shot to %s\n' % result_path

    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)
        
    finally:
        raw_input('press enter to exit ...\n')