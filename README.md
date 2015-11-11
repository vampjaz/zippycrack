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

### Quick docs:

All the information is specified during initialization:

    zippycrack.zippycrack(func,
    	passfile,
    	numthreads=4,
    	cont=False,
    	mode=ROUND_ROBIN)

* **func**: the function called to evaluate if the password is correct. This should return `True` if the password is correct, `False` otherwise. The only parameter passed to it is the password to try.
* **passfile**: the file to read newline-separated passwords from.
* **numthreads**: number of threads to start. Default 4.
* **cont**: boolean value to continue looking if a password is found.
* **mode**: selects the mode of distribution of the passwords to each thread.


**Modes**:

`ROUND_ROBIN`: distributes passwords in a round-robin distribution:

    1    2    3    4
    5    6    7    8 ...

**currently unimplemented** `SEGMENTED`: segments the password file equally among threads:

    1   100  200  300
    2   101  201  301 ...

The actual work is done during the call to `run()`. This function will return a list of passwords found to be correct.

### Extended docs:

There is also an extended "mode" of operation, under `zippycrack.zippycrack_extended`, which will require more user side code, but is more powerful. Each thread instantiates its own class, which allows there to be persistent objects across all attempts in each thread.

To use simply substitute your custom class for the `func` variable during initialization. It needs to extend the `zippycrack.xdefault` class, with three optional functions overridden:

* `__init__(self,tid)` - called on initialization, `tid` is thread ID
* `run(self,pwd)` - called once per password, `pwd` is the password. as before, return `True` to indicate success
* `done(self)` - called on completion, use to clean up stuff

--------------

Note: this library is a work in progress.

Another note: I am not responsible for anyone using this library illegally.
