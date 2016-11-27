import urllib2
import re
import pickle
import pprint
from bs4 import BeautifulSoup
import json
import sys

def printlog(content):
    print(content)
    f.write(content+'\n') # python will convert \n to os.linesep

def extractstr(pre, post, body):
    m = re.search(pre + '(.+?)' + post, body)
    if m:
        return m.group(1)
    else:
        return ""
def extractURLs(pre, post, body):
    try:
        body = " ".join(body.split())
        body = body.split(pre, 1)[1]
        body = body.split(post, 1)[0]
        return extractlinks(body)
    except:
        return ""

def extractlinks(html):
    soup = BeautifulSoup(html,"html.parser")
    anchors = soup.findAll('a')
    links = []
    for a in anchors:
        links.append(a['href'])
    return links
def gethtml(url):
    req = urllib2.Request(url)
    req.add_header('Cookie', key)
    resp = urllib2.urlopen(req)
    return resp
def exp_dict(course):
    global hasExpanded
    if hasExpanded == 0:
        coursedic[course] = {}
    hasExpanded = 1

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


content='<html><head>    <meta charset="utf-8" />    <meta http-equiv="X-UA-Compatible" content="IE=edge" />    <title></title>     <script src="http://karakterer.dtu.dk/Scripts/jquery-1.7.1.min.js" type="text/javascript"></script>    <!--<script src="tt@ReleaseHelper.BaseUrl@Url.Content("~/Scripts/modernizr-1.7.min.js")" type="text/javascript"></script>-->    <style>        #outercontent_0_LeftColumn { width: 0px;}        #outercontent_0_RightColumn { width: 0px;}        #outercontent_0_ContentColumn { width: 100%;}        table td{ border: 0px;}    </style></head><body>            <form id="karsumForm" runat="server"><a id="top" ></a><h1>    Karakterfordeling</h1><h2>01005 Matematik 1, Sommer 2016</h2><table>    <tr>        <td style="padding-right: 2em">            Antal tilmeldte        </td>        <td>            1081        </td>    </tr>    <tr>        <td style="padding-right: 2em">            Fremm&#248;dte        </td>        <td>            1048        </td>    </tr>        <tr>            <td style="padding-right: 2em">                Antal best&#229;et            </td>            <td>                759                (70                %                af de tilmeldte,                72                %                af de fremm&#248;dte)            </td>        </tr>        <tr>            <td style="padding-right: 2em">                Eksamensgennemsnit            </td>            <td>7,9 (Efter 7-trinsskalaen)            </td>        </tr>             <tr>                 <td style="padding-right: 2em">                     Andre versioner                 </td>                 <td>                         <a href="http://karakterer.dtu.dk/Histogram/1/01005-3/Summer-2015" style="padding-right: 3px;">s15</a>                         <a href="http://karakterer.dtu.dk/Histogram/1/01005-3/Summer-2014" style="padding-right: 3px;">s14</a>                         <a href="http://karakterer.dtu.dk/Histogram/1/01005-3/Winter-2013" style="padding-right: 3px;">v13</a>                         <a href="http://karakterer.dtu.dk/Histogram/1/01005-3/Summer-2013" style="padding-right: 3px;">s13</a>                 </td>             </tr></table><br /><table style="width: 100%;">    <tr>            <td style="width: 50%;">                <h3>                    Resultater                </h3>'
avg = content.join(content.split())
avg = avg.split('Eksamensgennemsnit', 1)[1]
#print avg
avg = avg.split('Efter 7-',1)[0]
avg = extractstr('<td>',' \(', avg).replace(',', '.')
avg = float(avg)

pp = content.replace(" ", "")
pp = pp.split("afdetilmeldte,", 1)[1]
pp = float(pp.split("%afdefremm", 1)[0].replace(',', '.'))
print pp


