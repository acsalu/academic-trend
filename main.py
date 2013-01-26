#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
import json
import cgi
import urllib
import urllib2
import cookielib
import httplib

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
    
    
def query(keyword, year):
	UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17'
	#GOOGLE_SCHOLAR_URL = 'http://scholar.google.com/scholar?hl=en&q=%(query)s&btnG=Search&as_subj=eng&as_std=1,5&as_ylo=&as_vis=0'	
	BASE_URL = 'http://api.mendeley.com/oapi/documents/search/%(query)s%%20published_in%%3A%(year)d/?consumer_key=683c042b310ebdf5e52887317ba4694a05103a279'
	url = BASE_URL % {'query': urllib.quote(keyword.encode('utf-8')), 'year':year}
	#jar = cookielib.FileCookieJar("cookies")
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	req = urllib2.Request(url=url, headers={'User-Agent': UA})
	#return req.headers
	res = opener.open(req)
	data = json.load(res)
	#return url
	return data['total_results']
	
# if resp.status==200:
# 			html = resp.read()
# 			results = []
# 			html = html.decode('ascii', 'ignore')
# 			return html	
#     else:
#     	return resp.status
    
# 	resp = conn.getresponse() 
# 	
# 	
# 	req = urllib2.Request(url=url, headers={'User-Agent': UA})
# 	
# 	cookies = cookielib.MozillaCookieJar()
# 	cookies.load()
# 	cookie_handler= urllib2.HTTPCookieProcessor(cookies)
# 	redirect_handler= urllib2.HTTPRedirectHandler()
# 	opener = urllib2.build_opener(redirect_handler,cookie_handler)
# 	
# 	hdl = opener.urlopen(req)
# 	html = hdl.read()
# 	#urllib2.urlopen(urllib2.Request(url="http://www.google.com"))
# 	return 'hi' #self.parse(html)
	
 
def parse(html):
	start_tag = '<div id="gs_ab_md">'
	end_tag = '</div>'
	start = html.find(start)
	end = html.find(end)
	
	almost = html[start + len(start_tag):end]
	prefix = 'About'
	postfix = 'result'
	return int(almost[almost.find(prefix) + len(prefix):almost.find(postfix)].replace(',', ''))

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	template_values = {}
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))
        
class QueryHandler(webapp2.RequestHandler):
	def get(self):
		#start = 2011
		#end = 2012
		keyword = self.request.get("q")
		start = int(self.request.get("start"))
		end = int(self.request.get("end"))
		result = []
		for i in range(start, end + 1):
			result.append(query(keyword, i))
		
		self.response.out.write(json.dumps(result))
	

		

app = webapp2.WSGIApplication([
    (r'/', MainHandler),
    (r'/query', QueryHandler)
], debug=True)
