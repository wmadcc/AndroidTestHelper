#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import zipfile
import platform
import subprocess

import static_variables

class Utils:
    def __init__(self):
        '''__init__'''
        self.sys_plat     = platform.platform()
        self.java_home    = os.getenv('JAVA_HOME')
        self.android_home = os.getenv('ANDROID_HOME')
        
        self.cur_dir      = os.path.abspath('.')
        self.file_dir     = os.path.dirname(os.path.abspath(__file__))
        
        if 'windows' in self.sys_plat.lower():
            self.sys_is_windows = True;
        else :
            self.sys_is_windows = False
            
        if self.java_home is None:
            print 'warning: JAVA_HOME is %s ' % self.java_home
        if self.android_home is None:
            print 'warning: system ANDROID_HOME is %s' % self.android_home
            scripts_dir = os.path.dirname(self.file_dir)
            local_android_home = os.path.join(scripts_dir, static_variables.ANDROID_TOOLS_DIR_NAME)
            print 'set android home to local android tools directory %s' % local_android_home
            self.android_home = local_android_home
        
    def print_self_variables(self):
        '''print inner variables of this class'''
        print 'system_platform: %s' % self.sys_plat 
        print 'system_is_windows: %s' % self.sys_is_windows
        
        print 'cur_dir: %s' % self.cur_dir
        print 'file_dir: %s' % self.file_dir
        
        print 'JAVA_HOME: %s' % self.java_home
        print 'ANDROID_HOME: %s' % self.android_home
    
    def timestamp(self):
        '''return current time in specific format'''
        return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    
    def run_system(self, command):
        '''run command in system command line'''
        if isinstance(command, list):
            commands = ''
            for each_arg in command:
                commands = commands + ' ' + each_arg
            commands = commands.strip()
        else:
            commands = command 
        
        print 'run: %s\n' % commands
        os.system(commands)
    
    def run_command(self, command):
        '''get a subprocess to run command in system command line'''
        if isinstance(command, list):
            commands = ''
            for each_arg in command:
                commands = commands + ' ' + each_arg
            commands = commands.strip()
        else:
            commands = command  
        
        print 'run: %s\n' % commands
        
        return subprocess.Popen(commands, shell=True, \
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
    def run_adb(self, command):
        '''get a subprocess to run adb command'''
        if self.android_home is None:
            raise Exception, 'ANDROID_HOME is None, please check system settings'
        
        if self.sys_is_windows:
            adb_tool = os.path.join(self.android_home, 'platform-tools', 'adb.exe')
        else:
            adb_tool = os.path.join(self.android_home, 'platform-tools', 'adb')
            
        if isinstance(command, list):
            command[0:0] = [adb_tool]
        else:
            command = '%s %s' % (adb_tool, command)
        
        return self.run_command(command)
    
    def run_adb_shell(self, command):
        '''get a subprocess to run adb shell command'''
        if self.android_home is None:
            raise Exception, 'ANDROID_HOME is None, please check system settings'
        
        if self.sys_is_windows:
            adb_tool = os.path.join(self.android_home, 'platform-tools', 'adb.exe')
        else:
            adb_tool = os.path.join(self.android_home, 'platform-tools', 'adb')
            
        if isinstance(command, list):
            command[0:0] = [adb_tool, 'shell']
        else:
            command = '%s shell %s' % (adb_tool, command)
            
        return self.run_command(command)
    
    def kill_5037(self):
        '''kill process which is now occupying  port 5037'''
        sys_platform = self.sys_plat.lower()
        
        print 'system platform is %s' % sys_platform
        
        if 'windows' in sys_platform:
            get_pid_process = self.run_command('netstat -ano | findstr 5037 | findstr  LISTEN')
            get_pid_output = get_pid_process.communicate()[0].strip()
        
            if get_pid_output == '':
                print 'Port 5037 is not occupied'
                return
            
            print get_pid_output
            pid = get_pid_output.split()[-1]
            
    #         get_process_name = self.run_command('tasklist /FI 'PID eq %s'' % pid)
    #         process_name_output = get_process_name.communicate()[0].strip()
    #         print process_name_output
    #         process_name = process_name_output.split()[-6]
    #           
    #         get_process_path = self.run_command('wmic process where name=' + \
    #                                                    ''%s' get executablepath' % process_name)
    #         process_path_output = get_process_path.communicate()[0].strip()
    #         print process_path_output
    #         process_path = process_path_output.split()[1]
    #   
    #         process_dir_path = os.path.dirname(process_path)
    #           
    #         self.run_system('explorer.exe %s' % process_dir_path)
            
            self.run_system('taskkill /F /PID %s' % pid)
        
        elif 'linux' in sys_platform:
            print 'system is linux and the code is not debugged!'
            get_pid_process = self.run_command('netstat -apn | grep 5037 | grep LISTEN')
            get_pid_output = get_pid_process.communicate()[0].strip()
            
            if get_pid_output == '':
                print 'Port 5037 is not occupied'
                return
            
            print get_pid_output
            pid = get_pid_output.split()[-1].split('/')[0]
            print 'kill PID: %s' % pid
            self.run_system('kill %s' % pid)
            print 'kill PID: %s successfully!' % pid
            
        elif 'darwin' in sys_platform:
            get_pid_process = self.run_command('lsof -i -P | grep 5037 | grep LISTEN')
            get_pid_output = get_pid_process.communicate()[0].strip()
            
            if get_pid_output == '':
                print 'Port 5037 is not occupied'
                return
            
            print get_pid_output
            pid = get_pid_output.split()[1]
            print 'kill PID: %s' % pid
            self.run_system('kill %s' % pid)
            print 'kill PID: %s successfully!' % pid
            
        else:
            raise Exception, 'unknown system!'
    
    def is_any_device_connected(self):
        '''check whether there is any android device connected'''
        list_devices_process = self.run_adb('devices')
        process_stdout = list_devices_process.communicate()[0].strip()
        if 'device' in process_stdout.split():
            return True
        else:
            return False
    
    def start_and_check(self):
        '''check android devices and restart adb if necessary'''
        self.run_adb('wait-for-device')
        time.sleep(2)

        if not self.is_any_device_connected():
            self.kill_5037()
            time.sleep(1)
            self.run_adb('start-server').communicate()
            time.sleep(1)
            
        if not self.is_any_device_connected():
            raise Exception, 'no android device connected!'
    
    def get_devices_list(self):
        '''get connected android devices list'''
        devices_result = self.run_adb('devices -l')
        result_stdout = devices_result.communicate()[0].strip()
        devices_list = []
        for each_line in result_stdout.splitlines():
            if 'device ' not in each_line:
                continue
            line_list = each_line.split(' ')
            device_id = line_list[0]
            for ecah_element in line_list:
                if ecah_element.startswith('usb:'):
                    device_model = ecah_element.replace(':', '_')
                elif ecah_element.startswith('model:'):
                    device_model = ecah_element[6:]
                    break
            devices_list.append({'device_id': device_id, 'device_model': device_model})
        
        if len(devices_list) == 0:
            print 'WARN: devices_list is empty which indicates that no android device exist!'
            
        return devices_list
    
    def get_app_pid_list(self, pkg_name, device_id=None):
        '''get app pid list'''
        app_pid_list = []
        
        if device_id is None:
            print 'get app pid list of %s' % pkg_name
            device_id_shell = 'shell'
        else:
            print 'get app pid list of %s in device %s' % (pkg_name, device_id)
            device_id_shell = '-s %s shell' % device_id
            
        if self.sys_is_windows:
            get_pid_process = self.run_adb('%s ps | findstr %s$' % (device_id_shell, pkg_name))
        else:
            get_pid_process = self.run_adb('%s ps | grep -w %s' % (device_id_shell, pkg_name))
            
        get_pid_process_stdout = get_pid_process.communicate()[0].strip()
        result_lines = get_pid_process_stdout.splitlines()
        if result_lines == []:
            print "the process doesn't exist"
            return app_pid_list
        
        for each_line in result_lines:
            app_pid_dict = {}
            word_list = each_line.split(' ')
            word_list.remove(word_list[0])
            pattern = re.compile(r'\d+')
            pid = pattern.findall(' '.join(word_list))[0]
            app_pid_dict['process_name'] = word_list[-1].strip()
            app_pid_dict['pid'] = pid
            app_pid_list.append(app_pid_dict)
        return app_pid_list
    
    def kill_process(self, pkg_name, device_id=None):
        '''kill specific package process'''
        if device_id is None:
            device_id_shell = 'shell'
        else:
            device_id_shell = '-s %s shell' % device_id
        app_pid_list = self.get_app_pid_list(pkg_name, device_id)
        if app_pid_list == []:
            print 'there is no process named %s' % pkg_name
        else:
            for each_pid_dict in app_pid_list:
                process_name = each_pid_dict.get('process_name')
                pid = each_pid_dict.get('pid')
                print 'kill PID: %s of process %s ...' % (pid, process_name)
                kill_process = self.run_adb('%s kill %s' % (device_id_shell, pid))
                print kill_process.communicate()[0].strip()
  
    def get_focused_package_and_activity(self, device_id=None, device_model=None):
        '''get focused package and activity'''
        if device_model is None:
            print 'get focused package and activity ...'
        else:
            print 'get focused package and activity from %s ...' % device_model
        
        if self.sys_is_windows:
            find_util = 'findstr'
        else:
            find_util = 'grep'        
        
        if device_id is None:
            shell_str = 'shell'
        else:
            shell_str = '-s %s shell' % device_id
        
        pattern = re.compile(r'[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+')
        dump_process = self.run_adb('%s dumpsys window w | %s \/ | %s name=' 
                                    % (shell_str, find_util, find_util))
        dump_process_stdout = dump_process.communicate()[0].strip()
        pkg_and_act_str = pattern.findall(dump_process_stdout)[0]
        pkg_name = pkg_and_act_str.split('/')[0]
        activity = pkg_and_act_str.split('/')[1]
        print 'package: %s, activity: %s' % (pkg_name, activity)
        
        return {'package': pkg_name, 'activity': activity}
    
    def get_current_package_name(self, device_id=None, device_model=None):
        '''get current package name'''
        return self.get_focused_package_and_activity(device_id, device_model)['package']
    
    def get_current_activity(self, device_id=None, device_model=None):
        '''get current activity'''
        return self.get_focused_package_and_activity(device_id, device_model)['activity']
        
    def get_3rd_packages_dict(self, device_id=None, device_model=None):
        '''get 3rd packages dictionary(key: name, value: path)'''
        packages_dict = {}
        if device_id is None:
            shell_str = 'shell'
        else:
            shell_str = '-s %s shell' % device_id
        
        if device_model is None:
            print 'get 3rd packages list(name and path) ...'
        else:
            print 'get 3rd packages list(name and path) from %s ...' % device_model
            
        list_3rd_packages_process = self.run_adb('%s pm list packages -f -3' % shell_str)
        process_stdout = list_3rd_packages_process.communicate()[0].strip()
        for each_line in process_stdout.splitlines():
            pkg_name = each_line.split(':')[-1].split('=')[-1].strip()
            pkg_path = each_line.split(':')[-1].split('=')[0].strip()
            packages_dict[pkg_name] = pkg_path
        
        if len(packages_dict) == 0:
            print 'WARN: packages_dict is empty which indicates that no 3rd package exist!'
        
        return packages_dict
      
    def get_packages_dict(self, device_id=None, device_model=None):
        '''get packages dictionary(key: name, value: path)'''
        packages_dict = {}
        if device_id is None:
            shell_str = 'shell'
        else:
            shell_str = '-s %s shell' % device_id
        
        if device_model is None:
            print 'get packages list(name and path) ...'
        else:
            print 'get packages list(name and path) from %s ...' % device_model
            
        list_packages_process = self.run_adb('%s pm list packages -f' % shell_str)
        process_stdout = list_packages_process.communicate()[0].strip()
        for each_line in process_stdout.splitlines():
            pkg_name = each_line.split(':')[-1].split('=')[-1].strip()
            pkg_path = each_line.split(':')[-1].split('=')[0].strip()
            packages_dict[pkg_name] = pkg_path
        
        if len(packages_dict) == 0:
            print 'WARN: packages_dict is empty which indicates that no package exist!'
        
        return packages_dict
                    
    def get_file_name(self, file_path):
        '''get file name from file path exclude file type'''
        file_full_name = os.path.basename(file_path);
        last_point_index = file_full_name.rfind('.')
        
        if last_point_index < 0:
            return file_full_name
        else:
            return file_full_name[0:last_point_index]
     
    def zip_dir(self, dir_name, zip_file_name=None):
        '''zip target directory into zip file '''
        if zip_file_name is None:
            if os.path.isfile(dir_name):
                zip_file_name =  os.path.join(os.path.dirname(dir_name), \
                                          self.get_file_name(dir_name) + '.zip')
            else:
                zip_file_name =  os.path.join(os.path.dirname(dir_name), \
                                          os.path.basename(dir_name) + '.zip')
        
        print 'zip %s to %s' % (dir_name, zip_file_name)
        zf = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
        if os.path.isfile(dir_name):
            zf.write(dir_name, os.path.basename(dir_name))
        else :
            files_list = []
            empty_dirs = []
            for root, dirs, files in os.walk(dir_name):
                for each_dir in dirs:
                    abs_dir_path = os.path.join(root, each_dir)
                    if os.listdir(abs_dir_path) == []:
                        empty_dirs.append(abs_dir_path)
                        
                for name in files:
                    files_list.append(os.path.join(root, name))
        
            for file_name in files_list:
                arcname = os.path.relpath(path=file_name, start=dir_name)
                zf.write(file_name, arcname) 
                   
            for each_dir in empty_dirs:
                dir_relpath = os.path.relpath(path=each_dir, start=dir_name)
                zip_info = zipfile.ZipInfo(os.path.join(dir_relpath, ''))
                zf.writestr(zip_info, '')
            
        zf.close()
        return zip_file_name

    def unzip_file(self, zip_file_name, unzip_to_dir=None):
        '''unzip zip file to target directory'''
        if  unzip_to_dir is None:
            unzip_to_dir = os.path.join(os.path.dirname(zip_file_name), \
                                        self.get_file_name(zip_file_name))
        
        print 'unzip %s to %s' % (zip_file_name, unzip_to_dir)
        
        if not os.path.exists(unzip_to_dir): 
            os.makedirs(unzip_to_dir)
            
        zf = zipfile.ZipFile(zip_file_name, 'r', zipfile.ZIP_DEFLATED)
        zf.extractall(unzip_to_dir)
        zf.close()
        return unzip_to_dir
      
    def __del__(self):
        pass
        
if __name__ == '__main__':
    local_utils = Utils()
    local_utils.print_self_variables()
#     print local_utils.run_command('echo $PATH').stdout.read()
#     print local_utils.run_command(['echo', '$PATH']).stdout.read()
#     adb_test = local_utils.run_adb('devices')
#     print adb_test.stdout.read()
#     print adb_test.stderr.read()
#     print local_utils.get_devices_list()
#     
#     test_dir = os.path.join(os.path.dirname(__file__), '__init__.zip')
#     print local_utils.zip_dir(test_dir)
#     shutil.rmtree(test_dir)
#     print local_utils.unzip_file(test_dir)
    print local_utils.get_devices_list()
    raw_input('press enter to exit ...\n')