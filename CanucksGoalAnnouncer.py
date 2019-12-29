# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 10:04:13 2019

@author: Caleb Sample
"""

from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
import smtplib
import time
import math


gameOn = 1
initialTime = time.time()

while (gameOn == 1):
	
		#def GoalAnnouncer():
	#pass html in as string or file.
	
	source = requests.get('https://www.thescore.com/nhl/events').text
	
	webCode = BeautifulSoup(source,'lxml')
	
	divs=list(webCode.find_all('div',attrs={'class': 'col-xs-12 col-md-6'}))

	for i in range(len(divs)): #Find if a canucks game is today
		if ("VAN Canucks" in str(divs[i])):
			canucksDiv = divs[i]
		
		
		
	for div in canucksDiv.findAll('div',attrs={'class':'EventCard__clockColumn--3lEPz'}):		
		startTimeRaw = str(div.text)
	
	
	
	
	
	#Now find the position of the colon:
	colonIndex = startTimeRaw.find(':')
	gameOn = 1 #0 if the game is on. 1 if not.
	if ("PM" in startTimeRaw or "AM" in startTimeRaw):#colonIndex>0 and colonIndex<4):
		startHour = int(startTimeRaw[0:(colonIndex)])
		startHour -= 3
		startMin = int(startTimeRaw[colonIndex+1:colonIndex+3])
	else: 
		gameOn = 0 #the game has started	
	time.sleep(5)	
	
	#Get the current run time:
	runTime = time.time()-initialTime
	runtTime = math.floor(runTime/60)
	runTime = int(runTime)
	print('Game hasnt started yet. Been trying for ' + str(runTime) + ' seconds')
	
	
	
#Extract the start time: first get if Pm or am:
if ("PM" in startTimeRaw):
	startHour = startHour + 12 #add 12 if PM. subtract 3 for pacific time.
	


if (gameOn == 0):
	print('game on')
	#The program only needs to run while the game is on: so make sure its after start time, and less than 3 hours after.
	now = datetime.now()
	startingHour = now.hour
	finishHour = startingHour + 4 #Program runs for max 4 hours after game starts


#Now get the URL of the link:
linkString = str(canucksDiv.findAll('a'))[10:27]
linkString = 'https://www.thescore.com' + linkString

#Now fire up the game page:

source2 = requests.get(linkString).text
gameCode = BeautifulSoup(source2,'lxml')

#Need to check if someone scored:

goals = 0
currentGoals = 0

while (now.hour < finishHour):

	
	
	#find the canucks header
	teamNames1=list(gameCode.find_all('div',attrs={'class': 'Matchup__teamRow--1g_nG Matchup__separator--16XoG'}))#Matchup__teamName--vqpde'}))
	teamNames2=list(gameCode.find_all('div',attrs={'class': 'Matchup__teamRow--1g_nG'}))
	
	#for i in range(len(teamNames)): #Find the canucks row with score
	if ("VAN Canucks" in str(teamNames1)):
	
		
		for div in teamNames1[0].findAll('div',attrs={'class':'Matchup__teamScore--2BeCA'}):		
			currentGoals = str(div.text)	
			print('away')
			
	else:
		for div in teamNames2[1].findAll('div',attrs={'class':'Matchup__teamScore--2BeCA'}):		
			currentGoals = int(div.text)	
			print('Home')
	#Do something to check if number of goals has changed here:		
	if (currentGoals>goals):
		goals +=1
		
		#Message Sending function:
		#establish connection with gmail
		server = smtplib.SMTP('smtp.gmail.com',587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		
		server.login('pythonemailerguy@gmail.com','emjlzlppuwsncmwm')
		
		subject = 'CANUCKS GOAL!'
		body= 'GOAL SCORED\n     ' + linkString
		
		msg = f"Subject:{subject}\n\n{body}"
	
		server.sendmail(
			'pythonemailerguy',
			'csample@phas.ubc.ca',
			 msg
		 )
			    
		
		print('Email successfully sent')
		server.quit()
	time.sleep(60)	
						  
	  	
			
			
	
	
	
	
	
	
	

   
