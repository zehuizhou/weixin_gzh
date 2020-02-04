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
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=4ed5fac7b24bba823e18f5299a16232e&orderNo=GL20200112165156B8GF39F4&count=1&isTxt=0&proxyType=1'

# web
index_url = 'http://www.gsdata.cn/query/ajax_arc'

# cookie过期了就修改下
index_cookie = 'visitor_type=old; 53gid1=10270743298013; acw_tc=76b20feb15801189227037803e5be3d7c77521b97eba62d11b4f93c348e195; 53gid2=10270743298013; 53revisit=1580118925140; _csrf-frontend=db4dd489f46ccb24e29a05d810a89b21143d4f7ff84d39611af7513369da9402a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%228i_n5ADxgva5b7fHogsC7ypFH4Te-mxb%22%3B%7D; Hm_lvt_293b2731d4897253b117bb45d9bb7023=1580118925,1580137512,1580176844; visitor_type=old; 53gid0=10270743298013; 53kf_72213613_from_host=www.gsdata.cn; 53kf_72213613_keyword=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DRtNx8QezlhqNhsKl9A8ciddH_mIP3fTULFDNDe-4-o3%26wd%3D%26eqid%3Dd011363600a5b8a5000000065e2f95c8; 53kf_72213613_land_page=http%253A%252F%252Fwww.gsdata.cn%252F; kf_72213613_land_page_ok=1; 53uvid=1; onliner_zdfq72213613=0; 53gid1=10270743298013; _gsdataCL=WzAsIjEzNzU3MDI1MDUxIiwiMjAyMDAxMjgyMzA0MTEiLCI2MDQwMzJhOTE1ZTdiMjViMWE0ZDVlMWRkZDM4Mjc2YiIsMjYyNDk0XQ%3D%3D; _gsdataOL=262494%3B13757025051%3B%7B%220%22%3A%22%22%2C%221%22%3A%22%22%2C%222%22%3A%22%22%2C%223%22%3A%22%22%2C%224%22%3A%22%22%2C%225%22%3A%22%22%2C%2299%22%3A%2220200128%22%7D%3B841c7cf72b65bc07b3f6785146055deb; PHPSESSID=u3uln31amlrg9uaqusjlptss96; _identity-frontend=6ad5cb31f682446e273dd4eca93c137afd50abd99df6b145df9a6ca3f26576ffa%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A28%3A%22%5B%22573868%22%2C%22test+key%22%2C604800%5D%22%3B%7D; Hm_lpvt_293b2731d4897253b117bb45d9bb7023=1580223887'

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
detail_cookie = 'pgv_pvi=9100752896; pgv_pvid=8347507092; RK=pNrt2I0tTT; ptcz=5953521d372d7088d78ab819b49193fd7a0531a7d198ef6ce684e236c376f76e; sd_userid=16301563429994862; sd_cookie_crttime=1563429994862; pac_uid=1_244776919; eas_sid=t1p5w6V4G7I3h2e8D411j7c1M6; XWINDEXGREY=0; LW_uid=21K5k7Z9r775s2Z474r7G2U8W9; ptui_loginuin=2672085019; uin=o2672085019; uin_cookie=o2672085019; ied_qq=o2672085019; LW_sid=t1m5g7w9a7x522e6Z970d4y039; ua_id=HtWMWyTiAG1rGMGqAAAAAFKF8IskxdWAP_M1zj0KOeY=; rewardsn=; wxtokenkey=777; tvfe_boss_uuid=3dbfbe80b1257fe5; pgv_info=ssid=s464426438; o_cookie=2672085019'

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