#!/bin/bash
python -m MOSI -i CDS_winds.json -s CDS -f 1d
python -m MOSI -i CMEMS_currents_2D.json -s CMEMS -f 1d
python -m MOSI -i CMEMS_currents_3D.json -s CMEMS -f 1d
python -m MOSI -i CMEMS_salt.json -s CMEMS -f 1d
python -m MOSI -i CMEMS_temp.json -s CMEMS -f 1d
python -m MOSI -i CMEMS_waves.json -s CMEMS -f 1d
