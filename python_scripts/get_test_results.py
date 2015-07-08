#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from script_utils import utils
from script_utils import static_variables

def get_test_result(local_utils, phone_result_dir_path=None,
                    result_dir_path=None, device_model=None, device_id=None):
    '''get robotium test results from phone'''
    if phone_result_dir_path is None:
        phone_result_dir_path = '/sdcard/51TEST'
        
    if result_dir_path is None:
        file_path = os.path.abspath(__file__)
        file_dir = os.path.dirname(file_path)
        root_dir = os.path.dirname(file_dir)
        result_dir_path = os.path.join(root_dir, static_variables.RESULT_DIR_NAME, 
                                       static_variables.TEST_RESULT_DIR_NAME)
    if not os.path.exists(result_dir_path): 
        os.makedirs(result_dir_path)        
    
    if device_model is not None:
        device_model = device_model.replace(' ', '_')
        device_model_dir_path = os.path.join(result_dir_path, device_model)
    else:
        device_model_dir_path = result_dir_path
        
    if not os.path.exists(device_model_dir_path): 
        os.makedirs(device_model_dir_path)
        
    if device_id is not None:
        pull_str = '-s %s pull' % device_id
        rm_str = '-s %s shell rm -fr' % device_id
    else:
        pull_str = 'pull'
        rm_str = 'shell rm -fr' 
        
    pull_process = local_utils.run_adb('%s %s %s' % (pull_str, 
                                                     phone_result_dir_path, 
                                                     device_model_dir_path))
    (pull_process_stdout, pull_process_stderr) = pull_process.communicate();
    print pull_process_stdout
    print pull_process_stderr
    
    rm_process = local_utils.run_adb('%s %s' % (rm_str, phone_result_dir_path))
    (rm_process_stdout, rm_process_stderr) = rm_process.communicate()
    print rm_process_stdout
    print rm_process_stderr
        
    return result_dir_path

if __name__ == '__main__':
    try:
        local_utils = utils.Utils()
        local_utils.start_and_check()
        
#         result_path = get_test_result(local_utils)
#         print 'test results are now in %s\n' % result_path
        
        devices_list = local_utils.get_devices_list();
        print devices_list
        for each_device in devices_list:
            device_id = each_device.get('device_id')
            device_model = each_device.get('device_model')
            print 'device_model: %s; device_id: %s' % (device_model, device_id)
            print 'get test results from %s ...' % device_model
            result_path = get_test_result(local_utils=local_utils, 
                                          phone_result_dir_path=None, 
                                          result_dir_path=None, 
                                          device_model=device_model, 
                                          device_id=device_id)
            print 'test results are now in %s\n' % result_path

    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)
        
    finally:
        raw_input('press enter to exit ...\n')