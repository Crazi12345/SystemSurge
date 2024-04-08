#!/usr/bin/env python3
import os
import pyfiglet
import cmd


class CLI(cmd.Cmd):

    prompt = '>> '
    intro = "Welcome to SystemSurge"
    target_ip = "0.0.0.0"

    def do_config_target_ip(self, line):
        """sets the ip for target"""
        self.target_ip = line.strip()
    def do_vul_analysis(self, line):

        """runs a simple vulnerability analysis"""
        os.system("nmap "+self.target_ip +" -p-")

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
