from django.db import models
import re
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
# -*- coding: utf-8 -*-
# Create your models here.


class Website(models.Model):
    head = models.TextField()
    date = models.TextField()
    text = models.TextField()

    def __str__(self):
        return self.name

def parse(j,k):
    rroot_url = 'http://cs.whu.edu.cn/news_list.aspx?category_id=54&page='  # 一级页面的url
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    }
    grab_urls = []  #设置通知url容器
    for i in range(j,k+1):
        root_url = rroot_url+'i'
        request = urllib.request.Request(root_url, headers=header)
        root_response = urllib.request.urlopen(request).read()      #下载一级页面
        root_response = root_response.decode('utf-8')              #一级页面转码utf-8
        soup = BeautifulSoup(root_response, 'html.parser')        #使用beautifulsoup解析页面
        time.sleep(0.1)
        #link_grab_root = soup.find_all('a', href=re.compile(r'/news_show.aspx\?id=\d+'))
        #urls.append(link_grab_root)
        for link in soup.find_all('a', href=re.compile(r'/news_show.aspx\?id=\d+')):   #使用beautifulsoup获取通知url
            urls = "http://cs.whu.edu.cn" + str(link.get('href'))
            #print(urls)
            grab_urls.append(urls)
    #print(grab_urls)
    grab_data = []
    for url in grab_urls:
        request = urllib.request.Request(url, headers=header)
        url_response = urllib.request.urlopen(request).read()
        url_response = url_response.decode('utf-8')
        soup = BeautifulSoup(url_response, 'html.parser')
        data = {}
        title_node = soup.find(class_="sp1")
        data['title'] = title_node.get_text()
        repattern = re.compile(r'\d+年\d+月\d+日\d+时')
        data['date'] = repattern.findall(url_response)[0]
        content_node = soup.find_all("p")
        grab_text = []
        for text in content_node:
            text = text.get_text()
            new_text = re.sub('\u3000|\xa0|\n|版权所有 ©武汉大学计算机学院   | copyright © 2008-2018 School of Computer Science, Wuhan University. All Rights Reserved.|地址：湖北省武汉市八一路武汉大学 邮编：430072电话：027-68775361 027-68775363 \|', "", text)
            grab_text.append(new_text)
        #处理文章主体，删除空格，拼接文字
        for i in grab_text:
            if '' in grab_text:
                grab_text.remove('')
        separator = ''
        grab_text = separator.join(grab_text)
        #存入字典
        data['content'] = grab_text
        grab_data.append(data)
        #存入数据库
        Website.objects.create(head=title_node.get_text(), date=repattern.findall(url_response)[0], text=grab_text)

    #print(grab_data)
    #print("已成功抓取第" + start_page + "页至第"+ end_page +"页")