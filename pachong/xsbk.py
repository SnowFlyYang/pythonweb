#!/usr/bin/python2
#-*-coding:utf-8-*-
import urllib
import urllib2
import re
import time
import thread

#嗅事百科爬虫类
class QSBK:
	#初始化定义方法
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		#初始化headers
		self.headers = {'User-Agent':self.user_agent}
		#存放段子的变量
		self.stories = []
		#存放程序是否继续运行变量
		self.enable = False
	#传入某一页的索引获取页面代码
	def getPage(self,pageIndex):
		try:
			url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			#构建请求的request
			request = urllib2.Request(url,headers = self.headers)
			#利用urlopen获取页面代码
			response = urllib2.urlopen(request)
			#将页面转化成utf-8编码
			pageCode = response.read().decode("utf-8",'ignore')
			return pageCode
		except urllib2.URLError,e:
			if hasattr(e,"reason"):
				print u"连接糗事百科失败,错误原因",e.reason
				return None
	#传入某一页代码，放回本页不带图片的段子列表
	def getPageItems(self,pageIndex):
		pageStories = []
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print "页面加载失败..."
			return None
		pattern = re.compile('<div.*?author.*?clearfix">.*?<a .*?<img.*?>.*?</a>.*?<a .*?>.*?<h2>(.*?)</h2>.*?</a>.*?<div.*?content">.*?<span>(.*?)</span>.*?</div>(.*?)stats">.*?</div>',re.S)
		items = re.findall(pattern,pageCode)
		pageStories = []
		for item in items:
			haveimg=re.search("img",item[2])
			if not haveimg:
				replaceBR = re.compile("<br/>")
				text=re.sub(replaceBR,"\n",item[1])
				pageStories.append([item[0].strip(),text.strip()])
		return pageStories
	#加载并提取页面内容，加入到列表
	def loadPage(self):
		#如果当前未看的页数少于2页，则加载第一页
		if self.enable == True:
			if len(self.stories)<2:
				#获取第一页
				pageStories = self.getPageItems(self.pageIndex)
				
				#将该页的段子存放到全局list中
				if pageStories:
					self.stories.append(pageStories)
					#获取完之后索引页码加一
					self.pageIndex += 1
	#调用该方法每次敲回车打印输出一个段子
	def getOneStroy(self,pageStories,page):
		#遍历一页的段子
		for story in pageStories:
			#等待用户输入
			input = raw_input()
			#每当回车一次判断是否要加载新页面
			self.loadPage()
			#如果输入Q则则程序结束
			if input == 'Q':
				self.enable = False
				return
			try:
				print u"第%d页\t发布人:%s\t\n%s"%(page,story[0],story[1])
			except:
				print u"出错"
	#开始方法
	def start(self):
		print u"正在读取糗事百科,按回车查看新段子，Q退出"
		#使变量为True,程序可以正常运行
		self.enable = True
		#先加载一页内容
		self.loadPage()
		#局部变量，控制当前第几页
		nowPage = 0

		while self.enable:
			if len(self.stories)>0:
				#从全局list中获取一页的段子
				pageStories = self.stories[0]

				#当前读到的页数加一
				nowPage += 1
				#将全局list中第一元素删除，因为已经取出
				del self.stories[0]
				#输出该页的段子
				self.getOneStroy(pageStories,nowPage)

spider = QSBK()
spider.start()


