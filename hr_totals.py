import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup


#Get the number of career HRs from a player's page
def hr_tot(player_str):
    response = urlopen('https://www.baseball-reference.com' + player_str)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    

    table = soup.find('table',id='batting_standard')  # has to be 'batting_standard', and only batters hve that uncommented
    if table != None:
        table_tfoot = table.find_all('tfoot')

        hr_tot=0
        for tfoot in table_tfoot:
            td = tfoot.find_all('td')
            for t in td:
                if t['data-stat'] == 'HR' and t.text != '':
                    return(t.text)

            
#For a particular team/year combination (defined in team_str), find the maximum number of career HRs one of its starting lineups had

def find_hr_max(team_str):
    response = urlopen(team_str)
    html_doc = response.read()

    # Parse the html file
    soup = BeautifulSoup(html_doc, 'html.parser')

    table = soup.table
    table_rows = table.find_all('tr')


    lineups_tot = []
    
    for tr in table_rows:
        td = tr.find_all('td')
        if len(td) > 0:
            #This is try/except because there are a few more TRs after the relevant ones that do not have anchor links in them
            try:
                lineup={}
                lineup_hr_tot=0
                
                linklist = [i.a['href'] for i in td]
                for player in linklist:           
                    #Only look up the player if we have not looked him up before - this is the most expensive part!
                    if not player in players_list:
                        players_list.append(player)
                        hr_dict[player] = hr_tot(player)
                    #Try/except because the pitchers will not have entries generally due to BBREF's weirdness
                    try:
                        lineup_hr_tot = lineup_hr_tot + int(hr_dict[player])
                    except:
                        pass
                    lineup['game'] = tr.th.text
                    lineup['hr_tot'] = lineup_hr_tot
                    lineups_tot.append(lineup)
            except:
                pass
 

    max_hr = 0
    for index, lineup in enumerate(lineups_tot):
        if lineup['hr_tot'] > max_hr:
            max_index = index
            max_hr = lineup['hr_tot']

    return( lineups_tot[max_index])
    

#This runs all of the totals for a single year
#Starts by grabbing the MLB year page for that year, to get an iterable with the different teams that were in the league that year
#Then calls find_hr_max for each of those team/years
def get_year_tots(year):
    response = urlopen('https://www.baseball-reference.com/leagues/MLB/' + year + '.shtml')
    html_doc = response.read()

    # Parse the html file
    soup = BeautifulSoup(html_doc, 'html.parser')

    table = soup.table
    table_rows = table.find_all('tr')

    year_tots = {}

    for tr in table_rows:
        a=tr.th.a
        if a != None:
            year_tots[a.text] = find_hr_max('https://www.baseball-reference.com/teams/' + a.text + '/' + year + '-batting-orders.shtml')
            
    return(year_tots)
            
    
  
#Only do this initialization once!!  Even if we have to rerun years, we do not want to reinitialize these if we can avoid it
#As creating these is very expensive
players_list = []
hr_dict={}    

    
#Now, actually call the get_year_tots for each year we want
#This seems to only work for 1969-present, have not worked out what differences 1968-earlier have that make it not work on them
years = {}
for year in range(1969,2020):
    years[str(year)] = get_year_tots(str(year))
    
    

# Everything after this is just different ways to look at the years list of dicts of dicts...

# First, just get the max result

max_hr = 0;
for year in range(1969,2020):
    for key,teamdict in years[str(year)].items():        
        if teamdict['hr_tot'] > max_hr :
            max_hr = max(max_hr,teamdict['hr_tot'])
            max_game = teamdict['game']
            max_team = key
            max_year = year
        


print(max_hr,max_game, max_team, max_year)

# Second, we will reorganize this into a list of dicts (single) so we can make it a pd dataframe:

list_years = []

for year in range (1969,2020):
    for key, teamdict in years [str(year)].items():
        teamdict['year'] = year        
        teamdict['team'] = key
        list_years.append(teamdict)
    
    
print(list_years)

import pandas as pd

pd_frame = pd.DataFrame(list_years)

pd_frame.sort_values(by='hr_tot',ascending=False)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  
    print(pd_frame.sort_values(by='hr_tot',ascending=False))
