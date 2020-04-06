import re
import pandas as pd
import requests

data = pd.date_range(start='20200106', end='20200405')
date_list = data.array
date_lists = []
for i in date_list:
    date_lists.append(str(i)[0:10])
print(date_lists)

# a = 'dfdfdsfdsfsfdsfsdf'
#
# b = a.split('\n')
# print(b)
date_list = ['2020-01-18-', '2020-01-19-', '2020-01-20-', '2020-01-21-', '2020-01-22-',
             '2020-01-23-',
             '2020-01-24-', '2020-01-25-', '2020-01-26-', '2020-01-27-', '2020-01-28-',
             '2020-01-29-',
                 '2020-01-30-', '2020-01-31-',

             '2020-02-01-', '2020-02-02-', '2020-02-03-',
             '2020-02-04-', '2020-02-05-', '2020-02-06-',
             '2020-02-07-', '2020-02-08-', '2020-02-09-',
             '2020-02-10-', '2020-02-11-', '2020-02-12-',
             '2020-02-13-', '2020-02-14-', '2020-02-15-', '2020-02-16-']


# a = {'1': 2, '2': 2}
# a.update({'3': 3})
# print(len(date_list))

# text = '//@发生的发生的发萨达:对她说的分散//@asdfasddfas：'
#
# p = re.compile(r'//@(.*?)[:：]', re.S)
# forwarded_user_names = p.findall(text)  # 被转发人昵称列表
# forwarded_user_name = forwarded_user_names[0]  # 被转发人昵称
#
# print(forwarded_user_names)
# print(type(forwarded_user_name))

"""
    for date in date_list:
        for num in range(0, 24):
            # 保存第一页数据，并修改总页数
            wb = WbSpider(keyword=key, start_time=date + str(num), end_time=date + str(num + 1), page=1)

            data = wb.start()
            save_data(csv_name, data)

            print('################################################')
            print(f"{date + str(num)}~{date + str(num + 1)}第1数据存储成功。。。。。。")
            print('################################################')

            # 保存剩下页数数据
            for i in range(2, total_page+1):
                wb = WbSpider(keyword=key, start_time=date+str(num), end_time=date+str(num+1), page=i)
                data = wb.start()
                save_data(csv_name, data)
                print('################################################')
                print(f"{date+str(num)}至{date+str(num+1)}第{i}页数据存储成功。。。。。。")
                print('################################################')
"""

"""
    for date in date_list:
        # 保存第一页数据，并修改总页数
        wb = WbSpider(keyword=key, start_time=date, end_time=date, page=1)

        data = wb.start()
        save_data(csv_name, data)

        print('################################################')
        print(f"{date}第1页数据存储成功")
        print('################################################')

        # 保存剩下页数数据
        for i in range(2, total_page + 1):
            wb = WbSpider(keyword=key, start_time=date, end_time=date, page=i)
            data = wb.start()
            save_data(csv_name, data)
            print('################################################')
            print(f"{date}第{i}页数据存储成功")
            print('################################################')
"""