# import libraries
import urllib2
from bs4 import BeautifulSoup
import csv
import os

# specify the url
round_1_page = 'http://www.volleyball.world/en/vnl/men/resultsandranking/round1'
match_page = 'http://www.volleyball.world'

#query the website and return the html
page = urllib2.urlopen(round_1_page)

# parse the html using beautifulsoup
soup = BeautifulSoup(page, 'html.parser')

teams = []
for i in range(0, 16):
    id = 'wcbody_0_wcgridpad781180e1c6f34a88b89e0ca072c046b8_1_wcmenucontent_0_PoolsBox_Pools_PoolsBox_0_ctl00_0_Ranks_0_Link2_' + str(i)
    country_tag = soup.find('a', attrs={'id':id})
    rank_tag =  country_tag.parent.parent.parent.previous_sibling.previous_sibling
    games_tag = rank_tag.next_sibling.next_sibling.next_sibling.next_sibling
    wins_tag = games_tag.next_sibling.next_sibling
    losses_tag = wins_tag.next_sibling.next_sibling
    tup = (country_tag.text.strip(), rank_tag.text.strip(), wins_tag.text.strip(), losses_tag.text.strip())
    teams.append(tup)

os.remove('team_data.csv')
with open('team_data.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['country', 'rank', 'wins', 'losses'])
    for row in teams:
        writer.writerow(row)


matches = []
for i in range(0,120):
    id = 'wcbody_0_wcgridpad781180e1c6f34a88b89e0ca072c046b8_1_wcmenucontent_0_PoolsBox_Pools_PoolsBox_0_ctl01_0_Results_0_MatchRow_' + str(i)
    tag = soup.find('tr', attrs={'id':id})
    date = tag.find_next('td', 'table-td-light')
    country_tag1 = tag.find_next('span', 'score')
    country_tag2 = country_tag1.find_next('span', 'score')
    score_tag1 = country_tag2.find_next('span', 'score')
    score_tag2 = score_tag1.find_next('span', 'score')
    
    # link = tag['data-href']
    # temp = match_page + link[:-4] + 'match'
    # curr_match_page = urllib2.urlopen(match_page + link[:-4] + 'match')
    # match_soup = BeautifulSoup(curr_match_page, 'html.parser')

    tup = ()
    if (score_tag1.text > score_tag2.text):
        tup = (date.text.strip(), country_tag1.text.strip(), country_tag2.text.strip(), score_tag1.text.strip(), score_tag2.text.strip())
    elif (score_tag1.text < score_tag2.text):
        tup = (date.text.strip(), country_tag2.text.strip(), country_tag1.text.strip(), score_tag2.text.strip(), score_tag1.text.strip())
    matches.append(tup)

os.remove('match_data.csv')
with open('match_data.csv', 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['date', 'win_country', 'loss_country', 'win_score', 'loss_score'])
    for row in matches:
        writer.writerow(row)
