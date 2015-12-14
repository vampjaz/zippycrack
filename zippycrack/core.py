from multiprocessing import Process, Queue
import sys

## constants
ROUND_ROBIN = 1
SEGMENTED = 2
EXIT_ = 77777 # idk... this is for exiting the thread; will never be a number

## passcrack class
class zippycrack:
	def __init__(self,func,passfile,numthreads=4,cont=False,mode=ROUND_ROBIN):
		# func to run to check, file uri line separated, num threads, boolean to continue if found a correct, mode to distribute passwords
		self.func = func
		self.passfile = passfile
		self.numthreads = numthreads
		self.cont = cont
		self.mode = mode
		self.printqueue = Queue()

	def worker_thread(self,queue,tid):
		r = True
		while r:
			pwd = queue.get()
			if pwd == EXIT_:
				r = False
				break
			ret = self.func(pwd) ## func must return a boolean if correct
			if ret:
				self.printqueue.put("Thread {} found a match: {}".format(tid,pwd))
				if not self.cont:
					## TODO: exit all threads
					r = False
			#queue.task_done()  ## apparently not in multiprocessing
		self.printqueue.put("_EXIT_ "+str(tid))

	def run(self):
		self.threads = []
		self.queues = []
		for i in range(self.numthreads):
			nq = Queue()
			self.queues.append(nq)
			th = Process(target=self.worker_thread,args=(self.queues[i],i))
			th.start()

		pfile = open(self.passfile,'r')
		if self.mode == ROUND_ROBIN:
			current = 0
			for i in pfile.readlines():
				pwd = i.strip()
				self.queues[current].put(pwd)
				current += 1
				if current >= self.numthreads:
					current = 0
		for q in self.queues: #
			q.put(EXIT_)
		## now wait for the print queues to populate:
		runningt = [True]*self.numthreads
		passes = []
		while True in runningt:
			n = self.printqueue.get()
			if '_EXIT_' in n:
				print "Exited thread {}".format(n.split()[-1])
				runningt[int(n.split()[-1])] = False  ## idk if this is the best way to do this..
				if not self.cont:
					sys.exit()
			else:
				if "match: " in n:
					passes.append(n.split('match: ',1)[-1])
				print n
		print "Done"
		return passes
