import requests
from bs4 import BeautifulSoup
import csv

key = input('Please enter the term :')
location = input('Please enter the location too : ')
url = 'https://www.yell.com/ucs/UcsSearchAction.do?scrambleSeed=1144416941&keywords={}&location={}&pageNum=2'.format(key, location)
headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

datas = []
count_page = 0
for page in range(1, 11):
    count_page+=1
    print('scraping page :', count_page)
    req = requests.get(url+str(page), headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.findAll('div', 'row businessCapsule--mainRow')
    for it in items:
        name = it.find('h2', 'businessCapsule--name').text
        try: address = ''.join(it.find('span', {'itemprop':'address'}).text.strip().split('\n'))
        except : address = ''
        try : website = it.find('a', {'rel' : 'nofollow noopener'})['href'].replace('http://', '').replace('www.', '').replace('https://', '').split('/')[0]
        except : website = ''
        telp = it.find('span', 'business--telephoneNumber').text
        image = it.find('div', 'col-sm-4 col-md-4 col-lg-5 businessCapsule--leftSide').find('img')['data-original']
        if 'http' not in image: image = 'https://www.yell.com{}'.format(image)
        datas.append([name, address,website,telp,image])

kepala = ['Name', 'Adress', 'Website', 'Phone Number', 'Image URL']
writer = csv.writer(open('results/{}_{}.csv'.format(key, location), 'w', newline=''))
writer.writerow(kepala)
for d in datas: writer.writerow(d)