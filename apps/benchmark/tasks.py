from celery import shared_task
import redis
import requests
from bs4 import BeautifulSoup
import json

r = redis.Redis(host='localhost', port=6379, db=0)


@shared_task
def cpu_scrapy_tasks():
    url = [
        {'category': 'platform', 'url': 'https://www.cpubenchmark.net/cross-platform.html'},
        {'category': 'gaming', 'url': 'https://www.cpubenchmark.net/top-gaming-cpus.html'},
        {'category': 'overclock', 'url': 'https://www.cpubenchmark.net/overclocked_cpus.html'},
        {'category': 'single-thread', 'url': 'https://www.cpubenchmark.net/singleThread.html'}
    ]

    for i in url:
        once = False
        category = i.get('category')
        if category in ['overclock', 'single-thread']:
            once = True
        details = []
        text = requests.get(i.get('url'), timeout=20).text
        soup = BeautifulSoup(text, 'html.parser').find('ul', class_='chartlist')
        if once:
            for i in soup.find_all('li')[::2]:
                details.append({'name': i.find('span', class_='prdname').get_text(strip=True),
                                'url': i.find('a').attrs['href'].split('?')[1],
                                'grade': i.find('span', class_='count').get_text(strip=True),
                                'rank': i.find('div').get_text(strip=True)})

            r.set(f'benchmark:cpu:{category}:once', json.dumps(details))

        else:
            details = []
            for i in soup.find_all('li', class_='platform-cpu'):
                details.append({'type': i.find('button', class_='buttonToggle').get_text(strip=True),
                                'name': i.find('span', class_='prdname').get_text(strip=True),
                                'url': i.find('a').attrs['href'].split('?')[1],
                                'grade': i.find('span', class_='count').get_text(strip=True),
                                'rank': i.find('div').get_text(strip=True)})
            r.set(f'benchmark:cpu:{category}:all', json.dumps(details))

            details = []
            for i in soup.find_all('li', class_='platform-cpu desktop'):
                details.append({'type': i.find('button', class_='buttonToggle').get_text(strip=True),
                                'name': i.find('span', class_='prdname').get_text(strip=True),
                                'url': i.find('a').attrs['href'].split('?')[1],
                                'grade': i.find('span', class_='count').get_text(strip=True),
                                'rank': i.find('div').get_text(strip=True)})

            r.set(f'benchmark:cpu:{category}:desktop', json.dumps(details))

            details = []
            for i in soup.find_all('li', class_='platform-cpu laptop'):
                details.append({'type': i.find('button', class_='buttonToggle').get_text(strip=True),
                                'name': i.find('span', class_='prdname').get_text(strip=True),
                                'url': i.find('a').attrs['href'].split('?')[1],
                                'grade': i.find('span', class_='count').get_text(strip=True),
                                'rank': i.find('div').get_text(strip=True)})

            r.set(f'benchmark:cpu:{category}:laptop', json.dumps(details))

    return 'cpu scrapy task success'


@shared_task
def gpu_scrapy_tasks():
    url = [
        {'category': 'g3d-mark', 'url': 'https://www.videocardbenchmark.net/high_end_gpus.html'},
        {'category': 'price-performance', 'url': 'https://www.videocardbenchmark.net/gpu_value.html'},
        {'category': 'direct-compute', 'url': 'https://www.videocardbenchmark.net/directCompute.html'},
        {'category': 'high-mid-range', 'url': 'https://www.videocardbenchmark.net/mid_range_gpus.html'},
        {'category': 'low-mid-range', 'url': 'https://www.videocardbenchmark.net/midlow_range_gpus.html'},
        {'category': 'low-end', 'url': 'https://www.videocardbenchmark.net/low_end_gpus.html'},
        {'category': 'common', 'url': 'https://www.videocardbenchmark.net/common_gpus.html'}
    ]

    for i in url:
        details = []
        text = requests.get(i.get('url'), timeout=20).text
        category = i.get('category')
        soup = BeautifulSoup(text, 'html.parser').find('ul', class_='chartlist')
        for i in soup.find_all('li'):
            details.append({'name': i.find('span', class_='prdname').get_text(strip=True),
                            'url': i.find('a').attrs['href'].split('?')[1],
                            'grade': i.find('span', class_='count').get_text(strip=True),
                            'rank': i.find('div').get_text(strip=True)})

        r.set(f'benchmark:gpu:{category}', json.dumps(details))

    return 'gpu scrapy task success'


