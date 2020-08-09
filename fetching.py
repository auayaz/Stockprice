import time
import re
import os
import numpy as np
from urllib.request import urlopen
import requests
import bs4
from bs4 import BeautifulSoup

class fetching():
	
	def __init__(self,delta_t,filename,googleticker):

		self.delta_t = delta_t
		self.filename = filename
		self.googleticker = googleticker
		self.falling = None


	def fetchGF(self):
		"""
		fetches the ticker price from google finance.
		"""

		url="http://www.google.com/finance?&q="
		txt=urlopen(url+self.googleticker).read()
		txt = urlopen("http://www.google.com").read()
		print (txt)
		
		k=re.search('id="ref_(.*?)">(.*?)<',txt)
		if k:
			tmp=k.group(2)
			q=tmp.replace(',','')

		else:

			q="Nothing found for: " + self.googleticker
		
		return q

	def fetchP5(self):

		#fetches the ticker price from plus500.no

		url="http://www.plus500.no/Instruments/"
		txt=urllib.urlopen(url+Plus500ticker).read()
		k=re.search('innskudd',txt)
		if k:
			tmp=k.group(1)
			q=tmp.replace(',','')
		else:
			q="Nothing found for: "+Plus500ticker
		return q


	def fetchyahoo(self):

		url = "https://finance.yahoo.com/quote/TSLA/"
		r = requests.get(url)
		soup = bs4.BeautifulSoup(r.text,'lxml')
		price = soup.find('div',{'class':"D(ib) Mend(20px)"}).find('span').text
		price = (price.replace(',', ''))
		price = float(price)
		return price

	def record_to_file(self,endtime):
		"""
		records the stock price to file for a time period 
		"""

		t = time.time()
		googleticker = self.googleticker
		outfile = open(self.filename,'w')
		statement = (time.time()-t) < endtime

		while statement:

			value = self.fetchGF()
			elapsed = time.time() - t

			#print value, elapsed
			outfile.write('%s    %g \n'%(elapsed,value))
			time.sleep(self.delta_t)
			statement = (time.time()-t) < endtime
	
		outfile.close()


	def real_time(self,window):
		"""
		real time fetching and analyzing
		"""

		t = time.time()
		googleticker = self.googleticker
		price = np.zeros(window)
		tid = np.zeros(window)

		for i in range(len(tid)):
			
			time.sleep(self.delta_t)
			price[i] = self.fetchyahoo()
			tid[i] = time.time() - t
			print(price[i], tid[i])
		
		while True:
			self.analyze_prices_live(price)		#Analyzing
			price,tid = self.rearrenge(price,tid)
			price[-1] = float(self.fetchGF())
			tid[-1] = time.time() - t
			time.sleep(self.delta_t)

	"""
	def analyze_prices_live(self,price):
				
		sudden_drop = abs(price[-1] - price[-2])		
		print 'We are falling!!?!?!?!?! %g'%(sudden_drop)
	"""
	def analyze_from_file(self):
		"""
		reads the stock price from a file. storing the information in two lists: value and time
		"""

		inputdata = open(self.filename,'r')
		lines = inputdata.readlines()
		value = []
		time = []
		for line in lines:
			words = line.split()
			price = float(words[0])
			t = float(words[1])
			value.append(price)
			time.append(t)
		inputdata.close()
		
		return value,time


def rearrenge(self,x,y):

		"""
		pushes all the elements down a noch, leaving x[-1] = x[-2]
		"""

		for i in range(len(x)-1):
			x[i] = x[i+1]
			y[i] = y[i+1]

		return x,y


def test_urllib():
	#Testing urllib

	import urllib2
	req = urllib2.Request('https://www.yr.no')

	response = urllib2.urlopen(req)
	the_page = response.read()


if __name__ == '__main__':
	
	ob = fetching(1,'test.txt','TSLA')
	ob.fetchyahoo()
	#ob.record_to_file(1)
	#ob.analyze_from_file()
	ob.real_time(window = 100)
	#test_urllib();