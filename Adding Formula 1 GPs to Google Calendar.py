
# coding: utf-8

# ### Adding Formula 1 GPs to Google Calendar
# 
# -WARNING - Some country/city names will be in portuguese and the GP time are in the Brasilia time zone(BRT = GMT-3)
# <br>
# <br>
# The reason behind this project is that Google Calendar has a feature that automatically adds sporting events to your calendar, but formula 1 isn´t on the list, so the idea is to make a code that can add these events to your calendar. I will also be adding other motorsports events like Formula 2, Formula 3, Formula E and Formula Renault Eurocup
# <br>
# <br>
# The data from this project will be scraped from different webpages, the information that is being searched is the GP and it´s respective date, for some cases the hour has already being scheduled so it will also be added.
# <br>
# <br>
# Google has made avaiable the Calendar API, so you will also need to have it installed in your system for the code to work.

# In[2]:


#imporing the packages that will be used

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime


# In[8]:


#formula 1

#scraping the site for the gp/date/hour

url="https://globoesporte.globo.com/motor/formula-1/noticia/calendario-da-formula-1-em-2019.ghtml"
html=urlopen(url)
soup=BeautifulSoup(html,"html.parser")

#dictionary to translate the months from portuguese to english
months={"março":"March","abril":"April","maio":"May","junho":"June","julho":"July","agosto":"August",
        "setembro":"September","outubro":"October","novembro":"November","dezembro":"December"}

df=[]
table=soup.find("table",class_="show-table__content")
table=table.find_all("tr")

#the table in the site will be cleaned from undesireble letters and spaces
#the for using the months dictionary is used to translate the months into english

for item in table:
    cell=item.find_all("td")
    date=cell[0].get_text().lower().replace("º","").strip()
    for month in months:
            date=date.replace(month,months[month]).replace(" de "," ")
    gp=cell[1].get_text().title()
    hour=cell[3].get_text()
    df.append([date,gp,hour])
df=pd.DataFrame(df,columns=["date","circuit","hour"])

#the first row is the columns labels

formula1=df[1:]

#the dates and hours will be transformed in datetime objects

dates=[]
for item in formula1["date"]:
        date=datetime.datetime.strptime(item,"%d %B")
        value=datetime.datetime(day=date.day,month=date.month,year=2019).date()
        dates.append(value)
formula1["date"]=dates

hours=[]
for item in formula1["hour"]:
    hour=datetime.datetime.strptime(item,"%Hh%M")
    value=hour.time()
    hours.append(value)

formula1["hour"]=hours


# In[10]:


#formula 2

#scraping the site for the gp/date
#formula 2 GPs happen in two consecutive dates, so both of them will be considered
#the dates will be transformed into datetime objects

url="https://en.wikipedia.org/wiki/2019_FIA_Formula_2_Championship"
html=urlopen(url)
soup=BeautifulSoup(html,"html.parser")

data=[]
table=soup.find("table",style="font-size:85%;")
for row in table.find_all("tr"):
    cells=row.find_all("td")
    try:
        country=row.find("span",class_="flagicon").a.get("title")
    except AttributeError:
        pass
    if len(cells)==3:
        date1=cells[1].find(text=True).replace("\n","")
        date1=datetime.datetime.strptime(date1,"%d %B")
        date1=datetime.datetime(day=date1.day,month=date1.month,year=2019).date()
        
        date2=cells[2].find(text=True).replace("\n","")
        date2=datetime.datetime.strptime(date2,"%d %B")
        date2=datetime.datetime(day=date2.day,month=date2.month,year=2019).date()
        
        data.append([country,date1,date2])
        
formula2=pd.DataFrame(data,columns=["circuit","date 1","date 2"])


# In[182]:


#formula 3

#scraping the site for the gp/date
#formula 3 GPs happen in two consecutive dates, so both of them will be considered
#the dates will be transformed into datetime objects

url="https://en.wikipedia.org/wiki/2019_FIA_Formula_3_Championship"
html=urlopen(url)
soup=BeautifulSoup(html,"html.parser")

data=[]
table=soup.find("table",style="font-size:85%;")

for row in table.find_all("tr"):
    cells=row.find_all("td")
    try:
        country=row.find("span",class_="flagicon").a.get("title")
    except AttributeError:
        pass
    if len(cells)==3:
        date1=cells[1].find(text=True).replace("\n","")
        date1=datetime.datetime.strptime(date1,"%d %B")
        date1=datetime.datetime(day=date1.day,month=date1.month,year=2019).date()
        
        date2=cells[2].find(text=True).replace("\n","")
        date2=datetime.datetime.strptime(date2,"%d %B")
        date2=datetime.datetime(day=date2.day,month=date2.month,year=2019).date()
        
        data.append([country,date1,date2])
        
formula3=pd.DataFrame(data,columns=["circuit","date 1","date 2"])


# In[14]:


#formula renault eurocup

#scraping the site for the gp/date
#formula Renault Eurocup GPs happen in two consecutive dates, so both of them will be considered
#the dates will be transformed into datetime objects

url="https://www.renaultsport.com/the-2019-formula-renault-eurocup-calendar-announced.html"
html=urlopen(url)
soup=BeautifulSoup(html,"html.parser")