@shared_task
def ram_scrapy_tasks():
    url = [
        {'category': 'ddr5', 'url': 'https://www.memorybenchmark.net/threaded_ddr5.html'},
        {'category': 'ddr4', 'url': 'https://www.memorybenchmark.net/threaded_ddr4.html'},
        {'category': 'ddr3', 'url': 'https://www.memorybenchmark.net/threaded_ddr3.html'},
        {'category': 'ddr5-read-transfer', 'url': 'https://www.memorybenchmark.net/read_uncached_ddr5.html'},
        {'category': 'ddr4-read-transfer', 'url': 'https://www.memorybenchmark.net/read_uncached_ddr4.html'},
        {'category': 'ddr3-read-transfer', 'url': 'https://www.memorybenchmark.net/read_uncached_ddr3.html'},
        {'category': 'ddr2-read-transfer', 'url': 'https://www.memorybenchmark.net/read_uncached_ddr2_all.html'},
        {'category': 'ddr5-write-transfer', 'url': 'https://www.memorybenchmark.net/write_ddr5.html'},
        {'category': 'ddr4-write-transfer', 'url': 'https://www.memorybenchmark.net/write_ddr4.html'},
        {'category': 'ddr3-write-transfer', 'url': 'https://www.memorybenchmark.net/write_ddr3.html'},
        {'category': 'ddr2-write-transfer', 'url': 'https://www.memorybenchmark.net/write_ddr2_all.html'},
        {'category': 'ddr5-memory-latency', 'url': 'https://www.memorybenchmark.net/latency_ddr5.html'},
        {'category': 'ddr4-memory-latency', 'url': 'https://www.memorybenchmark.net/latency_ddr4.html'},
        {'category': 'ddr3-memory-latency', 'url': 'https://www.memorybenchmark.net/latency_ddr3.html'},
        {'category': 'ddr2-memory-latency', 'url': 'https://www.memorybenchmark.net/latency_ddr2_all.html'}
    ]

    for i in url:
        details = []
        text = requests.get(i.get('url'), timeout=20).text
        category = i.get('category')
        soup = BeautifulSoup(text, 'html.parser')
        soup = soup.find('div', {'class': 'chart_body'})
        for i in soup.find_all('li'):
            details.append({'name': i.find('span', {'class': 'prdname'}).get_text(),
                            'count': i.find('span', {'class': 'count'}).get_text(),
                            })

        r.set(f'benchmark:ram:{category}', json.dumps(details))

    return 'ram scrapy task success'


@shared_task
def disk_scrapy_tasks():
    url = [
        {'category': 'ssd', 'url': 'https://www.harddrivebenchmark.net/ssd.html'},
        {'category': 'disk-high', 'url': 'https://www.harddrivebenchmark.net/high_end_drives.html'},
        {'category': 'disk-high-mid-range', 'url': 'https://www.harddrivebenchmark.net/mid_range_drives.html'},
        {'category': 'disk-low-mid-range', 'url': 'https://www.harddrivebenchmark.net/low_mid_range_drives.html'},
        {'category': 'disk-low-end', 'url': 'https://www.harddrivebenchmark.net/low_end_drives.html'},
        {'category': 'sequential-read', 'url': 'https://www.harddrivebenchmark.net/sequential-read.html'},
        {'category': 'sequential-write', 'url': 'https://www.harddrivebenchmark.net/sequential-write.html'},
        {'category': 'random-seek-read-write', 'url': 'https://www.harddrivebenchmark.net/random-read-write.html'},
        {'category': 'common', 'url': 'https://www.harddrivebenchmark.net/common_drives.html'},
    ]

    for i in url:
        details = []
        text = requests.get(i.get('url'), timeout=20).text
        category = i.get('category')
        soup = BeautifulSoup(text, 'html.parser')
        soup = soup.find('div', {'class': 'chart_body'})
        for i in soup.find_all('li'):
            details.append({'name': i.find('span', {'class': 'prdname'}).get_text(),
                            'count': i.find('span', {'class': 'count'}).get_text(),
                            })

        r.set(f'benchmark:disk:{category}', json.dumps(details))

    return 'disk scrapy task success'



@shared_task
def pc_scrapy_tasks():
    url = [
        {'category': 'fastest-desktops', 'url': 'https://www.pcbenchmarks.net/fastest-desktop.html'},
        {'category': 'fastest-systems', 'url': 'https://www.pcbenchmarks.net/leaderboard.html'},
        {'category': 'fastest-laptops', 'url': 'https://www.pcbenchmarks.net/fastest-laptop.html'},
        {'category': 'fastest-server', 'url': 'https://www.pcbenchmarks.net/fastest-server.html'},
    ]

    for i in url:
        details = []
        text = requests.get(i.get('url'), timeout=20).text
        category = i.get('category')
        soup = BeautifulSoup(text, 'html.parser').find('ul', class_='chartlist')
        for i in soup.find_all('li'):
            details.append({'name': i.find('p', {'class': 'clmn-1'}).get_text(),
                            'count': i.find('span', {'class': 'count'}).get_text(),
                            'cpu': i.find('p', {'class': 'clmn-2'}).get_text(),
                            'main_board': i.find('span', {'class': ''}).get_text(),
                            'vga': i.find_all('td')[3].get_text(),
                            'ram': i.find_all('td')[7].get_text(),
                            'os': i.find_all('td')[11].get_text(),
                            })

    return 'pc scrapy task success'

