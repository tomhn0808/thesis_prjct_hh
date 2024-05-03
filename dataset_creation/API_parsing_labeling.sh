#!/bin/bash

#Get json data from VirusTotal API
json_data=$(curl --request GET \
  --url https://www.virustotal.com/api/v3/files/"$1" \
  --header 'x-apikey: '$2'')  # $1=first argument
#Get json data from VirusShare API
#json_data=$(curl --url "https://virusshare.com/apiv2/quick?apikey=your_virusshare_api_key&hash=$1")
#Check if successful curl execution and data retrieve



#Parse the json and print some information if any of those information is provided by VirusTotal 
echo "Threat category detected:"
jq ".data.attributes.popular_threat_classification.popular_threat_category" <<< "$json_data"

echo -e " \n Family of malware detected and a count of how many AV have detected as such:"
jq ".data.attributes.popular_threat_classification.popular_threat_name" <<<  "$json_data"

echo -e " \n Suggested threat label identified by a majority of AV:"
jq ".data.attributes.popular_threat_classification.suggested_threat_label" <<< "$json_data"

echo -e " \n Tags associated with the file:"
jq ".data.attributes.tags" <<< "$json_data"

# Parse data from VirusTotal API

#First, compact data to make sure it is accepted format for AVClass labeling tool
json_data_compacted=$(jq -c "." <<< "$json_data")
echo "$json_data_compacted" > report.json

#Second, Get the malware family out of the report
avclass_report_fam=$(avclass -f report.json)
malware_fam=$(echo "$avclass_report_fam" | cut -d$'\t' -f2-)

#Third, Get report with class of malware, filetype, MD5 hash value, etc.
#Multiple filtering to extract information in different variable using regular expression
# Hash value, all class of malware identified, the name and the support nb of the major class identified
avclass_report=$(avclass -f report.json -t)

hashvalue=$(echo "$avclass_report" | cut -d$'\t' -f1)

report_file=$(echo "$avclass_report" | grep -o 'FILE:[^|]*')

report_class=$(echo "$avclass_report" | grep -o 'CLASS:[^,]*')
class_name=$(echo "$report_class" | grep -o ':\([^|]*\)' | sed 's/://g')
major_class=$(echo "$class_name" | tr ' ' '\n' | head -n 1)

class_nb_support=$(echo "$report_class" | grep -o '\|[0-9]*$')
number_major_class=$(echo "$class_nb_support" | tr ' ' '\n' | head -n 1)

#Calcul the total nb of time a class is identified
class_nb_sum=$(echo "$report_class" | grep -o '\|[0-9]*$' | sed 's/[^0-9]//g' | awk '{s+=$1} END {print s}')
#Print each variable
echo $report_class
echo $class_name
echo $major_class
echo $class_nb_support
echo $number_major_class
echo $class_nb_sum

#Calculate percentage
percentage=$(echo "100 * $number_major_class / $class_nb_sum" | bc)
echo "$number_major_class is $percentage % of CLASS detected"

#Validate the data and put the (MD5) hash value in a txt file for an isolation of the hash value of specific trojan threat
if [[ $percentage -gt 80 ]]; then

  # Do something if the value is greater than 80 %
  if [[ $major_class == "backdoor" || $major_class == "backdoor:webshell" ]]; then
    echo "$hashvalue" >> backdoor.txt
  fi
  if [[ $major_class == "rootkit" ]]; then
    echo "$hashvalue" >> rootkit.txt
  fi
  if [[ $major_class == "downloader" ]]; then
    echo "$hashvalue" >> downloader.txt
  fi
  if [[ $major_class == "ransomware" ]]; then
    echo "$hashvalue" >> ransomware.txt
  fi
  if [[ $major_class == "ddoser" ]]; then
    echo "$hashvalue" >> ddoser.txt
  fi
  if [[ $major_class == "expkit" ]]; then
    echo "$hashvalue" >> expkit.txt
  fi
  if [[ $major_class == "fakeantivirus" ]]; then
    echo "$hashvalue" >> fakeantivirus.txt
  fi
  echo "The value $value is higher than 80.00"
fi
