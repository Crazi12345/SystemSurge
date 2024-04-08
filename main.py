#!/usr/bin/env python3
import os
import pyfiglet
import cmd


class CLI(cmd.Cmd):

    prompt = '>> '
    intro = "Welcome to SystemSurge"

    def do_hello(self, line):
        """Print a greeting."""
        print("Hello, World!")

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
