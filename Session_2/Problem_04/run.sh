#!/bin/bash

# set aimes meta data
source ../../Session_1/export_aims_metadata.sh

# run calculation 
$fhi_aims | tee output | grep Total\ energy\ uncorrected