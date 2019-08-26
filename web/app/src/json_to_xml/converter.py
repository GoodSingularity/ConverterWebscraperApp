#!/usr/bin/python

import json
import sys
import os
from json import loads
from lxml import etree
from copy import deepcopy
import argparse
import pathlib
def xmlify(src, vr):
    output = ""
    provisioning = etree.Element("provisioning",
                                 version="1.1", productID=str(vr))
    nvm = etree.SubElement(provisioning, 'nvm')

    with open("/app/src/json_to_xml/"+str(src), "r") as f:
        data = json.load(f)
        for i in data:
            etree.SubElement(nvm, "param",
                             name=str(i), value=str(data[i]))

    content = etree.tostring(provisioning).decode('ascii')
    content = content.replace("><", "> \n<")
    root = etree.XML(content)
    output = etree.tostring(root, xml_declaration=True,
                            encoding='UTF-8').decode('ascii')
    return output
def converter(src,dst,vr):
    output = xmlify(src,vr)
    p = open('/app/src/json_to_xml/'+dst+'', "w+")
    p.write(str(xmlify(src, vr)))
    p.close()
    print("Json to XMl extracted!")
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help='&source of the json file&')
    parser.add_argument("destination", help='&destination of new xml file&')
    parser.add_argument("-version", help='&version, productID&', default="mxb")
    args = parser.parse_args()
    if(not (args.src.endswith('.json')) and (args.dst.endswith('.xml'))):
        sys.exit()
    converter(args.src, args.destination, args.version)
