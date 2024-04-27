import subprocess
import time
list_hashes=[]
apikey1="you_VirusTotal_API_key"
with open("hashes2.txt", 'r') as fi:
    for line in fi:
        clean_line = line.rstrip('\n')
        list_hashes.append(clean_line)
for hash in list_hashes:
        apikey="apikey" + str(apikey1)
        api_key = f"{apikey}"
        api_key_bash = eval(api_key)
        subprocess.run(["./API_parsing_labeling.sh",hash,api_key_bash])
print(list_hashes)
