#!/usr/bin/python3
# private classes
from cisco import show_cmd_ssh
# show_cmd_ssh(hostname, username, password, command): 

class TshootBackend:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def get_config(self, list_of_commands, list_of_devices):
        device_output = {}
  
        for device in list_of_devices:
            outputs = []
            for command in list_of_commands:
                if not show_cmd_ssh(device, self.username, self.password, command):
                    return False
                for data in show_cmd_ssh(device, self.username, self.password, command):
                    outputs.append(data.strip('\r\n'))
            device_output[device] = outputs
        return device_output

        




