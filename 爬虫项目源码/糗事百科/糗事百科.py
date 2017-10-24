# coding=utf-8
import urllib
import urllib2
import re
import thread
import time

# 定义QSBK爬虫类
class QSBK:
    # 初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        # 初始化headers
        self.headers = {'User-Agent' :self.user_agent}
        # 存放段子的变量，每一个元素是每一页段子
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False

    # 传入某一页的索引获得页面的代码
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            # 构建请求的request
            request = urllib2.Request(url,headers=self.headers)
            # 利用urlopen获取页面的代码
            response = urllib2.urlopen(request)
            # 将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print "error",e.reason
                return None

    # 传入某一页的代码，返回本页不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "page load error"
            return None
        pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</',re.S)
        items = re.findall(pattern,pageCode)
        # 存储每页的段子们
        pageStories = []
        # 遍历正则表达式匹配的信息
        for item in items:
            # item[0]段子发布人， item[1]内容， item[2]赞数
            pageStories.append([item[0].strip(),item[1].strip(),item[2].strip()])
        return pageStories

    # 加载并提取页面的内容，加入到列表中
    def loadPage(self):
        # 如果当前未看的页数少于2页，则加载新的一页
        if self.enable==True:
            if len(self.stories)<2:
                # 获取新的一页
                pageStories = self.getPageItems(self.pageIndex)
                # 将改页的段子放到全局的list中
                if pageStories:
                    self.stories.append(pageStories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1

    # 调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        # 遍历一页的段子
        for story in pageStories:
            input = raw_input()
            # 每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            # 如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人：%s\t 赞：%s\n%s" %(page,story[0],story[2],story[1])

    # 开始方法
    def start(self):
        print u'正在读取，回车查看，Q退出'
        # 使变量为True，程序可以正常运行
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 当前读到的页数加一
                nowPage +=1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()