#!/usr/bin/env python
# -*- coding: utf-8 -*-

#need to install pychartdir module，http://blog.csdn.net/gb112211/article/details/43272049

import os
import time
import string

from script_utils import utils
from script_utils import static_variables

def get_cpu_and_memory(local_utils, device_id=None, device_model=None, 
                       times=0, interval=1, pkg_name=None, strict_match=False):
    result_dict = {}
    
    if local_utils.sys_is_windows:
        find_util = 'findstr'
    else:
        find_util = 'grep'
    
    if pkg_name is None:
        pkg_name = local_utils.get_current_package_name(device_id=device_id, 
                                                        device_model=device_model)
    
    if device_id is None:
        top_str = 'shell top'
    else:
        top_str = '-s %s shell top' % device_id
    
    if times > 0:
        top_process = local_utils.run_adb('%s -n %s -d %s | %s %s'
                                          % (top_str, times, interval, find_util, pkg_name))
        print 'getting CPU and memory info ...\n'
    else:
        top_process = local_utils.run_adb('%s -d %s | %s %s'
                                          % (top_str, interval, find_util, pkg_name))
        input_key = raw_input('Please press the Enter key to stop recording:\n')
        if input_key == '':
            local_utils.run_adb('kill-server').communicate()
            time.sleep(1)
            local_utils.start_and_check()
    
    top_out = top_process.communicate()[0]
    
    file_path = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_path)
    root_dir = os.path.dirname(file_dir)
    result_dir_path = os.path.join(root_dir, static_variables.RESULT_DIR_NAME,
                                   static_variables.CPU_AND_MEMORY_DIR_NAME)
    if not os.path.exists(result_dir_path): 
        os.makedirs(result_dir_path)
        
    if device_model is not None:
        device_model = device_model.replace(' ', '_')
        device_model_dir_path = os.path.join(result_dir_path, device_model)
    else:
        device_model_dir_path = result_dir_path
        
    if not os.path.exists(device_model_dir_path): 
        os.makedirs(device_model_dir_path)
    
    file_path = os.path.join(device_model_dir_path, '%s_%s' 
                             % (local_utils.timestamp(), 
                                static_variables.CPU_AND_MEMORY_FILE_NAME))
    result_file = open(file_path, 'w')
    
    if device_model is not None:
        result_file.write('\n%s-%s\n' % (device_model, local_utils.timestamp()))
    else:
        result_file.write('\n%s\n' % local_utils.timestamp())
    
    for each_line in top_out.splitlines():
        result_file.write('%s\n' % each_line)
        line_list = each_line.strip().split()
        process_name = line_list[-1]
        
        if strict_match and process_name != pkg_name:
            continue
        
        if not result_dict.has_key(process_name):
            result_dict[process_name] = {'cpu': [], 'memory': []}
            
        result_dict[process_name]['cpu'].append(line_list[2])
        result_dict[process_name]['memory'].append(line_list[6])
           
    result_file.close() 
    print 'refer cpu and memory detail to %s' % file_path
    return result_dict

