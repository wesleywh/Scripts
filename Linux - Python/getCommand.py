import urllib2
import os

pageRequest = raw_input("Enter Webpage(EX:www.byu.edu): ")
getRequest = raw_input("Page Request(EX:index.html): ")
urlToCall = "http://"+pageRequest+"/"+getRequest
pageContent = urllib2.urlopen(urlToCall).read()
print pageContent
