# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import re


class Tool:
    removeImg=re.compile('<img.*?>| {7}|')
    removeAddr=re.compile('<a.*?>|</a>')
    replaceLine=re.compile('<tr>|<div>|</div>|</p>')
    replaceTD=re.compile('<td>')
    replacePara=re.compile('<p.*?>')
    replaceBR=re.compile('<br<br>|<br>')
    removeExtraTag=re.compile('<.*?>')

    def replace(self,x):
        x=re.sub(self.removeImg,"",x)
        x=re.sub(self.removeAddr,"",x)
        x=re.sub(self.replaceLine,"\n",x)
        x=re.sub(self.replaceTD,"\t",x)
        x=re.sub(self.replacePara,"\n  ",x)
        x=re.sub(self.replaceBR,"\n",x)
        x=re.sub(self.removeExtraTag,"",x)
        return x.strip()
        
class BDTB:
    
    def __init__(self,baseUrl,seeLZ):
        self.baseURL=baseUrl
        self.seeLZ='?see_lz='+str(seeLZ)
        self.tool=Tool()

    def login_in(self,username,password):
        self.username=username
        self.password=password
        self.loginUrl='https://passport.baidu.com/v2/api/?login'
        tokenUrl='https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login'
        
        self.cookie=cookielib.CookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)        
        baiduMainUrl = "http://www.baidu.com";
        resp = urllib2.urlopen(baiduMainUrl);
        #respInfo = resp.info();
        #print "respInfo=",respInfo;
        for index, cookie in enumerate(self.cookie):
            print '[',index, ']',cookie;
        #获取token
        tokenReturn=urllib2.urlopen(tokenUrl)
        
        matchVal = re.search(' "token" : "(.*?)"',tokenReturn.read())
        self.tokenVal=matchVal.group(1)
        print self.tokenVal

        pKeyUrl='https://passport.baidu.com/v2/getpublickey?token='+self.tokenVal+'&tpl=pp&apiver=v3&callback=bd__cbs__bqxcfc'
        print 'pKeyUrl:'+pKeyUrl
        rsa=urllib2.urlopen(pKeyUrl)
        #print rsa.read()
        matchVal2=re.search('''"key":'(.*?)'}''',rsa.read())
        print rsa.read()
        rsakey=matchVal2.group(1)
        print matchVal2
        print matchVal2.group(1)


        self.post=urllib.urlencode({
            'username' : '15029277900',
            'password' : 'cclpw2nybz',
            'apiver':'v3',
            'u' : 'http://www.baidu.com/',
            'tpl' : 'mn',
            'token' : self.tokenVal,
            'staticpage' : 'https://www.baidu.com/cache/user/html/v3Jump.html',
            #'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
            'isPhone' : 'false',
            'safeflg':'0',
            'charset' : 'UTF-8',
            'callback' : 'parent.bd__pcbs__8s6huc' ,
            'crypttype':'12',
            'detect':'1',
            'rsakey':rsakey,
            'mem_pass':'on',
            'verifycode'    : "",
            "logintype":"basicLogin",
            'logLoginType':'pc_loginDialog'})
        #self.postdata=self.postdata.encode('utf-8')

        post={
            'apiver':'v3',
            'callback':'parent.bd__pcbs__tgmpuy',
            'charset':'UTF-8',
            'codestring':'',
            'countrycode':'',
            'cryttype':'12',
            'detect':'1',
            'gid':'',
            'idc':'',
            'isPhone':'false',
            'logLoginType':'pc_loginDialog',
            'loginmerge':'true',
            'logintype':'dialogLogin',
            'mem_pass':'on',
            'password':'cclpw2nybz',
            'ppui_logintime':'',
            'quick_user':'0',
            'rsakey':rsakey,
            'safeflg':'0',
            'splogin':'rate',
            'staticpage':'https://www.baidu.com/cache/user/html/v3Jump.html',
            'subpro':'',
            'token':self.tokenVal,
            'tpl':'mn',
            'tt':'',
            'u':'https://www.baidu.com/',
            'username':'15029277900',
            'verifycode':'',

            }
        postdata=urllib.urlencode(post)
        request=urllib2.Request(url=self.loginUrl,data=self.post)
        
        request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8');
        request.add_header('Accept-Encoding','gzip, deflate, br');
        request.add_header('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3');
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0');
        request.add_header('Content-Type','application/x-www-form-urlencoded');

        
        result=urllib2.urlopen(request)
        print result.read()
        for index, cookie in enumerate(self.cookie):
            print '[',index, ']',cookie;
        content=urllib2.urlopen('http://i.baidu.com/').read()
        print content
       
        
        #print result
    
    def getPage(self,pageNum):
        try:
            url=self.baseURL+self.seeLZ+'&pn='+str(pageNum)
            request=urllib2.Request(url)
            response=urllib2.urlopen(request)
           # print self.response.read()
            self.response=response.read().decode('utf8')
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接百度贴吧失败：",e.reason
                print None
    def getTitle(self):
        page=self.response
#        print page
        pattern=re.compile('<h1.*?class="core_title_txt.*?>(.*?)</h1>',re.S)
        result=re.search(pattern,page)
        if result:
            print result.group(1)
            return result.group(1).strip()
        else:
            print "error!!!"
            return None
    def getPageNum(self):
        page=self.response
#        print page
        pattern=re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>.*?</li>',re.S)
        result=re.search(pattern,page)
        if result:
           print '共'+str(result.group(1))+'页'
           return result.group(1).strip()
        else:
            print "error!!!"
            return None
    def getContent(self):
        page=self.response
        pattern=re.compile('div id="post_content_.*?>(.*?)</div>',re.S)
        result=re.findall(pattern,page)
        if result:
            for item in result:
                print self.tool.replace(item)
        else:
            print "error!!!"
            return None








        
baseURL='http://tieba.baidu.com/p/3931377615'
bdtb=BDTB(baseURL,0)
bdtb.login_in('15029277900','cclpw2nybz')
checkreturn=urllib2.urlopen('https://passport.baidu.com/v2/api/?login')
print checkreturn.read()
#bdtb.getPage(1)
#bdtb.getTitle()
#bdtb.getPageNum()
#bdtb.getContent()