text=soup.find_all("td")[7:]
df=[]

for i in range(0,10):
    if i==0:
        date=text[0].get_text()
        circuit=text[1]
    else:
        date=text[2*i].get_text()
        circuit=text[2*i+1].get_text()
    df.append([date,circuit]) 
    
formulare=pd.DataFrame(df,columns=["date 1","circuit"])

#creating the date 2 column
formulare["date 2"]=formulare["date 1"]

#fixing a bad formatted row
formulare["date 1"][formulare["date 1"]=="October"]="October 24-26"

#splitting the dates that are on the same cell

for i,item in enumerate(formulare["date 1"]):
    dates=formulare.loc[i,"date 1"].split("-")
    date1=dates[0]
    date2=date1.split(" ")[0]+" "+dates[1]
    formulare.loc[i,"date 1"]=date1
    formulare.loc[i,"date 2"]=date2
    
#fixing bad formatted cells

formulare["date 2"][formulare["date 2"]=="August September 1"]="September 1"
formulare["date 2"][formulare["date 2"]=="May June 2"]="June 2"

#transforming the dates into datetime objects

for i,item in enumerate(formulare["date 1"]):
    date1=datetime.datetime.strptime(formulare.loc[i,"date 1"],"%B %d")
    formulare.loc[i,"date 1"]=datetime.datetime(day=date1.day,month=date1.month,year=2019).date()+datetime.timedelta(days=1)
    date2=datetime.datetime.strptime(formulare.loc[i,"date 2"],"%B %d")
    formulare.loc[i,"date 2"]=datetime.datetime(day=date2.day,month=date2.month,year=2019).date()

#the TBA circuit was selected to be Yas Marina and the race in Red Bull ring was changed to Hockenheimring
    
formulare["circuit"][formulare["circuit"]=="TBA"]="Yas Marina,UAE"
formulare["circuit"][formulare["circuit"]=="Red Bull Ring, Austria"]="Hockenheimring, Germany"
formulare["date 1"][formulare["circuit"]=="Hockenheimring, Germany"]=datetime.datetime(day=5,month=10,year=2019)
formulare["date 2"][formulare["circuit"]=="Hockenheimring, Germany"]=datetime.datetime(day=6,month=10,year=2019)
formulare.loc[0,"circuit"]

#fixing the circuit names

circuits=[]
formulare["circuit"][0]=str(formulare["circuit"][0])
for item in formulare["circuit"]:
    for word in ["<td>","</td>","¹","²"]:
        item=item.replace(word,"")
    value=item.split(",")[-1]
    circuits.append(value)

formulare["circuit"]=circuits


# In[184]:


#adding the events to the calendar

#setting up the google calendar api

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server()
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('calendar', 'v3', credentials=creds)

#adding formula 1 to the calendar

#the if clause was created because Brazil adopts a different time zone during the summer time
#the datetime format has to be inputted as:
#year-month-day-hour-minute-second-timezone
#YYYY-MM-DDTHH:MM:SS±HH:MM

for i,item in enumerate(formula1["Data"]):
    i=i+1
    if i>18:
        event = {
          'summary': " Formula 1: "+formula1["GP"][i]+' GP',
          'start': {
            'dateTime': str(formula1["Data"][i])+"T"+str(formula1["Horario"][i])+"-02:00"
          },
          'end': {
            'dateTime': str(formula1["Data"][i])+"T"+str(formula1["Horario"][i])+"-02:00"
          },
        }
    else:
          event = {
          'summary': " Formula 1: "+formula1["GP"][i]+' GP',
          'start': {
            'dateTime': str(formula1["Data"][i])+"T"+str(formula1["Horario"][i])+"-03:00"
          },
          'end': {
            'dateTime': str(formula1["Data"][i])+"T"+str(formula1["Horario"][i])+"-03:00"
          },
        }
    event = service.events().insert(calendarId='primary', body=event).execute()

#adding formula 2 to the calendar

for i,item in enumerate(formula2["date 1"]):
    event = {
      'summary': " Formula 2: "+formula2["circuit"][i]+' GP',
      'start': {
        'dateTime': str(formula2["date 1"][i])+"T10:00:00-03:00"
      },
      'end': {
        'dateTime': str(formula2["date 2"][i])+"T10:00:00-03:00"
      },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()


#adding formula 3 to the calendar

for i,item in enumerate(formula3["date 1"]):
    event = {
      'summary': " Formula 3: "+formula3["circuit"][i]+' GP',
      'start': {
        'dateTime': str(formula3["date 1"][i])+"T10:00:00-03:00"
      },
      'end': {
        'dateTime': str(formula3["date 2"][i])+"T10:00:00-03:00"
      },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()

#adding formula renault eurocup to calendar

for i,item in enumerate(formulare["circuit"]):
    event = {
      'summary': " Formula Renault Eurocup: "+formulare["circuit"][i]+' GP',
      'start': {
        'dateTime': str(formulare["date1"][i])+"T00:00:00-03:00"
      },
      'end': {
        'dateTime': str(formulare["date2"][i])+"T00:00:00-03:00"
      },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
