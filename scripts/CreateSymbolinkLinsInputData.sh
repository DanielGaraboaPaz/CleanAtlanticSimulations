#!/bin/bash
function SimboLinkForInputData(){
    data_type=$1
    source_path=$2
    sim_main_path=$3

    meteo_path='/input_data/meteorology'
    waves_path='/input_data/waves'
    hydro_path='/input_data/hydrodynamic'
    watqu_path='/input_data/waterQuality'

    if [ "$1" == "meteorology" ]; then
        ln -s $2 $3$meteo_path

    elif [ "$1" == "waves" ]; then
        ln -s $2 $3$waves_path

    elif [ "$1" == "waterQuality" ]; then
        ln -s $2 $3$watqu_path

    elif [ "$1" == "hydrodynamic" ]; then
        ln -s $2 $3$hydro_path

    else
        echo 'Introduce one of the following options:' "meteorology", "waves", "waterQuality" 'or' "hydrodynamic"
    fi  

}


SimboLinkForInputData meteorology $ATLANTIC_WINDS_PATH Atlantic_OceanSources
SimboLinkForInputData waves $ATLANTIC_WAVES_PATH Atlantic_OceanSources
SimboLinkForInputData waterQuality $ATLANTIC_WATERQUALITY_PATH Atlantic_OceanSources
SimboLinkForInputData hydrodynamic $ATLANTIC_HYDRODYNAMIC_PATH Atlantic_OceanSources

SimboLinkForInputData meteorology $ATLANTIC_WINDS_PATH Atlantic_Rivers
SimboLinkForInputData waves $ATLANTIC_WAVES_PATH Atlantic_Rivers
SimboLinkForInputData waterQuality $ATLANTIC_WATERQUALITY_PATH Atlantic_Rivers
SimboLinkForInputData hydrodynamic $ATLANTIC_HYDRODYNAMIC_PATH Atlantic_Rivers

SimboLinkForInputData meteorology $PORTUGAL_WINDS_PATH Atlantic_Rivers
SimboLinkForInputData waves $PORTUGAL_WAVES_PATH Atlantic_Rivers
SimboLinkForInputData waterQuality $PORTUGAL_WATERQUALITY_PATH Atlantic_Rivers
SimboLinkForInputData hydrodynamic $PORTUGAL_HYDRODYNAMIC_PATH Atlantic_Rivers

SimboLinkForInputData meteorology $SPAIN_WINDS_PATH Atlantic_Rivers
SimboLinkForInputData waves $SPAIN_WAVES_PATH Atlantic_Rivers
SimboLinkForInputData waterQuality $SPAIN_WATERQUALITY_PATH Atlantic_Rivers
SimboLinkForInputData hydrodynamic $SPAIN_HYDRODYNAMIC_PATH Atlantic_Rivers


