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
	keyword = keyword.replace(' ', '+')

	MAS_API_URL = 'http://academic.research.microsoft.com/json.svc/search?AppId=a47fc86b-18e6-445c-836c-f51494f65822&FullTextQuery=%s&YearStart=%d&YearEnd=%d'
	url = MAS_API_URL % (keyword, year, year)
	opener = urllib2.build_opener()
	req = urllib2.Request(url=url)
	res = opener.open(req)
	data = json.load(res)
	return data['d']['Publication']['TotalItem']
	
class MainHandler(webapp2.RequestHandler):
    def get(self):
    	template_values = {}
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))
        
class QueryHandler(webapp2.RequestHandler):
	def get(self):
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
