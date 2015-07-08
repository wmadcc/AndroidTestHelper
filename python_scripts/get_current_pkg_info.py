#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import shutil

from script_utils import utils
from script_utils import static_variables

def get_aapt_tool(local_utils):
    if local_utils.sys_is_windows:
        aapt_search_path = os.path.join(local_utils.android_home, 'build-tools', '*', 'aapt.exe')
    else:
        aapt_search_path = os.path.join(local_utils.android_home, 'build-tools', '*', 'aapt')
    aapt_tool = glob.glob(aapt_search_path)[-1]  
    
    return aapt_tool

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
        
        aapt_tool = get_aapt_tool(local_utils)
        
        file_path = os.path.abspath(__file__)
        file_dir = os.path.dirname(file_path)
        root_dir = os.path.dirname(file_dir)
        
        result_dir_path = os.path.join(root_dir, static_variables.RESULT_DIR_NAME)
        if not os.path.exists(result_dir_path):
            os.makedirs(result_dir_path)
        result_file_path = os.path.join(result_dir_path, 
                                        static_variables.CURRENT_PKG_INFO)
        result_file = open(result_file_path, 'w')
        
        tmp_apk_dir_path = os.path.join(root_dir, static_variables.TEMP_DIR_NAME)
        if not os.path.exists(tmp_apk_dir_path):
            os.makedirs(tmp_apk_dir_path)
             
#         tmp_apk_path = os.path.join(tmp_apk_dir_path, 'tmp_%s.apk' % local_utils.timestamp())
#         get_match_apk(local_utils, target_path=tmp_apk_path)
#         aapt_process = local_utils.run_command('%s dump badging %s' % (aapt_tool, tmp_apk_path))
#         (aapt_result_out, aapt_result_err) = aapt_process.communicate()
#           
#         timestamp_str = local_utils.timestamp()
#         print timestamp_str
#         result_file.write('\n%s\n' % timestamp_str)
#           
#         print aapt_result_out
#         result_file.write('\n%s\n' % aapt_result_out)
#           
#         print aapt_result_err
#         result_file.write('\n%s\n' % aapt_result_err)
            
        devices_list = local_utils.get_devices_list()
        for each_device in devices_list:
            device_id = each_device.get('device_id')
            device_model = each_device.get('device_model')
                
            tmp_apk_path = os.path.join(tmp_apk_dir_path, 'tmp_%s.apk' % local_utils.timestamp())
            get_match_apk(local_utils=local_utils, package_name=None, 
                          target_path=tmp_apk_path, device_id=device_id, device_model=device_model)
            aapt_process = local_utils.run_command('%s dump badging %s' % (aapt_tool, tmp_apk_path))
            (aapt_result_out, aapt_result_err) = aapt_process.communicate()
                
            timestamp_str = '%s - %s' % (device_model, local_utils.timestamp())
            print timestamp_str
            result_file.write('\n%s\n' % timestamp_str)
                
            print aapt_result_out
            result_file.write('\n%s\n' % aapt_result_out)
                
            print aapt_result_err
            result_file.write('\n%s\n' % aapt_result_err)
             
        result_file.close()
        shutil.rmtree(tmp_apk_dir_path)
        print 'refer result to %s\n' % result_file_path
    
    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)
        
    finally:
        raw_input('press enter to exit ...\n')