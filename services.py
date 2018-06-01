from paramiko import client

class ssh:
	client = None 

	def __init__(self, address, username, password):
		# Let the user know we're connecting to the server
		print("Connecting to server.")
		# Create a new SSH client
		self.client = client.SSHClient()
		# The following line is required if you want the script to be able to access a server that's not yet in the known_hosts file
		self.client.set_missing_host_key_policy(client.AutoAddPolicy())
		# Make the connection
		self.client.connect(address, username=username, password=password, look_for_keys=False)


	def sendCommand(self, command):
		#check if connection is made previously
		if(self.client):
			stdin, stdout, stderr = self.client.exec_command(command)
			while not stdout.channel.exit_status_ready():
				#print stdout data when available
				if stdout.channel.recv_ready():
					#get the first 1024 bytes
					alldata = stdout.channel.recv(1024)
					while stdout.channel.recv_ready():
						#retrieve the next 1024 bytes
						alldata += stdout.channel.recv(1024)

					#print as string with utf8 encoding
					print(str(alldata, "utf8"))
		else:
			print('Connection not opened')

connection = ssh("192.168.1.43", "david", "password")

connection.sendCommand("ls")