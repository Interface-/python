import urllib
import urllib2
import cookielib
import re
import time

hosturl = 'http://www.zhihu.com'
posturl = 'http://www.zhihu.com/login/email'
captcha_pre = 'http://www.zhihu.com/captcha.gif?r='

#set cookie
cj = cookielib.CookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

#get xsrf
h = urllib2.urlopen(hosturl)
html = h.read()
xsrf_str = r'&lt;input type="hidden" name="_xsrf" value="(.*?)"/&gt;'
xsrf = re.findall(xsrf_str, html)
print xsrf

#get captcha
def get_captcha():
    captchaurl = captcha_pre + str(int(time.time() * 1000))
    print captchaurl
    data = urllib2.urlopen(captchaurl).read()
    f = file('captcha.jpg',"wb")
    f.write(data)
    f.close()
    captcha = raw_input('captcha is: ')
    print captcha
    return captcha

#post data
def post_data(captcha,xsrf):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
               'Referer' : 'http:www.zhihu.com'}
    postData = {'_xsrf' : xsrf,
                'password' : '1995216qw',
                'captcha' : captcha,
                'email' : '13149216714',
                'remember_me' : 'true',
                }

    #request
    postData = urllib.urlencode(postData)
    print postData
    request = urllib2.Request(posturl, postData, headers)
    response = urllib2.urlopen(request)
    text = response.read()
    return text

#post it
captcha=get_captcha()
print captcha
text=post_data(captcha,xsrf)
print text

#post again
captcha=get_captcha()
text=post_data(captcha,xsrf)
print text

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
               'Referer' : 'http:www.zhihu.com'}
request = urllib2.Request(url='http://www.zhihu.com', headers=headers)
response = urllib2.urlopen(request)
print response.read()
