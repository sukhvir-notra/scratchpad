import json
from io import open
from json2html import *
from colorama import init
from termcolor import colored
import time

init() #get the coloring module ready

with open('baselight_new2.txt','r',encoding='utf-16') as message:
	data = json.load(message)

print "Information for following hosts was retrieved:\n"+'-'*20+'\n'

for key in sorted(data.keys()):
	print key 

search="\n\nwhat do you want to search for?\n"+"="*30+"\n1. Show all data for a host\n2. Show data for specific key\n3. Search for a specific value\n4. Produce a HTML file\n\nYour choice: "

while True:
	try:
		choice=input(search)

		if choice==1:
			query=raw_input("\nEnter the IP you are looking for: ")
			for key in data.keys():
				if query in key:
					for k,v in sorted(data[key].iteritems()):
						print k + "\n" + "-"*len(k)
						print v

		elif choice==2:
			print "\nYou can choose to display data from one of the following keys:\n"
			index=next(iter(data))
			for k in sorted(data[index].keys()):
				print k

			key_choice=raw_input("\n\nWhich key would you like to see: ")

			if key_choice in data[index]:

				one_or_all=input("\nWould you like to see the data for this key for:\n1. Single host\n2. All hosts\n\nyour choice: ")

				if one_or_all==1:
					print "\nEnter the ip you would like to see the data from. Follwoing hosts are available:\n"
					for key in sorted(data.keys()):
						print key

					ip_choice=raw_input("\nYour choice: ")

					print data[ip_choice][key_choice]

				elif one_or_all==2:
					for key in sorted(data.keys()):
						print "-"*10+"\n"+data[key][key_choice]

				else:
					print "incorrect entry"
			else:
				print "incorrect entry"

		elif choice==3:
			query=raw_input("\nEnter the value you are looking for: ")
			for k in data.keys():
				for k1,v1 in data[k].iteritems():
					if query in v1:
						print "\n\nInformation found in " + k + '\n' + "-"*len(k)
						print '\n'+ k1 + '\n' + '='*len(k1)
						index=v1.find(query)				
						print v1[:index] + colored(query,'red', 'on_white') + v1[(index+len(query)):]

		elif choice==4:
			html = json2html.convert(data)

			html=html.replace('\r\n','<br>')
			html=html.replace('</th><td><br>','</th><td><br><pre>')
			html=html.replace('</td></tr>','</td></tr></pre>')

			appendage=""
			index=1
			for key in data.keys():
				rep='<table border="1"><tr><th>'+key
				repn='<table border="1"><tr><th><div id="'+key+'"></div>'+key
				html=html.replace(rep,repn)
				appendage=appendage+'<br><a href="#'+key+'">'+key+'</a><br>'
				#index
				for k in data[key].keys():
					rep=k
					repn='<div id="'+k+'-'+key+'"></div>'+k  
					appendage=appendage+'&emsp;&emsp;<a href="#'+k+'-'+key+'">'+k+'</a><br>'
					
					find=html.find(k)
					i = 0

					while find != -1 and i!=index:
						find=html.find(rep,find+1)
						i+=1

					if i==index:
						html=html[:find]+repn+html[find +len(k):]

				index+=1

			html='<pre>'+appendage+html+'</pre>'

			timestamp= time.strftime("%Y-%m-%d-%H%M")
			timestamp=timestamp+'.html'

			f=open(timestamp,"w")
			f.write(html)
			f.close()

			print "\n\n" + timestamp + " file created in current directory\n\n"
		else:
			print "\nChoose a number between 1 and 3"

	except KeyboardInterrupt:

		print "\n\nexiting .. Bye...\n\n"
		break