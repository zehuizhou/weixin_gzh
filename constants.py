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
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=8d7cc3c74eeb76ad422c67df45944d31&orderNo=GL20200131152126nmVxqyej&count=1&isTxt=0&proxyType=1'

# web
index_url = 'http://www.gsdata.cn/query/ajax_arc'

# cookie过期了就修改下
index_cookie = 'visitor_type=old; 53gid2=11300403675005; 53revisit=1582991410761; acw_tc=76b20fea15857574622268621e22f738891536d30f5cb336771fbc852731ce; _csrf-frontend=1242d3bdb062308aaee162b2791335534e5e81145c71b6e0b5bade5d619d4d61a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22va2kWlfyiSjQDAF_YPWCn5LjDiNFNr4e%22%3B%7D; Hm_lvt_293b2731d4897253b117bb45d9bb7023=1584453005,1585757464,1586147014; 53gid0=11300403675005; visitor_type=old; 53gid1=11300403675005; 53kf_72213613_from_host=www.gsdata.cn; 53kf_72213613_keyword=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DatnzBAWv93kJKkSiFV8IOgYdLSPqAVHixZkghgF_SpG%26wd%3D%26eqid%3Dd1c063370009be1c000000045e8aaec2; 53kf_72213613_land_page=http%253A%252F%252Fwww.gsdata.cn%252F; kf_72213613_land_page_ok=1; 53uvid=1; onliner_zdfq72213613=0; _gsdataCL=WzAsIjE4MDk3NTU2NTU5IiwiMjAyMDA0MDYxMzE3MjEiLCJlNTA4MGIxYTMxNmIyYzczMzFiNzljMWVkMWNlN2E3NCIsMTIwNTIyXQ%3D%3D; _gsdataOL=120522%3B18097556559%3B%7B%220%22%3A%22%22%2C%221%22%3A%22%22%2C%222%22%3A%22%22%2C%223%22%3A%22%22%2C%224%22%3A%22%22%2C%225%22%3A%22%22%2C%2299%22%3A%2220200406%22%7D%3B1379eb64f30071f28371b5e3b3b9b637; PHPSESSID=bmovcpejocqap1vl9tbb6urhp4; _identity-frontend=d9c9dc3f2b7347a382f0c84ccf705e244b9c5ea8ff5ba8269616f41c07a53125a%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A28%3A%22%5B%22228674%22%2C%22test+key%22%2C604800%5D%22%3B%7D; Hm_lpvt_293b2731d4897253b117bb45d9bb7023=1586150247'

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
detail_cookie = 'RK=1Mrt2o0tRR; ptcz=92f7c034bacefda6b02f83225cde534286dfd1ac8d9330dfc122f582607673c5; pgv_pvi=2349735936; tvfe_boss_uuid=cabacb0c10b4a901; pgv_pvid=7079222748; LW_uid=f1k5j6T075A2u5H5b5c7J474s2; eas_sid=k1Y5C6O0S5b2D505U5D7S4l7z7; o_cookie=2672085019; pac_uid=1_2672085019; XWINDEXGREY=0; ied_qq=o2672085019; uin_cookie=o2672085019; LW_sid=H1S5B7A9c1m8Z7l4d7m6O172g9; uin=o0244776919; skey=@vVXtji1gL; pgv_si=s6304292864; _qpsvr_localtk=0.25625078201167106; rewardsn=; wxtokenkey=777'

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