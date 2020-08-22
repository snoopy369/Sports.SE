
# coding: utf-8

# In[2]:


import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


# In[11]:


def parse_boxscore(box_str):
    response = urlopen('https://www.hockey-reference.com' + box_str)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    scoring_table = soup.find('table',id='scoring')
    
    scoreDict = {}
    up3Dict   = {}
    
    if scoring_table != None:
        for cell in scoring_table.find_all('td'):
            teams = cell.find_all(href=re.compile('teams'))
            if teams:
                for team in teams:
                    teamstr = team.string
                    if teamstr in scoreDict:
                        scoreDict[teamstr] += 1
                    else:
                        scoreDict[teamstr] = 1
                    if len(scoreDict) == 1:
                        if scoreDict[teamstr] >= 3:
                            up3Dict[teamstr] = 1
                    else:
                        for key,value in scoreDict.items():
                            if key != teamstr:
                                otherScore = value
                        if scoreDict[teamstr] - value >= 3:
                            up3Dict[teamstr] = 1

        winner = max(scoreDict, key=lambda key: scoreDict[key])
        loser  = min(scoreDict, key=lambda key: scoreDict[key])
        if (winner != loser) and (loser in up3Dict):
            print(up3Dict)
            print(winner)
            print(loser)
            
            return(1)
        else:
            return(0)
                


# In[13]:


# Change range to search a range of your choice - best to cut into chunks to not overwhelm the server
for year in range(1980,2000):
    try:
        print('Checking '+str(year)+':')
        response = urlopen('https://www.hockey-reference.com/playoffs/NHL_' + str(year) + '.html')
        html_doc = response.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        
        playoff_table = soup.find('table', id='all_playoffs')
        if playoff_table != None:
            for box_table in playoff_table.find_all('table'):
                for box_link in box_table.find_all('a'):
                    rc = parse_boxscore(box_link['href'])
                    if rc == 1:
                        print('Found one! ' + box_link['href'])
        
    except:
        print('Oops, year '+str(year)+' not found!')

