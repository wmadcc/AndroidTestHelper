#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import shutil

from script_utils import utils
from script_utils import static_variables

def resign_app_under_test(local_utils,
                          keystore_dir_path=None,
                          keystore_name='debug.keystore',
                          alias_name='androiddebugkey',
                          keystore_passwd='android',
                          key_passwd='android',
                          src_apk_dir=None,
                          src_apk_name='*.apk',
                          resigned_apk_dir=None,
                          resigned_apk_name=None):
    '''resign specific target apk'''
    sign_dir_name = 'META-INF'
    apk_dir_base_name = 'target'
    unsign_apk_base_name = 'target_unsign'
    unsign_apk_name = 'target_unsign.apk'
    resigned_temp_apk_name = 'target_resigned_temp.apk'

    file_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_path)
    root_dir = os.path.dirname(file_dir)
    if src_apk_dir is None:
        src_apk_dir = os.path.join(root_dir, static_variables.SRC_APK_DIR_NAME)
    if not os.path.exists(src_apk_dir):
        os.makedirs(src_apk_dir)

    src_apk_path = os.path.join(src_apk_dir, src_apk_name)
    src_apk_list = glob.glob(src_apk_path)
    print src_apk_list
    if len(src_apk_list) > 1:
        print 'search apk pattern is %s' % src_apk_path
        raise Exception, 'over 2 target apk exist!'
    elif len(src_apk_list) == 0:
        print 'search apk pattern is %s' % src_apk_path
        raise Exception, 'no target apk exist!'

    if resigned_apk_dir is None:
        resigned_apk_dir = os.path.join(root_dir, static_variables.RESIGNED_APK_DIR_NAME)
    if not os.path.exists(resigned_apk_dir):
        os.makedirs(resigned_apk_dir)

    target_apk_path = src_apk_list[0]
    if resigned_apk_name is None:
        resigned_apk_name = local_utils.get_file_name(target_apk_path) + '_resigned.apk '

    print 'rename apk to zip file ...'
    apk_zip_path =  target_apk_path + '.zip'
    os.rename(target_apk_path, apk_zip_path)

    print 'unzip apk zip to directory ...'
    apk_unzip_dir_path = os.path.join(src_apk_dir, apk_dir_base_name)
    local_utils.unzip_file(apk_zip_path, apk_unzip_dir_path)
    os.rename(apk_zip_path, target_apk_path)

    print 'delete signature directory ...'
    sign_dir_path = os.path.join(apk_unzip_dir_path, sign_dir_name)
    if os.path.exists(sign_dir_path):
        shutil.rmtree(sign_dir_path)

    print 'zip apk directory into zip file ...'
    unsign_apk_zip_path = os.path.join(src_apk_dir, unsign_apk_base_name + '.zip')
    local_utils.zip_dir(apk_unzip_dir_path, unsign_apk_zip_path)

    print 'rename zip file to apk ...'
    unsign_apk_path = os.path.join(src_apk_dir, unsign_apk_name)
    os.rename(unsign_apk_zip_path, unsign_apk_path)

    resigned_temp_apk_path = os.path.join(src_apk_dir, resigned_temp_apk_name)
    resigned_apk_path = os.path.join(resigned_apk_dir, resigned_apk_name)
    if keystore_dir_path == None:
        keystore_dir_path = os.path.join(os.environ['HOME'], '.android')
    keystore_path = os.path.join(keystore_dir_path, keystore_name)

    jarsigner_tool = os.path.join(local_utils.java_home, 'bin', 'jarsigner')
    local_utils.run_system('%s -verbose -keystore %s -storepass '
                           '%s -keypass %s -signedjar %s %s %s'
                           % (jarsigner_tool, keystore_path, keystore_passwd,
                              key_passwd, resigned_temp_apk_path, unsign_apk_path, alias_name))

    if local_utils.sys_is_windows:
        zipalign_search_path = os.path.join(local_utils.android_home,
                                             'build-tools', '*', 'zipalign.exe')
    else:
        zipalign_search_path = os.path.join(local_utils.android_home,
                                             'build-tools', '*', 'zipalign')
    zipalign_tool = glob.glob(zipalign_search_path)[-1]
    local_utils.run_system('%s 4 %s %s' % (zipalign_tool,
                                           resigned_temp_apk_path, resigned_apk_path))

    if os.path.exists(apk_unzip_dir_path):
        shutil.rmtree(apk_unzip_dir_path)
    if os.path.exists(unsign_apk_path):
        os.remove(unsign_apk_path)
    if os.path.exists(resigned_temp_apk_path):
        os.remove(resigned_temp_apk_path)

    return resigned_apk_path

if __name__ == '__main__':
    try:
        local_utils = utils.Utils()
        resiged_apk_path = resign_app_under_test(local_utils,
                                                 keystore_dir_path=None,
                                                 keystore_name='debug.keystore',
                                                 alias_name='androiddebugkey',
                                                 keystore_passwd='android',
                                                 key_passwd='android',
                                                 src_apk_dir=None,
                                                 src_apk_name='*.apk',
                                                 resigned_apk_dir=None,
                                                 resigned_apk_name=None)
        print 'refer resigned apk to %s\n' % resiged_apk_path

#         uninstall_process = local_utils.run_adb('uninstall com.zhangdan.app')
#         (uninstall_process_stdout, uninstall_process_stderr) = uninstall_process.communicate()
#         print uninstall_process_stdout
#         print uninstall_process_stderr
#
#         install_process = local_utils.run_adb('install %s' % resiged_apk_path)
#         (install_process_stdout, install_process_stderr) = install_process.communicate()
#         print install_process_stdout
#         print install_process_stderr

        devices_list = local_utils.get_devices_list()
        print devices_list
        for each_device in devices_list:
            device_id = each_device.get('device_id')
            uninstall_process = local_utils.run_adb('-s %s uninstall com.zhangdan.app' % device_id)
            (uninstall_process_stdout, uninstall_process_stderr) = uninstall_process.communicate()
            print uninstall_process_stdout
            print uninstall_process_stderr

            install_process = local_utils.run_adb('-s %s install %s'
                                                  % (device_id, resiged_apk_path))
            (install_process_stdout, install_process_stderr) = install_process.communicate()
            print install_process_stdout
            print install_process_stderr

    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)

    finally:
        raw_input('press enter to exit ...\n')