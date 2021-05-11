import sys
import time
import socket
import random
import argparse
import threading
from colorama import init
init()

parser = argparse.ArgumentParser()
parser.add_argument("host", action="store", help="Host to connect to")
parser.add_argument("-port", "-p", type=int, required=True, help="Which port to connect with")
parser.add_argument("-num", "-n", type=int, default=1000, help="Amount of times to probe the host")
parser.add_argument("-timeout", "-t", type=int, default=3000, help="How long we should try to connect for until it returns an error (MS)")
parser.add_argument("-sleep", "-s", type=int, default=1000, help="Delay until next TCP request (MS)")
parser.add_argument("-loop", "-l", default=False, action="store_true", help="Constantly pinging the host (Even if number specified)")
parser.add_argument("-ipv4", "-4", default=True, action="store_true", help="Uses IPv4")
parser.add_argument("-ipv6", "-6", default=False, action="store_true", help="Uses IPv6")

args = parser.parse_args()

args.timeout /= 1000
args.sleep /= 1000

def get_ip(host):
	try:
		if args.ipv6:
			return socket.getaddrinfo(host, None, socket.AF_INET6)[0][4][0]
		elif args.ipv4:
			return socket.getaddrinfo(host, None, socket.AF_INET)[0][4][0]
		else:
			return socket.gethostbyname(host)
	except socket.gaierror:
		sys.exit("Hosts IP address was not retrievable.")

host = get_ip(args.host)

def create_sock():
	if args.ipv6:
		sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		data = (host, args.port, 0, 0)
	elif args.ipv4:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		data = (host, args.port)

	return sock, data
			#This Script Was Made By: BLU3#7236 On Discord
i = 0

print("""\

    ____  __    __  __ ____
   / __ )/ /   / / / /__  /
  / __  / /   / / / / /_ < 
 / /_/ / /___/ /_/ /___/ / 
/_____/_____/\____//____/  
                           

                    """)

if args.host != host:
	print("Connecting to \033[93m{} ({}) on TCP \033[93m{}".format(args.host, host, args.port))
else:
	print("Connecting to \033[93m{} on TCP \033[93m{}".format(args.host, args.port))

class TCPPinger(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while True:
			try:
				sock, data = create_sock()

				sock.settimeout(args.timeout)

				start = time.time() * 1000
				
				resp = sock.connect_ex(data)

				now = int(time.time() * 1000 - start)

				if resp == 0:
					print("\033[39mConnected to \033[32m{} Port={} \033[39mTime=\033[32m{}ms \033[39mProtocol=\033[32mTCP".format(host, args.port, now))
					time.sleep(args.sleep)
				else:
					print("\033[31m{} Got Dropped By BLU3".format(host, args.port))
					time.sleep(args.sleep)

				sock.close()
			except socket.error:
				print("Socket failure...")
				time.sleep(args.sleep)

if __name__ == "__main__":
	pinger = TCPPinger()
	pinger.setDaemon(True)
	pinger.start()
	
	while i < args.num:
		try:
			if not args.loop: i += 1
			
			time.sleep(1)
		except KeyboardInterrupt:
			break