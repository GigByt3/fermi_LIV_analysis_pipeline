#! /bin/bash

while read line
do
   IFS="%" read -r TRIGGERa <<< "$line"
   DATE=$(cut -b 1-2 <<< "${TRIGGERa}")
   TRIGGERb=$(sed 's/\r//g' <<< "${TRIGGERa}")
   TRIGGER="${TRIGGERb}${SUB}"
   echo "Downloading Trigger: ${TRIGGER}"
   echo "Year 20${DATE}"
   for i in 1 2 3 4 5 6 7 8 9;
   do
   wget https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/bursts/20${DATE}/bn${TRIGGER}/current/glg_tte_n${i}_bn${TRIGGER}_v00.fit
   wget https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/bursts/20${DATE}/bn${TRIGGER}/current/glg_tte_n${i}_bn${TRIGGER}_v01.fit
   mv glg_tte_n${i}_bn${TRIGGER}_v00.fit GBM_files/glg_tte_n${i}_bn${TRIGGER}_v00.fit
   mv glg_tte_n${i}_bn${TRIGGER}_v01.fit GBM_files/glg_tte_n${i}_bn${TRIGGER}_v01.fit; 
   done
done < fermi_ids.csv