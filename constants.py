#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-01-28 09:57
# @Author  : July
import requests
from lxml import html
import os
import sys
import datetime
import csv
from fake_useragent import UserAgent


ua = UserAgent(verify_ssl=False)


etree = html.etree

# 代理ip地址
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=fc91ea822efb13836dc07508b3a47898&orderNo=GL20200131152126nmVxqyej&count=1&isTxt=0&proxyType=1'

# web
index_url = 'http://www.gsdata.cn/query/ajax_arc'

# cookie过期了就修改下
index_cookie = 'visitor_type=old; acw_tc=76b20ff415831107523344124e6aeec0a1fbf23d3574752aca4ec3e76c9553; _csrf-frontend=78052acb4025d004896fefa7987ef43063d0e74a6fdb00be8aa757f9dfde59d2a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22KNUleYp92D7v39FMuHJvJKX-TBdeaq__%22%3B%7D; 53gid2=11579411834005; 53gid0=11579411834005; 53gid1=11579411834005; 53revisit=1583110752487; 53kf_72213613_from_host=www.gsdata.cn; 53kf_72213613_land_page=http%253A%252F%252Fwww.gsdata.cn%252F; kf_72213613_land_page_ok=1; 53uvid=1; onliner_zdfq72213613=0; _gsdataCL=WzAsIjEzNzU3MDI3NTk5IiwiMjAyMDAzMDIwODU5NDYiLCJjZGQyOTAxODNhMGM1OGQ1MmIwNmM5MzdkNWNmMDQwZCIsMjY1NDY3XQ%3D%3D; _gsdataOL=265467%3B13757027599%3B%7B%220%22%3A%22%22%2C%221%22%3A%22%22%2C%222%22%3A%22%22%2C%223%22%3A%22%22%2C%224%22%3A%22%22%2C%225%22%3A%22%22%2C%2299%22%3A%2220200302%22%7D%3B0e7c174a76ae88b5c1d5b447922997b2; _identity-frontend=34c492f17376825dadf2d91d78db33fac19024acefe18045dcb32b63866fe15ca%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A28%3A%22%5B%22576491%22%2C%22test+key%22%2C604800%5D%22%3B%7D; visitor_type=old; Hm_lvt_293b2731d4897253b117bb45d9bb7023=1583110752,1583118831; 53kf_72213613_keyword=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DMJrPxDSnroZ2v4cdJOXzXmgTEjQ1XXSEHGkpJomxmx7%26wd%3D%26eqid%3Da3b375010006b382000000045e5c79ed; 2019ncov=1; Hm_lpvt_293b2731d4897253b117bb45d9bb7023=1583118876; PHPSESSID=38j43hjb7ke09g9r6p2pm52rj7'

web_header = {
    'Host': 'www.gsdata.cn',
    'User-Agent': ua.random,
    'Accept': '*/*',
    'Accept-Encodin': 'gzip, deflate',
    'Cookie': index_cookie,
    'Referer': 'http://www.gsdata.cn/query/arc?q=%E8%82%BA%E7%82%8E',
    'X-Requested-With': 'XMLHttpRequest'
}

"""

"""
detail_cookie = 'pgv_pvi=5671963648; pgv_pvid=6382757760; RK=PFrtiq0NER; ptcz=5208263401e5f54b61c96ac84e969534d84ed2f16cb174cbd23372bbdb8e22da; pac_uid=0_fc2abde7eca45; XWINDEXGREY=0; eas_sid=a1n5N7s1J930V6C6T3Q7z9y0v8; rewardsn=; wxtokenkey=777'

detail_header = {
    'Host': 'mp.weixin.qq.com',
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encodin': 'gzip, deflate',
    'Cookie': index_cookie
}

li = ['2019-12-31', '2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05', '2020-01-06',
             '2020-01-07', '2020-01-08', '2020-01-09', '2020-01-10', '2020-01-11', '2020-01-12', '2020-01-13',
             '2020-01-14', '2020-01-15', '2020-01-16', '2020-01-17', '2020-01-18', '2020-01-19', '2020-01-20',
             '2020-01-21', '2020-01-22', '2020-01-23', '2020-01-24', '2020-01-25', '2020-01-26', '2020-01-27',
             '2020-01-28']

a = ['疫情', '肺炎', '病毒', '武汉', '口罩', '患者',
                                          '钟南山', '医生', '专家', '物资', '谣言', '火神山', '病人',
            '辟谣', '红十字会', '药物', '韩红', '李兰娟', '李文亮', '高福']
# res = requests.get(url=index_url, headers=web_header).json()
# print(res)


# detail_res = requests.get(url='https://mp.weixin.qq.com/s?__biz=MjM5MjQxNDY2Nw==&mid=2649471846&idx=1&sn=e1d2dac23d3ce8b591f26204cc7f24be&scene=0', headers=detail_header).content.decode()
# root_detail_res = etree.HTML(detail_res)
# article_author = root_detail_res.xpath("//span[@class='rich_media_meta rich_media_meta_text']/text()")[0] if \
#     root_detail_res.xpath("//span[@class='rich_media_meta rich_media_meta_text']/text()") else '1'
# article_author = article_author.replace(' ', '').replace('\n', '')  # 作者
# article_content = root_detail_res.xpath("string(//div[@class='rich_media_content '])")  # 文章内容
#
# article_img_url = root_detail_res.xpath("//div[@class='rich_media_content ']//img/@data-src")  # 图片链接
# article_img_url = '\n'.join(article_img_url)
# article_video_url = root_detail_res.xpath("//iframe/@data-src")  # 视频链接
#
# print(article_author, article_content, article_video_url)