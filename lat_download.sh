#! /bin/bash

while read line
do
   NAME=${line%-*}
   KEY=${line##*-}
   KEY=${KEY//$'\r'}
   echo "Downloading Key: ${KEY}"
   echo "Naming it for Event ${NAME}"
   wget https://fermi.gsfc.nasa.gov/FTP/fermi/data/lat/queries/${KEY}_PH00.fits
   mv ${KEY}_PH00.fits LAT_files/${NAME}_PH00.fits
done < fermi_ids.csv
