import requests
from parsel import Selector
import re
from pprint import pprint
import csv


class Jiaozhen():
    def __init__(self):
        self.writer = ''

    def get_list(self, page=1):
        print(('正在处理第%s页' % page).center(70, '-'))
        url = 'https://vp.fact.qq.com/loadmore?artnum=0&page=' + str(page)
        resp = requests.get(url=url).json()
        content = resp['content']
        if not content:
            print('没有下一页了')
            return
        for data in content:
            id = data['id']
            image_url = data['coverrect']
            item = self.get_detail(id, image_url)
            print(item)
            self.writer.writerow(item)
        page += 1
        self.get_list(page)

    def get_detail(self, id, image_url):
        '''标题、全文链接、时间、图片链接、流传说法、查证要点、查证者、平台、来源、真伪'''
        url = 'https://vp.fact.qq.com/article?id=' + id
        resp = requests.get(url=url)
        sel = Selector(resp.text)
        item = {}
        item['全文链接'] = url
        item['标题'] = sel.xpath('//h1[@class="maintitle"]/text()').get('').strip()
        item['时间'] = re.findall('<span>时间 : (.*?)</span>', resp.text, re.S)[0].strip()
        item['流传说法'] = re.findall('originRumor = `(.*?)`', resp.text, re.S)[0].strip()
        item['查证要点'] = sel.xpath('string(//*[@class="check_content_points"])').get('').strip().replace('\n',
                                                                                                       '').replace('\r',
                                                                                                                   '').replace(
            '\t', '')
        item['查证者'] = sel.xpath('//*[@class="check_content_text check_content_writer"]/text()').get('').strip().replace(
            '查证者：', '')
        item['平台'] = sel.xpath('//*[@class="check_content_text check_content_writer"]/span/text()').get('').strip()
        item['来源'] = re.findall('>来源 : (.*?)<', resp.text, re.S)[0].strip()
        item['真伪'] = sel.xpath('string(//*[@class="mark_total"])').get('').strip()
        item['图片链接'] = image_url
        item['原文'] = sel.xpath('string(//*[@class="question text"])').get('').replace('\n', '').replace('\r',
                                                                                                        '').replace(
            '\t', '').replace(' ', '')
        item['原文图片链接'] = sel.xpath('//*[@class="question text"]//img/@src').getall()

        return item

    def main(self):
        with open('较真.csv', 'w', encoding='utf-8-sig', newline='') as f:
            fieldnames = ['标题', '时间', '流传说法', '查证要点', '查证者', '平台', '来源', '真伪', '全文链接', '图片链接', '原文', '原文图片链接']
            self.writer = csv.DictWriter(f, fieldnames=fieldnames)
            self.writer.writeheader()
            self.get_list()


if __name__ == '__main__':
    jiaozhen = Jiaozhen()
    jiaozhen.main()
