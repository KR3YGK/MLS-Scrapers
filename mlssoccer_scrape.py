# Note - this code must run in Python 2.x and you must download
# http://www.pythonlearn.com/code/BeautifulSoup.py
# Into the same folder as this program

import urllib
import re
import csv
import os

from BeautifulSoup import *

#enter difference site if want different year
url = raw_input('Enter MLS Schedule Site to Scrape - ')
if len(url) < 1 : url = "http://www.mlssoccer.com/schedule?month=all&year=2013&club=select&club_options=9&op=Update&form_build_id=form-pQu0jXvZXgTb2mTvMtNk-qacP9KN1JXFrpBjeTMH0qo&form_id=mp7_schedule_hub_search_filters_form"

#Filename chosen here. Change for other years.  Overwrite if it already exists.
if os.path.exists('mls2013.csv'):
    os.remove('mls2013.csv')

html = urllib.urlopen(url).read()

links=[]
#gets all the links for every regular season game.  Change if year changed.
hrefs=re.findall('href="(http://matchcenter.mlssoccer.com/matchcenter/2013.*?)"',html)
for h in hrefs:
    #adds '/boxscore' to end of href 
    boxscore=h+"/boxscore"
    link=[boxscore]
    #links now a list of all boxscore hrefs for season
    links=links+link
   
#iteration number       
i=0
for link in links:
    i=i+1
    html = urllib.urlopen(link).read()    
    soup = BeautifulSoup(html)
    date=soup.find('div',{"class":"sb-match-date"})
    
    home=soup.find('div',{'class':'sb-team sb-home'})
    home=home.find('span',{'class':'sb-club-name-full'})
    home=home.text
    
    away=soup.find('div',{'class':'sb-team sb-away'})
    away=away.find('span',{'class':'sb-club-name-full'})
    away=away.text
    
    try: date=date.text.encode('utf-8')
    except: date=""
    
    
    #tables with player stats
    table=soup.findAll('table',{ "class" : "ps-table" })
   
    
    with open('mls2014TEST.csv', 'a') as csvfile:
        tnum=0
        for t in table:
            tnum=tnum+1
        
            body=t.find('tbody')
            
            #get header from first table
            if tnum==1 and i==1: 
                head=t.find('thead')
                h=""
                
                #all the columns of header
                for c in head.findAll('td'):
                #convert the text in columns to unicode-8 so I can then convert to string.
                    h=h+","+c.text.encode('utf-8') 
                    
                h=str.split(h,",")
                h=h[1:]
                if tnum==1: h[0]='number'
                
                writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                #last 4 are for goalies.  Will need to rearrange their data to fit this.
                writer.writerow(['link']+['home']+['away']+['player_team']+['day']+['date']+h+['SV']+['P']+['CC']+['GA'])    
                
            
            #all the rows
            row=body.findAll('tr')
            playerdata=""
            player_team=""
        
        
            for r in row:
                playerdata=date
                
                if tnum==1: player_team=home
                if tnum==2: player_team=away
                if tnum==3: player_team=home
                if tnum==4: player_team=away
                
            #all the columns
                for c in r.findAll('td'):
                #convert the text in columns to unicode-8 so I can then convert to string.
                    playerdata=playerdata+","+c.text.encode('utf-8')
                
                #writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                playerdata=str.split(playerdata, ",")
                
                #these columns are diff variables for keepers move to right columns
                if playerdata[3]=="G":
                    ga=playerdata[6]
                    sv=playerdata[9]
                    p=playerdata[10]
                    cc=playerdata[11]
                    
                    playerdata[6]=""
                    playerdata[9]=""
                    playerdata[10]=""
                    playerdata[11]=""
                    
                    playerdata=playerdata+[sv]+[p]+[cc]+[ga]
                                        
                writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([link]+[home]+[away]+[player_team]+playerdata)
            
            