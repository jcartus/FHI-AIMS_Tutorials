#!/bin/bash

# set aimes meta data
source ../export_aims_metada.sh

# run calculation 
$fhi_aims | tee output | grep Total\ energy\ uncorrected