import requests
import time
import smtplib 

#get status codes
#if any != 200 send email
#if any != 200 send slack alert

#server access
	#check service status of httpd, mysql, php
	#check cpu load, ram, disk space


def send_mail(msg):

	sender = 'splashpressmedia@gmail.com'
	receiver = 'dave.splashpress@gmail.com'
	server = smtplib.SMTP('smtp.gmail.com', 587)
	#get the Gmail password from a separate file
	with open('keys.txt') as f:
		pwrd = f.read().strip() 
	server.starttls()
	server.ehlo()
	server.login('splashpressmedia@gmail.com', pwrd)
	server.sendmail(sender, receiver, msg)
	server.set_debuglevel(1)
	server.quit()



sites=['901am.com',
'audival.net',
'beblogging.com',
'bfeedme.com', 'codego.co']

sites_errors=[]

def parse_sites():

	for site in sites:
		if site[0:7] != 'http://':
			site = 'http://' + site
			print(site)
			try:
				r = requests.get(site)
				print(site, 'status code is: ', r.status_code)
				if r.status_code != 200:
					site_down =(site, r.status_code)
					sites_errors.append(site_down)
				time.sleep(3)
			except requests.exceptions.RequestException as e: 
				print(e)
				continue

		else:
			print(site)
			r = requests.get(site)
			print(site, 'status code is: ', r.status_code)
			if r != 200:
				site_down =(site, r.status_code)
				sites_errors.append(site_down)
			time.sleep(3)

	print(sites_errors)
	return sites_errors

def send_mail(sites_errors):

	subject = 'Site errors report'

	msg_text = 'The following sites have errors or are currently down: %r\n' %(sites_errors) 

	msg = 'Subject: %s\n\n%s' % (subject, msg_text)	

	try:
		send_mail(msg)
	except SMTPException:
		print('Sorry unable to send mail right now')

parse_sites()

















