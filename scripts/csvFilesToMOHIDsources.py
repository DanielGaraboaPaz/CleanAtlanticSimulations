#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 12:20:21 2019

@author: gfnl143
"""

import xml.etree.ElementTree as ET
import pandas as pd
import argparse

def indent(elem, level=2):
    i = "\n" + level*"   "
    j = "\n" + (level-1)*"   "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem


def csvRowToMOHIDDischargeFileSourceElemXML(root,source_id,name,x,y,z,rateFile):
    doc = ET.SubElement(root, "source")
    ET.SubElement(doc, "setsource", id=str(source_id),name=str(name))
    RateFileElement=ET.SubElement(doc, "rateTimeSeries")
    ET.SubElement(RateFileElement,"file",comment="name of csv file with discharge information (time and rate columns)",name=str(rateFile))
    ET.SubElement(RateFileElement,"scale",comment="scales the data on the file by this factor (not time)",value="1",)
    ET.SubElement(doc, "point",units_comment="(deg,deg,m)", x=str(x),y=str(y),z=str(z))
    return root


def csvRowToMOHIDPointSourceElemXML(root,source_id,name,x,y,z,rate,start=0,end='end'):
    doc = ET.SubElement(root, "source")
    ET.SubElement(doc, "setsource", id=str(source_id),name=name)
    ET.SubElement(doc, "rate", value=str(rate), comment="emission rate (Hz)")
    ET.SubElement(doc, "active", start=str(start), end =str(end))
    ET.SubElement(doc, "point", x=str(x),y=str(y),z=str(z),units_comment="(deg,deg,m)")
    return root

def csvRowToMOHIDTypeSourceElemXML(root,i,materialType,properties):

    ET.SubElement(root, "type", source=str(i),type=materialType,property=str(properties))

    return root



def toMOHIDLagrangianEmisorFile(df,fileName,timeUnits='seconds',scale=1):
        
    if timeUnits == 'seconds': 
        timeInUnits=(df.index-df.index[0]).total_seconds().values
        units = 'SECONDS'
    elif timeUnits ==  'days':
        timeInUnits=(df.index-df.index[0]).total_seconds().values/(3600.*24.)
        units = 'DAYS'
    
    format_string = '{:<16s} {:<1s}'
    f = open(fileName,'w+')
    f.write('TIME_CYCLE                : 0\n')
    f.write('TIME_UNITS                : '+units+'\n')
    f.write('SERIE_INITIAL_DATA        : ' + df.index[0].strftime('%Y %m %d %H %M %S')+'\n' )
    f.write('\n')
    f.write('!time          rate\n')
    f.write('<BeginTimeSerie>\n')
    k=0
    for time in timeInUnits:
        f.write(format_string.format(*[str(int(time)),str(df.magnitude[k]*scale)])+'\n')
        k=k+1
    f.write('<EndTimeSerie>')
    f.close()


def main():
    """
    to run the conversor is python main.py -f filename.csv
    Then copy the content from the output file filename.xml into sources your CEFAS_case.xml.
    The structure of your csv file must be:

    source_id,name,x,y,z,rate,start,end
    1,'name_or_source_1',0,10,0,1,1,1000
    2,'name_or_source_2',10,10,0,1,1,1000

        <type source="2" type='plastic' property="bag_1" comment="" />
        <type source="3" type='paper' property="cardboard_1" comment="" />
    ...
    """
    parser = argparse.ArgumentParser(description='CSV point file to MOHID Sources XML block')
    parser.add_argument("-f", "--file", dest="csvFilename", help="csv file style with columns names: source_id,name,x,y,z,rate,start,end")
    args = parser.parse_args()


    # Start the root for the MOHIDLagrangian setup
    xmlMOHIDtree = ET.Element("root")

    # Start the source definitions block
    sourceDefinitions = ET.SubElement(xmlMOHIDtree, "sourceDefinitions")
    df = pd.read_csv(args.csvFilename, delimiter=',')
    if 'file' in df:
        sourceId = 0
        for index, row in df.iterrows():
            if 'type' in row:
                materialTypes = row['type'].split('-')
                properties = row['property'].split('-')
                k = 0
                for materialType in materialTypes:
                    source_name = row['name'] + '_' + materialTypes[k] + '_' + properties[k]
                    sourceDefinitions = csvRowToMOHIDDischargeFileSourceElemXML(sourceDefinitions,
                                                                                sourceId, source_name,
                                                                                row.x, row.y, row.z,
                                                                                'data/'+row['file'])
                    print('-> Adding file source', row.name)
                    sourceId = sourceId+1
                    k = k+1
            else:
                sourceDefinitions = csvRowToMOHIDDischargeFileSourceElemXML(sourceDefinitions,
                                                                            sourceId,row['name'],
                                                                            row.x,row.y,row.z,
                                                                            'data/'+row['file'])
                print('-> Adding file source', row.name)
                sourceId = sourceId+1

    else:
        sourceId = 0
        for index, row in df.iterrows():
            if 'type' in row:
                materialTypes = row['type'].split('-')
                properties = row['property'].split('-')
            else:
                materialTypes = []
            k=0
            for materialType in materialTypes:
                source_name = row['name'] + '_'+ materialTypes[k] + '_' + properties[k]
                sourceDefinitions = csvRowToMOHIDPointSourceElemXML(sourceDefinitions,
                                                                    sourceId, source_name,
                                                                    row.x, row.y, row.z,
                                                                    row.rate)
                print('-> Adding point source', row)
                sourceId = sourceId+1
                k=k+1

    # Start the type definitions block
    typesDefinitions = ET.SubElement(xmlMOHIDtree,"types")
    sourceId = 0
    for index, row in df.iterrows():
        k = 0
        materialTypes = row['type'].split('-')
        properties = row['property'].split('-')
        for materialType in materialTypes:
            typesDefinitions = csvRowToMOHIDTypeSourceElemXML(typesDefinitions,
                                                              sourceId,
                                                              materialTypes[k],
                                                              properties[k])
            print('Adding types', row['name'])
            k = k+1
            sourceId = sourceId+1

    indent(xmlMOHIDtree)
    tree = ET.ElementTree(xmlMOHIDtree)
    tree.write(args.csvFilename.replace('.csv', '.xml'))

main()
