#!/usr/bin/env python
# -*- coding: utf-8 -*-

from script_utils import utils

def batch_uninstall(local_utils, device_id=None, device_model=None):
    '''uninstall 3rd packages in android device'''
    if device_model is None:
        from_device_str = ' '
    else:
        from_device_str = ' from %s ' % device_model
    
    if device_id is not None:
        uninstall_str = '-s %s uninstall' % device_id
    else:
        uninstall_str = 'uninstall'
        
    packages_dict = local_utils.get_3rd_packages_dict(device_id=device_id, 
                                                      device_model=device_model)
    
    for package_name in packages_dict:
        print 'uninstall %s%s...' % (package_name, from_device_str)
        uninstall_process = local_utils.run_adb('%s %s' % (uninstall_str, package_name))
        (uninstall_process_stdout, uninstall_process_stderr) = uninstall_process.communicate()
        print uninstall_process_stdout
        print uninstall_process_stderr

if __name__ == '__main__':
    try:
        local_utils = utils.Utils()
        local_utils.start_and_check()
        
#         batch_uninstall(local_utils)
#         print 'batch uninstall 3rd packages completed!\n'
        
        devices_list = local_utils.get_devices_list()
        print devices_list
        for each_device in devices_list:
            device_id = each_device.get('device_id')
            device_model = each_device.get('device_model')
            print 'device_model: %s; device_id: %s ' % (device_model, device_id)
            print 'batch uninstall 3rd packages from %s ...' % device_model
            batch_uninstall(local_utils=local_utils, 
                            device_id=device_id, 
                            device_model=device_model)
            print 'batch uninstall 3rd packages from %s completed!\n' % device_model
    
    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)
        
    finally:
        raw_input('press enter to exit ...\n')