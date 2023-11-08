import os
import datetime
import json
import requests
from lxml import html
from until import until
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.options.global_options import AxisOpts

class beike:
    __beike = None
    __beiketoday = None
    __ymd = ''
    __urls = [
        'https://nj.ke.com/ershoufang/pukou/pg{page}dp1sf1/',
        'https://nj.ke.com/ershoufang/liuhe/pg{page}dp1sf1/',
        'https://nj.ke.com/ershoufang/gulou/pg{page}dp1sf1/',
        'https://nj.ke.com/ershoufang/jianye/pg{page}dp1sf1/',
        'https://nj.ke.com/ershoufang/qinhuai/pg{page}dp1sf1/',
        'https://nj.ke.com/ershoufang/xuanwu/pg{page}dp1sf1/',
        'https://nj.ke.com/ershoufang/yuhuatai/pg{page}dp1sf1/',
        'https://nj.ke.com/ershoufang/qixia/pg{page}dp1sf1/',
        'https://nj.ke.com/ershoufang/jiangning/pg{page}dp1sf1/',
        'https://nj.ke.com/ershoufang/lishui/pg{page}dp1sf1/',
        'https://nj.ke.com/ershoufang/gaochun/pg{page}dp1sf1/',
    ]

    def __init__(self,ymd):
        self.__beike = until('beike','')
        self.__ymd = ymd;
        if(len(self.__ymd) == 0):
            self.__ymd = datetime.datetime.now().strftime('%Y%m%d')
        self.__beiketoday = until('beike',self.__ymd)

    def download(self):
        for url in self.__urls:
            for page in range(1,101):
                url_ = url.replace('{page}',str(page))
                try:
                    response = requests.get(url_)
                    print(url_,response.status_code)
                except Exception as e:
                    until.error(e)
                    continue
                tree = html.fromstring(response.content.decode("utf-8"))
                hrefs = tree.xpath('//li[@class="clear"]//div[@class="title"]/a/@href')
                if(len(hrefs) == 0):
                    break
                for href in hrefs:
                    if(self.__beiketoday.hasLog(href)):
                        break
                    try:
                        response = requests.get(href)
                        print(href,response.status_code)
                    except Exception as e:
                        until.error(e)
                        continue
                    tree = html.fromstring(response.content.decode("utf-8"))
                    data = {}
                    try:
                        title = tree.xpath('//div[@class="title"]//h1[@class="main"]/text()')[0]
                        data['title'] = title.strip()
                        price = tree.xpath('//div[@class="price-container"]//span[@class="unitPriceValue"]/text()')[0]
                        data['price'] = price
                        totalprice = tree.xpath('//div[@class="price-container"]//span[@class="total"]/text()')[0]
                        data['totalprice'] = totalprice
                        room = tree.xpath('//div[@class="room"]//div[@class="mainInfo"]/text()')[0]
                        data['room'] = room
                        buildarea = tree.xpath('//div[@class="area"]//div[@class="mainInfo"]/text()')[0]
                        data['buildarea'] = buildarea.strip('平米')
                        block = tree.xpath('//div[@class="communityName"]//a[@class="info no_resblock_a"]/text()')[0]
                        data['block'] = block
                        distname = tree.xpath('//div[@class="areaName"]//span[@class="info"]//a/text()')[0]
                        data['distname'] = distname
                        data['url'] = href
                    except Exception as e:
                        until.error(e)
                        continue
                    print(data)
                    self.__beiketoday.log(href)
                    self.__beiketoday.write(json.dumps(data,ensure_ascii=False),'house.txt')
        print('over')

    def count(self):
        distPrice = {}
        blockPrice = {}
        lines = self.__beiketoday.read('house.txt')
        for line in lines:
            arr = json.loads(line)
            if(arr['distname'] not in distPrice):
                distPrice[arr['distname']] = []
            distPrice[arr['distname']].append(arr['price'])

            if(arr['block'] not in blockPrice):
                blockPrice[arr['block']] = []
            blockPrice[arr['block']].append(arr['price'])

        print('计算区属均价')
        self.__beiketoday.delete('count_dist.txt')
        for dist in distPrice:
            total = 0
            for i in distPrice[dist]:
                total += int(i)
            price = round(total/len(distPrice[dist]))
            data = {}
            data[dist] = str(price)
            print(data)
            self.__beiketoday.write(json.dumps(data,ensure_ascii=False),'count_dist.txt')

        print('计算小区均价')
        self.__beiketoday.delete('count_block.txt')
        for block in blockPrice:
            total = 0
            for i in blockPrice[block]:
                total += int(i)
            price = round(total/len(blockPrice[block]))
            data = {}
            data[block] = str(price)
            print(data)
            self.__beiketoday.write(json.dumps(data,ensure_ascii=False),'count_block.txt')
        print('over')

    def render(self):
        x = []
        y = []
        lines = self.__beiketoday.read('count_dist.txt')
        for line in lines:
            arr = json.loads(line)
            for key, value in arr.items():
                x.append(key)
                y.append(value)
        bar = Bar()
        bar.add_xaxis(xaxis_data = x)
        bar.add_yaxis(series_name = '',y_axis = y)
        title = ''.join([self.__ymd,'区属均价'])
        bar.set_global_opts(title_opts=opts.TitleOpts(title = title))
        filename = ''.join([self.__beiketoday.getDir(),'html',os.sep,'dist.html'])
        print(filename)
        bar.render(filename)
        print('over')

if(__name__ == "__main__"):
    beike = beike('20231016')
    beike.download()
    #beike.count()
    #beike.render()