def draw_chart(local_utils, src_data_dict, device_model=None, result_dir_path=None):
    try:
        if src_data_dict is None \
            or len(src_data_dict) == 0:
            raise Exception, 'src_data_dict is %s' % src_data_dict
        
        import pychartdir
        
        times = 0
        labels = []
        layer = None
        chart = None
        process_count = 0
        
        cpu_colors = [0x8cd157, 0x57ced1, 0x5777d1, 0x57d175]
        memory_colors = [0x8e57d1, 0xd15757, 0xd1b557, 0xd157b4]
        
        for each_process in src_data_dict:
            cpu = src_data_dict[each_process]['cpu']
            memory = src_data_dict[each_process]['memory']
            
            cpu_data = []
            memory_data = []
            
            for each_cpu in cpu:
                cpu_data.append(string.atoi(each_cpu.split('%')[0]))
            
            for each_memory in memory:
                memory_data.append(string.atof(each_memory.split('K')[0]) / 1024.0)
            
            if times == 0:
                times = len(cpu)
                for i in range(1, times + 1):
                    labels.append(str(i))
                    
                if times <= 50:
                    xArea = times * 40
                elif 50 < times <= 90:
                    xArea = times * 20
                else:
                    xArea = 1800
            
                chart = pychartdir.XYChart(xArea, 800, 0xffffff, 0x000000, 1)
                chart.setPlotArea(60, 100, xArea - 100, 650)
                chart.addLegend(50, 30, 0, 'arialbd.ttf', 15).setBackground(pychartdir.Transparent)
        
                chart.addTitle('cpu and memory info', 'timesbi.ttf', \
                               15).setBackground(0xffffff, 0x000000, pychartdir.glassEffect())
                chart.yAxis().setTitle('Numerical', 'arialbd.ttf', 12)
                chart.xAxis().setTitle('Time / %ss' % interval, 'arialbd.ttf', 12)
                
                chart.xAxis().setLabels(labels)
        
                if times <= 50:
                    step = 1
                else:
                    step = times / 50 + 1
                
                chart.xAxis().setLabelStep(step)
                
                layer = chart.addLineLayer()
                layer.setLineWidth(2)
            
            layer.addDataSet(cpu_data, cpu_colors[process_count], 
                             each_process + '-cpu(%)')
            layer.addDataSet(memory_data, memory_colors[process_count], 
                             each_process + '-memory(M)')
                
            process_count += 1
        
        if result_dir_path is None:
            file_path = os.path.abspath(__file__)
            file_dir = os.path.dirname(file_path)
            root_dir = os.path.dirname(file_dir)
            result_dir_path = os.path.join(root_dir, static_variables.RESULT_DIR_NAME,
                                           static_variables.CPU_AND_MEMORY_DIR_NAME)
        if not os.path.exists(result_dir_path): 
            os.makedirs(result_dir_path)
            
        if device_model is not None:
            device_model = device_model.replace(' ', '_')
            device_model_dir_path = os.path.join(result_dir_path, device_model)
            chart_file_path = os.path.join(device_model_dir_path, '%s_%s.png' \
                                           % (device_model, local_utils.timestamp()))
        else:
            device_model_dir_path = result_dir_path
            chart_file_path = os.path.join(device_model_dir_path, 
                                           '%s.png' % local_utils.timestamp())
            
        if not os.path.exists(device_model_dir_path): 
            os.makedirs(device_model_dir_path)
    
        chart.makeChart(chart_file_path)
        
        return chart_file_path
    
    except Exception, ex:
        print '\ndraw chart failed: %s\n' % str(ex)

if __name__ == '__main__':
    try:
        times = 0
        interval = 1
        
        local_utils = utils.Utils()
        local_utils.start_and_check()
        
#         result_dict = get_cpu_and_memory(local_utils=local_utils, device_id=None, \
#                                          device_model=None, times=times,\
#                                          interval=interval, pkg_name=None, strict_match=False)
#         chart_path = draw_chart(local_utils=local_utils, src_data_dict=result_dict, 
#                                 device_model=None, result_dir_path=None)
#         print 'refer chart to %s' % chart_path
        
        devices_list = local_utils.get_devices_list()
        print devices_list
        for each_device in devices_list:
            device_id = each_device.get('device_id')
            device_model = each_device.get('device_model')
            result_dict = get_cpu_and_memory(local_utils=local_utils, device_id=device_id, \
                                             device_model=device_model, times=times, \
                                             interval=interval, pkg_name=None, strict_match=False)
            chart_path = draw_chart(local_utils=local_utils, src_data_dict=result_dict, 
                                    device_model=device_model, result_dir_path=None)
            print 'refer chart to %s' % chart_path
        
    except Exception, ex:
        print 'ERROR: %s\n' % str(ex)
         
    finally:
        raw_input('press enter to exit ...\n')