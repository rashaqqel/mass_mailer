import threading
import time

from components.mailer import Mailer
from components.manager import Manager
from components.reader import Reader
from shared.mail_server import MailServer
from shared.recipient import Recipient


class Program:

	reader: Reader
	manager: Manager
	mailer: Mailer
	limiter: threading.BoundedSemaphore
	time_limiter: threading.BoundedSemaphore
	mails_per_sec: int
	active: int
	finish: bool

	def __init__(self):
		self.reader = Reader()
		self.manager = Manager(self.reader.proxies, self.reader.mail_servers, self.reader.senders)
		self.mailer = Mailer(self.manager, self.reader.message)
		self.active = 0
		self.finish = False

	def acquire(self):
		self.limiter.acquire()
		if self.mails_per_sec > 0:
			self.time_limiter.acquire()
			self.active += 1

	def release(self):
		while not self.finish:
			if self.active > 0:
				self.active -= 1
				self.time_limiter.release()
			time.sleep(1)

	def send(self, recipient: Recipient):
		self.acquire()
		try:
			server: MailServer = self.manager.server()
			self.mailer.send_mail(server, recipient)
		except AssertionError as e:
			print('\n[!] %s ' % e)
			exit(1)
		finally:
			self.limiter.release()

	def check(self, server: MailServer):
		self.acquire()
		try:
			if not self.mailer.check_server(server):
				server.disable()
		finally:
			self.limiter.release()

	def main(self):

		# Read all configs
		self.reader.read()
		self.limiter = threading.BoundedSemaphore(self.reader.config.treads)
		self.mails_per_sec = self.reader.config.mails_per_second

		# Set up time limiter tread
		if self.mails_per_sec > 0:
			self.time_limiter = threading.BoundedSemaphore(self.mails_per_sec)
			thread = threading.Thread(target=self.release, args=[])
			thread.start()

		# Check if server are ok
		print("\n[ ] Scanning servers")
		tasks = []
		for server in self.manager.servers:
			if server.limit != 0:
				thread = threading.Thread(target=self.check, args=[server])
				thread.start()
				tasks.append(thread)

		while len(tasks) > 0:
			tasks.pop().join()

		print("\n[✓] server list scan finished")

		# Send emails
		print("\n[ ] Sending emails")
		for recipient in self.reader.recipients:
			thread = threading.Thread(target=self.send, args=[recipient])
			thread.start()
			tasks.append(thread)

		while len(tasks) > 0:
			tasks.pop().join()

		self.finish = True
		print("\n[✓] mail delivery finished")


Program().main()
