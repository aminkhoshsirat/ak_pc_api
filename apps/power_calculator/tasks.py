from celery import shared_task
from redis import Redis
from bs4 import BeautifulSoup
import requests
from time import sleep
import json


re = Redis(host='localhost', port=6379, db=0)


@shared_task()
def get_cpus():
    urls = [f'https://www.techpowerup.com/cpu-specs/?released={i}&mobile=No&server=No&sort=name' for i in
            range(2011, 2024)]

    cpus = []

    for url in urls:
        t = requests.get(url,
                         headers={
                             'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'},
                         timeout=100000).text
        soup = BeautifulSoup(t, 'html.parser')
        table = soup.find('table', class_='processors')
        for i in table.find_all('tr'):
            try:
                cpus.append({
                    'title': i.find_all('td')[0].get_text(strip=True),
                    'power': i.find_all('td')[7].get_text(strip=True),
                    'socket': i.find_all('td')[4].get_text(strip=True)
                })
            except:
                pass

        sleep(10)
    amd_socket = set({})
    intel_socket = set({})
    for i in cpus:
        b = i['socket'].replace("Socket", "").lstrip(" ")
        if b.isdigit():
            intel_socket.add(b)
        else:
            amd_socket.add(b)

    re.set('cpus', json.dumps(cpus))
    re.set('intel_socket', json.dumps(list(intel_socket)))
    re.set('amd_socket', json.dumps(list(amd_socket)))


