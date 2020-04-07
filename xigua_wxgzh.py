# -*- coding: utf-8 -*-
import csv
import os
import sys
import time
import requests
from fake_useragent import UserAgent
from lxml import html
from constants import proxy_url, detail_header

ua = UserAgent(verify_ssl=False)

etree = html.etree
proxy = {}

web_header = {
    'Host': 'zs.xiguaji.com',
    'cookie': 'ASP.NET_SessionId=a5fafnzutqbxq5nzhrvyalzc; _chl=key=BaiduOrginal; Hm_lvt_4137765507ebdf7b7a8bcfa91a9d08a4=1584320603; Qs_lvt_4671=1584320603; LoginTag=523ee08266b24fb5be22fb6dfb46f72f; _XIGUASTATE=XIGUASTATEID=12d1731d9b7a46c78506399564f0bd82; LogFlag=Login; _XIGUA=UserId=dab41783797b5d79&Account=07565d5e3f5bb33c&checksum=7fc8c6223d3d; LV2=1; Hm_lpvt_4137765507ebdf7b7a8bcfa91a9d08a4=1584320916; Qs_pv_4671=800788270337625700%2C2103339657472171800%2C2480861286840429600%2C4084783478806142500%2C1036833726433647200; ShowOneKeyAsyncTip2=1',
    'Referer': 'https://zs.xiguaji.com/Member',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'
}


def change_proxy(retry_count):
    if retry_count < 0:
        return

    result = requests.get(proxy_url).json()
    if result['msg'] == 'ok':
        ip = result['obj'][0]['ip']
        port = result['obj'][0]['port']
        proxies = {"http": "http://" + ip + ":" + port, "https": "http://" + ip + ":" + port}
        global proxy
        proxy = proxies
        print(f"代理ip为更改为：{proxies}")
        return proxies
    else:
        time.sleep(1)
        print('切换代理失败，重新尝试。。。')
        change_proxy(retry_count - 1)


def spider(page):
    need_list = []

    ret = requests.get(url='https://zs.xiguaji.com/MArticle/Attention/?order=-1&readCompare=-1&fans=-1&position=2&dayInterval=100&articleType=-1&IsAttentionMain=1&tags=24456&onlyTopLine=&page={}&more=1'.format(page), headers=web_header).content.decode()
    time.sleep(1)
    root = etree.HTML(ret)
    tr_list = root.xpath("//tr")
    for tr in tr_list:
        spread_index = tr.xpath("./td[1]/span/text()")[0]
        title = tr.xpath(".//div[@class='mp-article-title']/a/text()")[0]
        url = tr.xpath(".//div[@class='mp-article-title']/a/@href")[0]
        article_date = tr.xpath(".//div[@class='item-sub-title']/text()")[0]
        read = tr.xpath("./td[6]/text()")[0]
        reading = tr.xpath("./td[7]/text()")[0]

        # 详情页数据
        def get_data(count):
            if count < 0:
                return
            try:
                detail_res = requests.get(url=url, headers=detail_header, proxies=proxy,
                                          timeout=(3, 7)).content.decode()
                # time.sleep(0.5)
            except:
                change_proxy(3)
                return get_data(count - 1)
            if '访问过于频繁' in detail_res:
                change_proxy(3)
                return get_data(count - 1)
            return detail_res

        detail_res = get_data(3)

        # time.sleep(random.uniform(0, 0.3))

        root_detail_res = etree.HTML(detail_res)
        article_author = root_detail_res.xpath("//span[@class='rich_media_meta rich_media_meta_text']/text()")[0] if \
            root_detail_res.xpath("//span[@class='rich_media_meta rich_media_meta_text']/text()") else ''
        article_author = article_author.replace(' ', '').replace('\n', '')  # 作者
        article_content = root_detail_res.xpath("string(//div[@class='rich_media_content '])").replace(' ',
                                                                                                       '')  # 文章内容
        if article_content == '' or article_content is None:
            is_have = 0
        else:
            is_have = 1

        article_img_url = root_detail_res.xpath("//div[@class='rich_media_content ']//img/@data-src")
        article_img_url = '\n'.join(article_img_url)  # 图片链接
        article_video_url = root_detail_res.xpath("//iframe/@data-src")
        article_video_url = '\n'.join(article_video_url)  # 视频链接

        need = [article_date, title, read, reading, spread_index, url, article_content, article_img_url, article_video_url]
        print(need)

        need_list.append(need)
    return need_list


def get_path(file_name):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name)
    return path


def save_data(filename, data):
    # now = datetime.datetime.now().replace()
    # now = str(now)[0:10].replace('-', '').replace(' ', '').replace(':', '')
    path = get_path(filename + '.csv')
    if os.path.isfile(path):
        is_exist = True
    else:
        is_exist = False
    with open(path, "a", newline="", encoding="utf_8_sig") as f:
        c = csv.writer(f)
        if not is_exist:
            c.writerow(['日期', '标题', '阅读量', '在看数', '传播指数', '文章链接', '文章内容', '图片链接', '视频链接'])
        for line in data:
            c.writerow(line)


if __name__ == '__main__':
    for i in range(1, 100):
        data = spider(i)
        save_data(filename='四川发布', data=data)
        print(f"##############{i}##############保存成功")
