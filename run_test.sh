#!/bin/bash

if [ ${#} -ne 1 ]
then
    periode=$(date -d "1 days ago" "+%Y%m%d")
    manual=0
else
    argument=$1
    if [ ${#argument} -eq 8 ]
    then
        periode=${argument}
        manual=1
    else
        echo "Sorry, format argumen should be YYYYMMDD"
        exit
    fi
fi

tahun=${periode:0:4}
bulan=${periode:4:2}

file_config="D:\Yaafi\Learn\tes\config.cfg"
home_dir=`awk '(NR==1) {print $2}' ${file_config}`
log_dir=`awk '(NR==2) {print $2}' ${file_config}`
log_file="${log_dir}/Log_Processing_tes_de_${tahun}${bulan}.dat"


if [ ${manual} -eq 0 ]
then
    last_update=$(date +"%F %T")
    echo "${last_update} : Start ${periode}"
    echo "${last_update} : Start  ${periode}" >> ${log_file}
else
    last_update=$(date +"%F %T")
    echo "${last_update} : [Manual] Start  ${periode}"
    echo "${last_update} : [Manual] Start  ${periode}" >> ${log_file}
fi


last_update=$(date +"%F %T")
echo "${last_update} : scrapping indomart"
echo "${last_update} : scrapping indomart" >> ${log_file}
python python D:/Yaafi/Learn/tes/scraping/klikindomart.py >> ${log_file}

echo "${last_update} : scrapping tokped"
echo "${last_update} : scrapping tokped" >> ${log_file}
python D:/Yaafi/Learn/tes/scraping/tokped_data.py >> ${log_file}

echo "${last_update} : normalisasi indomart"
echo "${last_update} : normalisasi indomart" >> ${log_file}
python D:/Yaafi/Learn/tes/normalisasi/nor_indomart.py >> ${log_file}

echo "${last_update} : normalisasi tokped"
echo "${last_update} : normalisasi tokped" >> ${log_file}
python D:/Yaafi/Learn/tes/normalisasi/nor_tokopedia.py >> ${log_file}

last_update=$(date +"%F %T")
echo "${last_update} : data processing raw_product"
echo "${last_update} : data processing raw_product" >> ${log_file}
python D:/Yaafi/Learn/tes/data_pros/raw_products.py >> ${log_file}

last_update=$(date +"%F %T")
echo "${last_update} : data processing product_master"
echo "${last_update} : data processing product_master" >> ${log_file}
python D:/Yaafi/Learn/tes/data_pros/product_master.py >> ${log_file}

last_update=$(date +"%F %T")
echo "${last_update} : data processing products"
echo "${last_update} : data processing products" >> ${log_file}
python D:/Yaafi/Learn/tes/data_pros/products.py >> ${log_file}

last_update=$(date +"%F %T")
echo "${last_update} : ML prediction price"
echo "${last_update} : ML prediction price" >> ${log_file}
python D:/Yaafi/Learn/tes/ml/ml.py >> ${log_file}

last_update=$(date +"%F %T")
echo "${last_update} : ${periode} Finish"
echo "${last_update} : ${periode} Finish" >> ${log_file}
echo "=======================================================================" >> ${log_file}
