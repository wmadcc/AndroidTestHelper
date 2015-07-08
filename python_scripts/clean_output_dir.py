#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from script_utils import static_variables
import shutil

if __name__ == '__main__':
    try:
        del_chioce = raw_input('delete all of the default result directories? y to delete\n')
        if del_chioce == 'y':
            del_confirm = raw_input('confirm to delete? y to delete\n')
            if del_confirm == 'y':
                
                file_path = os.path.abspath(__file__)
                file_dir = os.path.dirname(file_path)
                root_dir = os.path.dirname(file_dir)
                
                del_dirs_list = [static_variables.RESIGNED_APK_DIR_NAME,
                                 static_variables.APKS_BACKUP_DIR_NAME,
                                 static_variables.RESULT_DIR_NAME,
                                 static_variables.TEMP_DIR_NAME]
                print '\n'
                for each_dir in del_dirs_list:
                    del_dir_path = os.path.join(root_dir, each_dir)
                    if os.path.exists(del_dir_path):
                        print 'deleting the directory %s ...\n' % del_dir_path
                        shutil.rmtree(del_dir_path)
                else:
                    print 'clean up output directories completed!\n'
                
    except Exception, ex:
        print 'ERROR: %s' % str(ex)
        
    finally:
        raw_input('press enter to exit ...')
