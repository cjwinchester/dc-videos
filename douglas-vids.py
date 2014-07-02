from mechanize import Browser
from bs4 import *
import re

mech = Browser()

mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

mech.set_handle_robots(False)

baseurl = "http://www.douglascounty-ne.gov/board-meetings/videos"

page = mech.open(baseurl)
html = page.read()
soup = BeautifulSoup(html)

vidlinks = []

lastlink = soup.find(title="End")['href']

m = re.search('start=(\d+)', lastlink)
lastnum = int(m.group(0).replace('start=',''))

def num_padder(x):
    if len(str(x)) == 1:
        return "0" + str(x)
    else:
        return str(x)

months = {'July': 'jul', 'June': 'jun', 'May': 'may', 'April': 'apr', 'March': 'mar', 'February': 'feb', 'January': 'jan', 'December': 'dec', 'November': 'nov', 'October': 'oct', 'September': 'sep', 'Sept': 'sep', 'August': 'aug' }
        
counter = 0

f = open('list.txt', 'wb')

while counter <= lastnum:
    url = baseurl + '?start=' + str(counter)
    page = mech.open(url)
    html = page.read()
    print 'reading page ' + str(counter)
    soup = BeautifulSoup(html)
    heds = soup.findAll('h2', {'class': 'contentheading'})
    for thing in heds:
        date = thing.text.strip()
        month = num_padder(date.split(" ")[0])
        day = num_padder(date.split(" ")[1].replace(",",""))
        year = date.split(" ")[2]
        link = months[month] + day + "-" + year[-2:] + '.flv'
        url = 'http://www.douglascounty-ne.gov/images/stories/videos/' + link
        print url
        f.write(url + '\n')
    counter = counter + 9
   
f.flush()
f.close()