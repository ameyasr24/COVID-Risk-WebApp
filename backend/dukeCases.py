from bs4 import BeautifulSoup
import re
import requests

def getDukeStudentCases():
     tables = getTables()
     infRate = 0
     tableNum = 0
     for table in tables:
          if tableNum == 1: #student table 
               td_list = table.find_all("td")
               numTested = int(re.sub("[^0-9]", "", td_list[15].text.strip()))
               numPositive = int(re.sub("[^0-9]", "", td_list[16].text.strip()))
               print("Total tests Student: " + str(numTested))
               print("Positive tests Student: " + str(numPositive))
               print("Infection rate Student: {:0.4f}%".format(100*(numPositive/numTested)))
               infRate = numPositive/numTested
          tableNum += 1

     return [infRate, infRate*2]

def getDukeFacultyCases():
     tables = getTables()
     infRate = 0
     tableNum = 0
     for table in tables:
          if tableNum == 0: #faculty table 
               td_list = table.find_all("td")
               numTested = int(re.sub("[^0-9]", "", td_list[15].text.strip()))
               numPositive = int(re.sub("[^0-9]", "", td_list[16].text.strip()))
               print("Total tests Faculty: " + str(numTested))
               print("Positive tests Faculty: " + str(numPositive))
               print("Infection rate Faculty: {:0.4f}%".format(100*(numPositive/numTested)))
               infRate = numPositive/numTested
          tableNum += 1

     return [infRate, infRate*2]

def getDukeTotalCases():
     tables = getTables()
     infRate = 0
     tableNum = 0
     for table in tables:
          if tableNum == 2: #total
               td_list = table.find_all("td")
               numTested = int(re.sub("[^0-9]", "", td_list[1].text.strip()))
               numPositive = int(re.sub("[^0-9]", "", td_list[2].text.strip()))
               print("Total tests Faculty: " + str(numTested))
               print("Positive tests Faculty: " + str(numPositive))
               print("Infection rate Faculty: {:0.4f}%".format(100*(numPositive/numTested)))
               infRate = numPositive/numTested
          tableNum += 1

     return [infRate, infRate*2]

def getTables():
     # Scrape Duke's COVID Testing Tracker for data
     URL = 'https://coronavirus.duke.edu/covid-testing/'
     page = requests.get(URL)

     soup = BeautifulSoup(page.content, 'html.parser')
     tables = soup.findAll("table")

     print("Tests conducted at Duke this week")
     return tables


#getDukeFacultyCases()
#getDukeStudentCases()
#getDukeTotalCases()