from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random
import numpy as np
import pandas as pd
from datetime import datetime
import ssl
from urllib.error import URLError
from urllib.error import HTTPError
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
class GetInformation(): 
    def __init__(self, i): 
        self.ListTopic = pd.read_csv('TopicLink{}.csv'.format(i))
        self.df_post = pd.DataFrame()
        self.df_post['title'] = []
        self.df_post['author'] = []
        self.df_post['like'] = []
        self.df_post['date'] = []
        self.df_post['content'] = []
    
    def getIdUserPost(self, url): 
    # url = "http://..." là link truy cập đến trang cần thu thập dữ liệu. 
    # sử dụng beautifulSoup, hãy import thư viện này trước khi gọi hàm
    # import ssl và đặt: 
    #ssl_context.check_hostname = False
    #ssl_context.verify_mode = ssl.CERT_NONE
        try: 
            html = urlopen(self, url, context=ssl_context)
            bs = BeautifulSoup(html, 'html.parser')
            FirstPost = bs.select('li.message.first')
            idUser = FirstPost[0].attrs['data-author']
            return idUser
        except HTTPError as e:
            pass
    def getListPostTopic(self, url): 
        try: 
            html = urlopen(url, context=ssl_context)
            bs = BeautifulSoup(html, 'html.parser')
            List_Post = bs.select('ol.messageList#messageList li[id^="post"]')
            return List_Post
        except HTTPError as e: 
            pass

    # return bs4.element.ResultSet
    # Là một danh sách các tags chứa post. 
    def getUserName(self, li_tag): 
        #li_tags là một tags chứa các bài post trên diễn đàn f319.com. 
        #li_tags có thuộc tính "data_author", gọi thuộc tính này để trả về tên user đã post bài
        # Trước khi gọi hàm này cần gọi hàm GetListPost Trước. 
        return li_tag.attrs['data-author']
        # return username (string)
    def getNummberofPage(self, url): 
        # Hàm này dùng để xác định số trang của một Topic
        try:
            try:
                html = urlopen(url, context=ssl_context)
                bs = BeautifulSoup(html, 'html.parser')
                nav = bs.select('div.pageNavLinkGroup')
                numberPage = (nav[0].find_all('a')[-2]).text
                return int(numberPage)
            except HTTPError as e:
                pass 
        except IndexError:
            pass
    def getTitle(self, url): 
        # Hàm này dùng để lấy ra tiêu đề của Topic. 
        # bs là beautifulSoup oject
        # return string
        html = urlopen(url, context=ssl_context)
        bs = BeautifulSoup(html, 'html.parser')
        title = bs.h1.text
        return title
    def getLikePost(self, li_tag): 
        # li_tag là tag chứa nội dung của post. 
        # Hàm Này trả về lượt like của một post
        liketag = (li_tag.find('a',href= re.compile('^(posts)((?!report).)*$') ,class_='OverlayTrigger'))
        if liketag == None: 
            like = 0
        else: 
            like = liketag.text[0]
        return like
    def getDatePost(self, li_tag): 
        # trước khi gọi hàm này cần gọi hàm getListPost
        # Hàm này trả về thuộc tính date. 
        date_string = (li_tag.find('a', class_='datePermalink')).text
        date_format = '%d/%m/%Y, %H:%M'
        date = datetime.strptime(date_string, date_format)
        return date
    def getContentPost(self, li_tag): 
        # Trước khi gọi hàm này, cần gọi hàm GetListPost 
        # Hàm này trẻ về nội dung của Post. 
        content = (li_tag.find('blockquote', class_= "messageText ugc baseHtml")).get_text().strip()    
        return content
    def addNewPost(self, url):
        li_tags = self.getListPostTopic(url) 
        for post in li_tags: 
            # li_tag là danh sách các tag li chứa nội dung của các post. 
            title = self.getTitle(url)
            like = self.getLikePost(post)
            author = self.getUserName(post)
            date = self.getDatePost(post)
            content = self.getContentPost(post)
            new_record = {'title': title, 'author': author, 'like': like, 'date': date, 'content': content}
            self.df_post = self.df_post.append(new_record, ignore_index=True)

            