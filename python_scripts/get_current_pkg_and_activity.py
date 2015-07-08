#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from script_utils import utils
from script_utils import static_variables

if __name__ == '__main__':
    try:
        local_utils = utils.Utils()
        local_utils.start_and_check()
    
        file_path = os.path.abspath(__file__)
        file_dir = os.path.dirname(file_path)
        root_dir = os.path.dirname(file_dir)
        result_dir_path = os.path.join(root_dir, static_variables.RESULT_DIR_NAME)
        if not os.path.exists(result_dir_path):
            os.makedirs(result_dir_path)
        result_file_path = os.path.join(result_dir_path, 
                                        static_variables.CURRENT_PKG_AND_ACT_FILE_NAME)
        result_file = open(result_file_path, 'w')
        
#         result_dict = local_utils.get_focused_package_and_activity()
#         pkg_name = result_dict.get('package')
#         cur_act = result_dict.get('activity')
#          
#         timestamp_str = local_utils.timestamp()
#         print timestamp_str
#         result_file.write('\n%s\n' % timestamp_str)
#          
#         pkg_name_str = 'Package: %s' % pkg_name
#         print pkg_name_str
#         result_file.write('\n%s\n' % pkg_name_str)
#          
#         act_str = 'Activity: %s' % cur_act
#         print act_str
#         result_file.write('\n%s\n' % act_str)
        
        devices_list = local_utils.get_devices_list()
        print devices_list
        for each_device in devices_list:
            device_id = each_device.get('device_id')
            device_model = each_device.get('device_model')
               
            result_dict = local_utils.get_focused_package_and_activity(device_id=device_id,
                                                                       device_model=device_model)
            pkg_name = result_dict.get('package')
            cur_act = result_dict.get('activity')
               
            timestamp_str = '%s - %s' % (device_model, local_utils.timestamp())
            print timestamp_str
            result_file.write('\n%s\n' % timestamp_str)
               
            pkg_name_str = 'Package: %s' % pkg_name
            print pkg_name_str
            result_file.write('\n%s\n' % pkg_name_str)
               
            act_str = 'Activity: %s' % cur_act
            print act_str
            result_file.write('\n%s\n' % act_str)
        
        result_file.close()
        print 'refer result to %s\n' % result_file_path

    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)
        
    finally:
        raw_input('press enter to exit ...\n')
    