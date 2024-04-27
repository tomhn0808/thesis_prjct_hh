import os
import shutil
directory_path = "/home/user/Downloads/collected_data/"
list_hashes=[]

#Example with Downloader Trojans here
with open("downloader.txt", 'r') as fi:
    for line in fi:
        clean_line = line.rstrip('\n')
        list_hashes.append(clean_line)

for hashes in list_hashes:
    # Filename format from VirusShare == "VirusShare_MD5hashvalue"
    filename = f"VirusShare_{hashes}"
    #Copy the file from source dir to isolated directory with all similarly identified trojans
    source_path = os.path.join(directory_path, filename)
    shutil.copy(source_path, '/home/user/Documents/downloader/')
    print(source_path)
