## zippycrack: a library that speeds up custom password cracking scripts with concurrency

Have you ever wanted to run a custom password cracking script in python, but you don't have the time to make a nice threaded interface for it? Well, `zippycrack` is here to help. It simplifies the writing of concurrent password crackers that need custom python code.

Say you need to break open a zip file:

    import zipfile,zippycrack

    def try_deflate(password):
    	try:
    		zfile = zipfile.ZipFile('test.zip')
    		zfile.extractall(pwd=password)
    		return True
    	except:
    		return False

    zc = zippycrack.zippycrack(try_deflate,'passwords.txt',numthreads=32)
    zc.run()

And it's just that easy:

    $ python zipcracker.py
    Thread 17 found a match: brooklyn
    Exited thread 17

All the thread handling is done for you, leaving you to spend your precious time on writing the important parts of the code.

Note: this library is a work in progress.

Another note: I am not responsible for anyone using this library illegally.
