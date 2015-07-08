#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import sqlite3

from script_utils import static_variables
from script_utils import utils

def convert_database_to_py(local_utils, src_database_file=None, dest_py_dir=None):
    file_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_path)
    root_dir = os.path.dirname(file_dir)

    if src_database_file is None:
        src_database_dir = os.path.join(root_dir, static_variables.SRC_DATABASE_DIR_NAME)
        if not os.path.exists(src_database_dir):
            os.makedirs(src_database_dir)
            
        database_search_path = os.path.join(src_database_dir, '*.db3')
        src_database_file_list = glob.glob(database_search_path)
        
        if len(src_database_file_list) == 0:
            raise Exception, ('no database file in %s' % src_database_dir)
        else:
            src_database_file = src_database_file_list[0]
        
    if not os.path.exists(src_database_file):
        raise Exception, ('%s not exist' % src_database_file)
        
    if dest_py_dir is None:
        dest_py_dir = os.path.join(root_dir, static_variables.DATABASE_PY_DIR_NAME)   
    if not os.path.exists(dest_py_dir):
        os.makedirs(dest_py_dir)
    
    database_basename = os.path.basename(src_database_file)
    database_name = local_utils.get_file_name(database_basename)
    dest_py_file_name = '%s.py' % database_name
    dest_py_file = os.path.join(dest_py_dir, dest_py_file_name)
    
    print 'convert %s to %s ...\n' % (src_database_file, dest_py_file)
    
    conn = sqlite3.connect(src_database_file, check_same_thread=False)
    cursor = conn.cursor()
    conn.text_factory = str
    
    retrive_tables_sql = 'select * from sqlite_master where type="table"'
    cursor.execute(retrive_tables_sql)
    tables_list = cursor.fetchall()
    
    dest_file = open(dest_py_file, 'w')
    
    dest_file.write('#!/usr/bin/env python\n')
    dest_file.write('# -*- coding: utf-8 -*-\n\n')
    dest_file.write('DATABASE_FILE_NAME = "%s"\n\n' % database_basename)
    dest_file.write('TABLE_NAME = "table_name"\n')
    dest_file.write('CREATE_SQL = "create_sql"\n')
    dest_file.write('DATA_DETAIL = "data_detail"\n\n')
    dest_file.write('CONFIG_DATA = [')
    
    for each_table in tables_list:
        dest_file.write('\n{')
        table_name = each_table[2]
        dest_file.write('TABLE_NAME: "%s", \n' % table_name)
        create_sql = each_table[4]
        dest_file.write('CREATE_SQL: "%s", \n' % create_sql)
        dest_file.write('DATA_DETAIL: (\n')
        
        cursor.execute('select * from %s' % table_name)
        rows = cursor.fetchall()
        for row in rows:
            new_row = list(row)
            dest_file.write('(')
            for element in new_row:
                if element is None:
                    dest_file.write('"", ')
                elif isinstance(element, unicode):
                    dest_file.write('%s", ' % element.encode('gb2312'))
                elif isinstance(element, int):
                    dest_file.write('%s, ' % element)
                else:
                    dest_file.write('"%s", ' % element)
                    
            dest_file.write('),\n')
            
        dest_file.write(')},\n')
        
    dest_file.write('\n]')
    dest_file.close()
    cursor.close()
    
    return dest_py_file

if __name__ == '__main__':
    try:
        local_utils = utils.Utils()
        result_file = convert_database_to_py(local_utils=local_utils, 
                                             src_database_file=None, 
                                             dest_py_dir=None)
        print 'refer result file to %s\n'  % result_file
        
    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)
        
    finally:
        raw_input('press enter to exit ...\n')