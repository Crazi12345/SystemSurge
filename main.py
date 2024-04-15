#!/usr/bin/env python3
import os
import pyfiglet
import cmd
import subprocess
import json
import re


class CLI(cmd.Cmd):

    prompt = '>> '
    intro = "Welcome to SystemSurge"
    target_ip = "0.0.0.0"
    target_user = "root"
    target_pass = "easybot"

    def do_version(self, line):
        """version checker"""
        with open('./Versions.json') as f:
            data = json.load(f)
        for key, value  in data.items():
            command = "sshpass -p "+self.target_pass+" ssh -t "+self.target_user + "@"+self.target_ip+" "+data[key]["version_cmd"]
            result = subprocess.getoutput(command)
            result = result.replace(self.target_ip, "")
            x = re.search(data[key]["regex"], result)
            try:
                if x.group() != data[key]["safe_version"]:
                    print('\x1b[2;30;41m' + key+ " "+x.group() +" "+ '\x1b[0m')
                else:
                    print( key+" "+x.group())
            except Exception as e:
                print(key+ " COULD NOT BE FOUND")
    def do_dos(self, line):
        """Attacks the dashboard server"""
        os.system("printf \"get robot model\"|nc "+self.target_ip+" 29999")

    def do_ip(self, line):
        """sets the ip for target"""
        self.target_ip = line.strip()

    def do_pass(self, line):
        """sets the pass for target"""
        self.target_pass = line.strip()
    def do_user(self, line):
        """sets the user for target"""
        self.target_user = line.strip()

    def do_vul_analysis(self, line):
        """runs a simple vulnerability analysis"""
        os.system("nmap "+self.target_ip + " -p-")

    def do_quit(self, line):
        """Exit the CLI."""
        return True


if __name__ == '__main__':
    try:
        ascii_banner = pyfiglet.figlet_format("SystemSurge")
        print(ascii_banner)
    except:
        pass

    CLI().cmdloop()
