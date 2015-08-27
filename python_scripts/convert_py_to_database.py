#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import glob
import sqlite3

from script_utils import utils
from script_utils import static_variables


def convert_py_to_database(local_utils, src_py_file=None, dest_database_dir=None):
    file_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_path)
    root_dir = os.path.dirname(file_dir)

    if src_py_file is None:
        src_py_dir = os.path.join(root_dir, static_variables.DATABASE_PY_DIR_NAME)
        if not os.path.exists(src_py_dir):
            os.makedirs(src_py_dir)

        py_search_path = os.path.join(src_py_dir, '*.py')
        src_py_file_list = glob.glob(py_search_path)

        if len(src_py_file_list) == 0:
            raise Exception('no py file in %s' % src_py_dir)
        else:
            src_py_file = src_py_file_list[0]

    if not os.path.exists(src_py_file):
        raise Exception('%s not exist' % src_py_file)

    if dest_database_dir is None:
        dest_database_dir = os.path.join(root_dir, static_variables.DEST_DATABASE_DIR_NAME)
    if not os.path.exists(dest_database_dir):
        os.makedirs(dest_database_dir)

    src_py_dir = os.path.dirname(src_py_file)
    src_py_file_name = local_utils.get_file_name(src_py_file)
    sys.path.append(src_py_dir)
    src_py = None
    import_src_py = 'import %s as src_py' % src_py_file_name
    exec(import_src_py)

    dest_database_name = src_py.DATABASE_FILE_NAME
    dest_databse_path = os.path.join(dest_database_dir, dest_database_name)
    if os.path.exists(dest_databse_path):
        os.remove(dest_databse_path)

    conn = sqlite3.connect(dest_databse_path, check_same_thread=False)
    cursor = conn.cursor()

    conn.text_factory = str

    config_data = src_py.CONFIG_DATA
    for each_table in config_data:
        table_name = each_table[src_py.TABLE_NAME]
        create_sql = each_table[src_py.CREATE_SQL]
        cursor.execute(create_sql)
        pattern = re.compile('%s\s*\(.*\)' % table_name)
        table_key_sql = re.search(pattern, create_sql).group()
        table_key_count = len(table_key_sql.split(','))

        data_detail = each_table[src_py.DATA_DETAIL]
        for data_tuple in data_detail:
            valuse_tuple_str = None
            if table_key_count > 1:
                valuse_tuple_str = '(%s?)' % ('?, ' * (table_key_count - 1))
            else:
                valuse_tuple_str = '(?)'
            cursor.execute('insert into %s values %s'
                           % (table_name, valuse_tuple_str), data_tuple)

    conn.commit()
    cursor.close()

    return dest_databse_path

if __name__ == '__main__':
    try:
        local_utils = utils.Utils()
        result_file = convert_py_to_database(local_utils=local_utils,
                                             src_py_file=None,
                                             dest_database_dir=None)
        print 'refer result file to %s\n' % result_file

    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)

    finally:
        raw_input('press enter to exit ...\n')
