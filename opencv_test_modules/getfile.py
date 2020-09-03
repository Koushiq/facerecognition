import os
arr = os.listdir('myfolder')
getid = len(arr)+1

for fp in arr:
    fileinfo=fp.split('-')
    id=int(fileinfo[0])
    print(id)