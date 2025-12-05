#! /bin/bash

while read line
do
   IFS="%" read -r TRIGGERa <<< "$line"
   DATE=$(cut -b 1-2 <<< "${TRIGGERa}")
   TRIGGER=$(sed 's/\r//g' <<< "${TRIGGERa}")
   echo "Downloading Trigger: ${TRIGGER}"
   echo "Year 20${DATE}"
   wget https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/bursts/20${DATE}/bn${TRIGGER}/current/glg_tte_n9_bn${TRIGGER}_v00.fit
   wget https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/bursts/20${DATE}/bn${TRIGGER}/current/glg_tte_n9_bn${TRIGGER}_v01.fit
done < grb_triggers.csv