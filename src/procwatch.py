import os
import sys
import subprocess
from datetime import datetime

class procwatch:
    def __init__(self, appName: str):
        self.appName = appName
        self.userid = str(os.getuid())
        self.runningApps = {}

    def getRunningApps(self):
        """
        Get a list of currently running processes along with their current RSS

        :return: A dict containing a list of all running processes
        """
        app = self.appName
        process = subprocess.Popen(
            ['ps', '-u', self.userid, '-o', 'rss,comm'], stdout=subprocess.PIPE, stderr=None)
        out, _ = process.communicate()
        # Clean output of newlines for parsing
        output = out.decode().replace('\n', ' ').strip()  # .replace(' ', '')
        list = output.split(' ')
        try:
            for i in range(len(list)):
                item = list[i]
                if item == '':
                    list.pop(i)
                else:
                    if item.isdigit():
                        if list[i + 1] in self.runningApps:
                            self.runningApps[list[i + 1]
                                         ].append({list[i + 1]: int(item)})
                        else:
                            self.runningApps[list[i + 1]
                                         ] = [{list[i + 1]: int(item)}]
        except IndexError:
            if app not in self.runningApps:
                raise LookupError("Application is not running or is not accessable")
            return self.runningApps[app]

    def getMemoryMb(self):
        """
        Get an application's current memory usage in Megabytes

        :return: Current memory usage in Megabytes (float)
        """
        processes = self.getRunningApps()
        final_rss = 0
        for proc in processes:
            final_rss += proc[self.appName]
        return final_rss / 1000

    def getMemoryKb(self):
        """
        Get an application's current memory usage in Kilobytes

        :return: Current memory usage in Kilobytes (float)
        """
        processes = self.getRunningApps()
        final_rss = 0
        for proc in processes:
            final_rss += proc[self.appName]
        return final_rss

    def getRunningTime(self):
        """
        Get an application's elapsed time

        :return: String containing the elapsed time in (%H:%M:%S) format
        """
        processes = self.getRunningApps()
        process = subprocess.Popen(
            ['ps', '-u', self.userid, '-o', 'rss,pid'], stdout=subprocess.PIPE, stderr=None)
        out, _ = process.communicate()
        output = out.decode()
        proc = str(processes[0][self.appName])
        for line in output.split('\n'):
            if proc in line:
                try:
                    pid = line.split('   ')[1].strip()
                except IndexError:
                    pid = line.split('  ')[1].strip()
        process = subprocess.Popen(
            ['ps', '-q', pid, '-o', 'etime'], stdout=subprocess.PIPE, stderr=None)
        out, _ = process.communicate()
        elapsed = out.decode().split('\n ')[1].strip()  # Clean string for returning
        return elapsed
