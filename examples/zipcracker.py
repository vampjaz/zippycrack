## example to decrypt password-protected zip files

## something strange i've found: zipfiles sometimes can be decrypted by multiple different passwords

import zipfile,zippycrack,sys,os

if len(sys.argv) != 3 and len(sys.argv) != 4:
	print "usage: zipcracker.py <zipfile> <password list> [num threads]"
	sys.exit(1)

filename = sys.argv[1]
pwlist = sys.argv[2]
thr = 4
try:
	if len(sys.argv) == 4:
		thr = int(sys.argv[3])
except:
	print "error: incorrect number of threads"
	sys.exit(4)

if not os.path.exists(filename):
	print "error: zip file {} doesn't exist".format(filename)
	sys.exit(2)

if not os.path.exists(pwlist):
	print "error: password list file {} doesn't exist".format(pwlist)
	sys.exit(3)

def try_deflate(password):
	try:
		zfile = zipfile.ZipFile(filename)
		zfile.extractall(pwd=password)
		return True
	except:
		return False

zc = zippycrack.zippycrack(try_deflate,pwlist,numthreads=thr,cont=True)
print zc.run()
