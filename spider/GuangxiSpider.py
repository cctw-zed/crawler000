# import re
# import time
# from urllib.parse import urljoin
# from ConnectToElasticSearch import ConnectToElasticSearch
#
# # import ConnectMongoDB
# import requests
# from bs4 import BeautifulSoup
#
#
# class GuangxiSpider(object):
#
#     def __init__(self):
#         self.connection = ConnectToElasticSearch()
#         self.headers = {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'Accept-Encoding': 'gzip, deflate',
#             'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
#             'Connection': 'keep-alive',
#             'Upgrade-Insecure-Requests': '1',
#             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
#         }
#         self.base_url = 'https://www.gxrd.gov.cn'
#
#     # 抓取url得到response
#     def crawl(self, url, seen):
#         seen.add(url)
#         response = requests.get(url,headers=self.headers)
#         if response.status_code == 200:
#             return response
#
#     # 解析网页中包含的所有url
#     def parse(self, response, unseen, seen):
#         soup = BeautifulSoup(response.text, 'lxml')
#         urls = soup.find_all('a', {"href": re.compile('^/html/*')})
#         # print(urls)
#         page_urls = set()
#         for url in urls:
#             # title = url.get_text()
#             full_url = urljoin(self.base_url, url['href'])
#             if re.match("/html/art*", url['href']):
#                 page_urls.add(full_url)
#             else:
#                 unseen.add(full_url)
#             # print(unseen)
#         page_urls.update(page_urls - seen)
#         print('--------------')
#         print(page_urls)
#         print('--------------')
#         unseen.update(unseen - seen)
#         return page_urls
#
#     def artParse(self, response, url):
#         soup = BeautifulSoup(response.text, 'lxml')
#         content = soup.find('meta', {"name":"description"})['content']
#         # time = soup.find('p', {"class":"text-center a_inf lh30"}).get_text().split("&nbsp")[1]
#         # print(time)
#         title = soup.find('h2').find('span').get_text()
#         site = '广西人大网'
#         res = {}
#         res['title'] = title
#         res['real_url'] = url
#         res['abstract'] = content
#         # res['time'] = time
#         res['site'] = site
#         return res
#
# if __name__ == '__main__':
#     Spider = GuangxiSpider()
#     unseen = set([Spider.base_url, ])
#     seen = set()
#
#     count, t1 = 1, time.time()
#
#     while len(unseen) != 0:
#         print('\nDistributed Crawling...')
#
#         responses = []
#         for url in unseen:
#             try:
#                 responses.append(Spider.crawl(url,seen))
#                 time.sleep(0.5)
#             except:
#                 continue
#
#         print('\nDistributed Parsing...')
#         for response in responses:
#             try:
#                 page_urls = Spider.parse(response, unseen, seen)
#                 # time.sleep(1)
#                 # print(page_urls)
#
#                 for url in page_urls:
#                     try:
#                         print(Spider.artParse(Spider.crawl(url, seen), url))
#                         time.sleep(0.3)
#                         count += 1
#                         print(count)
#                         # print(time.time() - t1)
#                     except:
#                         continue
#             except:
#                 continue
#
# print('Total time: %.1f s' % (time.time() - t1,))  # 53 s
