import ftplib, os

# take in FTP object and retrieve binary file
def getFile(ftp, filename):
    try:
        ftp.retrbinary('RETR ' +filename, open(filename,'wb').write)
    except:
        print('Error downloading ' +filename)

# take in FTP and upload to remote FTP server
def upLoad(ftp, filename):
    ext = os.path.splitext(filename)[1]
    if ext in ('.txt','.html','.htm','.csv'):
        ftp.storlines('STOR ' +filename, open(filename))
    else:
        ftp.storbinary('STOR ' +filename, open(filename, 'rb'), 1024)

# connect to server with credentials
ftp = ftplib.FTP('ftp.nluug.nl')
ftp.login('anonymous','ftplib-example')

data = []

ftp.cwd('/pub')
ftp.dir(data.append)
for dirs in data:
    print('-' +dirs)

print('Downloading README')
getFile (ftp,'README.nluug')
print('Download complete')

print('Uploading README')
try:
    upLoad(ftp,'README.nluug')
    print('Upload complete')
except:
    print('Failed to upload, invalid permission')

# close ftp connection
ftp.quit()
