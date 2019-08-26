import re
import subprocess
from subprocess import Popen, PIPE
import sys
import json
import os
from urllib.request import urlopen

def by_value(item):
    return item[1]
def readText(file):
    text = {}
    with open('/app/src/url_to_json/'+file+'.out', "r+") as f:
        line = f.readlines()
        lines = [line.rstrip('\n') for line in open('/app/src/url_to_json/'+file+'.out', "r")]

        for l in lines:
            if(re.findall(r"[A-Za-z]{1,}\.", l)):
                text[l] = 0
    return text
def webscraper(url, regexpr):
    file = 'plik.txt'
    text = {}
    print(regexpr)
    session = subprocess.check_output(['./app/src/url_to_json/script.sh',"%s" % (url), file, "%s" % (regexpr)])
    print("Webscrapped page ")
    try:
#[A-Za-z]{1,}\.
#([A-Z]\w+.)+(\w+|\w-[0-9]+.)\w+
        text = readText(file)

        app_json = json.dumps(text, indent=4)
        p = open('/app/src/url_to_json/'+file.split(".")[0]+'.json', "w+")
        p.write(app_json)
        p.close()
        return app_json
    except subprocess.CalledProcessError:
        print('Cannot call the process')
        return -1
	#val = subprocess.check_call("./script.sh %s %s" % (url, str(file)), shell=True)"
