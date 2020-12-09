# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

import xml.etree.ElementTree as ET
import glob

bateas_polygons_kml = glob.glob('*.kml')

root_template = ET.parse('TEMPLATE.kmz')
#template_coordinates = root_template.getroot().findall('Document/Placemark/Polygon/outerBoundaryIs/LinearRing/coordinates')[0].text

for kml_file in bateas_polygons_kml:
    try:
        root_polygon = ET.parse(kml_file)
        polygon_coordinates = root_polygon.getroot().findall('Placemark/MultiGeometry/Polygon/outerBoundaryIs/LinearRing/coordinates')[0].text
        root_template.findall('Document/Placemark/Polygon/outerBoundaryIs/LinearRing/coordinates')[0].text = polygon_coordinates
        root_template.write(kml_file.replace('.kml','.kmz').replace(' ',''))
    except:
        pass
    
