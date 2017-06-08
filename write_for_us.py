#list of keywords to search for
#open all results for x number of pages in SERPs
#store website name, url in a csv
#email results to user

#-- To do --#

#get group of 4 target keywords from user
#pass domains into Google using 'site:' search operand
#scrape number of indexed pages for that domain and save
#pass domain plus users target keywords to Google as above 
#save above number of indexed pages also

#scrape domains title & meta description
#strip out all 'http' etc
#construct a relevancy ratio for keywords & indexed pages


from bs4 import BeautifulSoup
import requests, argparse, csv, urllib
from urlparse import urlparse
import smtplib

import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders
from email.message import Message 
from collections import Counter

sender = None
receiver = None
text = None

def send_mail(sender, receiver, text):

	#create email message and send

	sender = 'splashpressmedia@gmail.com'
	receiver = 'dave.splashpress@gmail.com'
	subject = 'Your file is attached'

	msg = MIMEMultipart()

	msg['From'] = sender
	msg['To'] = receiver
	msg['Subject'] = subject
	body = 'Please see the file attached'


	filename = 'outreach_sites.csv'

	part = MIMEBase('application', 'octet-stream')
	part.set_payload(open('outreach_sites.csv', 'rb').read())
	Encoders.encode_base64(part)

	part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)

	msg.attach(part)
	text = msg.as_string()

	
	server = smtplib.SMTP('smtp.gmail.com', 587)
	with open('keys.txt', 'r') as fp:
		pwrd = fp.read().strip()
	server.ehlo()
	server.starttls()
	server.login('splashpressmedia@gmail.com', pwrd)
	server.sendmail(sender, receiver, text)
	server.close()


def get_serps(resp,counter, url_str, keywords):

	counter = 0

	#Counter goes up to 6 so a max of 59 search results or first 5 pages
	#set to 1 for testing purposes
	while counter != 1:

		#for results 11 onwards the search url must be altered
		if counter >= 1:
			resp = requests.get(url_str+'&start='+str(counter)+'0')
			

		#set Beautidul Soup object for search results content
		bsoup = BeautifulSoup(resp.text, "lxml")

		#find all the outbound urls from the results 
		for link in bsoup.find_all('a'):
			initial_urls.append(link.get('href'))

		#Create a list to store urls in
		parsed_urls = []	

		#remove unwanted characters from urls
		for i in initial_urls:
			if i[0:6] =='/url?q':

				parsed_urls.append(i)

		#remove the Google cached url from results
		for p_url in parsed_urls:
			if 'webcache' in p_url:
				parsed_urls.remove(p_url)


		#Strip out other unwanted characters to get the final urls

		for i in parsed_urls:
			head, sep, tail = i.partition('&sa=')
			final_urls.append(head.lstrip('/url?q='))

		counter += 1

	domains = []

	#use urlparse to get the domains from the final url results
	for i in final_urls:
		x = urlparse(i)
		y = (x.netloc)	
		domains.append(y)
		
	to_file(final_urls, domains)



def to_file(final_urls, domains):

	print 'Saving to file'

	urls = final_urls

	#create a dictionary of the domains and the write for us urls
	mydict = dict(zip(urls, domains))

	#print statement to check the urls are in the dict
	#print(mydict)


	#save to csv file
	fp = open('outreach_sites.csv', 'wb')
	writer = csv.writer(fp, delimiter=',')
	for k,v in mydict.items():
		print k,v
		writer.writerow([k,v])
	fp.close()

	#print('Successfully saved to file')
	#print('Sending mail')

	#send the email

	
	try:
		send_mail(sender, receiver, text)
		print 'Mail sent'
	except smtplib.SMTPException:
		'Unable to send mail, please try again later'
		import traceback
		traceback.print_exc()
	


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('target_keywords', nargs='+', help='enter your other target keywords')
	args = parser.parse_args()

	#create variables for requests and arparse to use
	search_engine = 'http://www.google.co.uk/search?hl=en&q='
	keywords = args.target_keywords
	write_us = '%20write%20for%20us'
	url_str = search_engine+write_us
	counter = 0

	resp = requests.get(url_str)

	get_serps(resp, counter, url_str, keywords)
	#check_metas()
	#to_file()


if __name__ == "__main__":
	initial_urls = []
	parsed_urls = []
	final_urls = []
	main()


	
	





		



