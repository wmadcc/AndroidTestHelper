#!/usr/bin/env python
# -*- coding: utf-8 -*-

from script_utils import utils

if __name__ == '__main__':
    try:
        local_utils = utils.Utils()
        local_utils.kill_5037()
        
    except Exception, ex:
        print 'ERROR: %s' % str(ex)
        
    finally:
        raw_input('press enter to exit ...\n')