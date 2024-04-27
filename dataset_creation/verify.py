import hashlib
import os
from collections import defaultdict

folder="/home/user/Downloads/collected_data/"
file_hashes=defaultdict(int)

#Compute hash value (SHA256) of all files in the directory and create a dictionnary containing all those hash values as key
for filename in os.listdir(folder):
	full_path=os.path.join(folder,filename)
	if os.path.isfile(full_path):
		with open(full_path,'rb') as f:
			hasher=hashlib.sha256()
			hasher.update(f.read())
			file_hash=hasher.hexdigest()
		file_hashes[file_hash]+=1

#Check for duplicates (if the value associated with a specific hash value is more than 1 == duplicate)
duplicates_found=False
for file_hash, count in file_hashes.items():
	if count > 1:
		duplicates_found = True
		print(f"Found {count} files with the same hash: {file_hash}")
if not duplicates_found:
	print("No duplicate files found in the folder")
print(file_hashes)

#Put all hashes in a list
list_hashes=[]
for key in file_hashes.keys():
		list_hashes.append(f"{key}\n")
print(list_hashes)
#Write each component of this list in "hashes2.txt"
with open("hashes2.txt", 'w') as fi:
		fi.writelines(list_hashes)