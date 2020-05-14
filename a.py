from zipfile import ZipFile

with ZipFile('input.zip') as myzip:
    name = myzip.namelist()
for i in name:
    i = i.rstrip('/')
    t = i.split('/')
    print('  ' * (len(t) - 1) + t[-1])