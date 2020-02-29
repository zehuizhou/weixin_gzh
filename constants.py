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
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=3f3a3212bb8129e0d70d325c41bed8c7&orderNo=GL20200223101445SA8mbNNF&count=1&isTxt=0&proxyType=1'

# web
index_url = 'http://www.gsdata.cn/query/ajax_arc'

# cookie过期了就修改下
index_cookie = 'acw_tc=76b20fe815813177246883744e4e628533b6a000162eaaa41b06489d153341; 53gid2=10307206372013; 53revisit=1581317726268; _csrf-frontend=3986149ab949de3e3acb72703477f124c386a454d2cb22908c2326274b22da40a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22zoNS2DZSkH9-OJUfJDUYq-SR3c5ikGUV%22%3B%7D; Hm_lvt_293b2731d4897253b117bb45d9bb7023=1581437472,1581488928,1581648153,1582423006; visitor_type=old; 53gid0=10307206372013; 53gid1=10307206372013; 53kf_72213613_from_host=www.gsdata.cn; 53kf_72213613_keyword=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DR1_eK3-GVFH2ZezcRvqPlGE1ad0gcQLmamEu0Ptx5KS%26wd%3D%26eqid%3Db1007c2000425f33000000045e51dbd7; 53kf_72213613_land_page=http%253A%252F%252Fwww.gsdata.cn%252F; kf_72213613_land_page_ok=1; _gsdataCL=WzAsIjEzNzU3MDI3NTk5IiwiMjAyMDAyMjMwOTU2NTIiLCIxY2M2MWJjYmE3YjQxMjIyNDQ2ZThjOGI1MGVjZmU0OCIsMjY1NDY3XQ%3D%3D; _gsdataOL=265467%3B13757027599%3B%7B%220%22%3A%22%22%2C%221%22%3A%22%22%2C%222%22%3A%22%22%2C%223%22%3A%22%22%2C%224%22%3A%22%22%2C%225%22%3A%22%22%2C%2299%22%3A%2220200223%22%7D%3Beef7f545cb61dffb279dfe028052d5be; PHPSESSID=i2966fjb7lidlnb5u22mqj2ae5; _identity-frontend=34c492f17376825dadf2d91d78db33fac19024acefe18045dcb32b63866fe15ca%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A28%3A%22%5B%22576491%22%2C%22test+key%22%2C604800%5D%22%3B%7D; Hm_lpvt_293b2731d4897253b117bb45d9bb7023=1582423015; 53uvid=1; onliner_zdfq72213613=0'

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
detail_cookie = 'pgv_pvi=9100752896; pgv_pvid=8347507092; RK=pNrt2I0tTT; ptcz=5953521d372d7088d78ab819b49193fd7a0531a7d198ef6ce684e236c376f76e; sd_userid=16301563429994862; sd_cookie_crttime=1563429994862; pac_uid=1_244776919; eas_sid=t1p5w6V4G7I3h2e8D411j7c1M6; XWINDEXGREY=0; tvfe_boss_uuid=bb828ca3a9cf9030; rewardsn=; wxtokenkey=777'

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