# import libraries
import urllib2
from bs4 import BeautifulSoup
import csv

# specify the url
round_1_page = 'http://www.volleyball.world/en/vnl/men/resultsandranking/round1'

#query the website and return the html
page = urllib2.urlopen(round_1_page)

# parse the html using beautifulsoup
soup = BeautifulSoup(page, 'html.parser')

# countries = []
# for i in range(0, 16):
#     id = 'wcbody_0_wcgridpad781180e1c6f34a88b89e0ca072c046b8_1_wcmenucontent_0_PoolsBox_Pools_PoolsBox_0_ctl00_0_Ranks_0_Link2_' + str(i)
#     country_tag = soup.find('a', attrs={'id':id})
#     rank_tag =  country_tag.parent.parent.parent.previous_sibling.previous_sibling
#     games_tag = rank_tag.next_sibling.next_sibling.next_sibling.next_sibling
#     wins_tag = games_tag.next_sibling.next_sibling
#     losses_tag = wins_tag.next_sibling.next_sibling

matches = []
for i in range(0,119):
    id = 'wcbody_0_wcgridpad781180e1c6f34a88b89e0ca072c046b8_1_wcmenucontent_0_PoolsBox_Pools_PoolsBox_0_ctl01_0_Results_0_MatchRow_' + str(i)
    tag = soup.find('tr', attrs={'id':id})
    date = tag.find_next('td', 'table-td-light')
    country_tag1 = tag.find_next('span', 'score')
    country_tag2 = country_tag1.find_next('span', 'score')
    score_tag1 = country_tag2.find_next('span', 'score')
    score_tag2 = score_tag1.find_next('span', 'score')
    tup = ()
    if (score_tag1.text > score_tag2.text):
        tup = (date.text.strip(), country_tag1.text.strip(), country_tag2.text.strip(), score_tag1.text.strip(), score_tag2.text.strip())
    else:
        tup = (date.text.strip(), country_tag2.text.strip(), country_tag1.text.strip(), score_tag2.text.strip(), score_tag1.text.strip())
    matches.append(tup)

with open('match_data.csv', 'wb') as out:
    writer = csv.writer(out)
    writer.writerow(['date', 'win_country', 'loss_country', 'win_score', 'loss_score'])
    for row in matches:
        writer.writerow(row)
