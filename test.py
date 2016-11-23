import re
from bs4 import BeautifulSoup

# -*- coding: utf-8 -*-
txt='<a href="https://evaluering.dtu.dk/kursus/26027/37530">                26027 Grundl&#230;ggende kemi E14 (E-14-13)            </a>        </div>        <div>            <a href="https://evaluering.dtu.dk/kursus/26027/78068">                26027 Grundl&#230;ggende kemi F14 (F-14-13)            </a>        </div>                            <div class="bar">Karakterhistorik</div>                    <div>                        <a href="http://karakterer.dtu.dk/Histogram/1/26027/Winter-2016">26027 Grundl&#230;ggende kemi v16</a>                    </div>                    <div>                        <a href="http://karakterer.dtu.dk/Histogram/1/26027/Summer-2016">26027 Grundl&#230;ggende kemi s16</a>                    </div>                    <div>                        <a href="http://karakterer.dtu.dk/Histogram/1/26027/Winter-2015">26027 Grundl&#230;ggende kemi v15</a>                    </div>                    <div>                        <a href="http://karakterer.dtu.dk/Histogram/1/26027/Summer-2015">26027 Grundl&#230;ggende kemi s15</a>                    </div>                    <div>                        <a href="http://karakterer.dtu.dk/Histogram/1/26027/Winter-2014">26027 Grundl&#230;ggende kemi v14</a>                    </div>        </div>    </div>    <div class="col-md-6">        <div class="box">            <div class="bar">Kursusansvarlige</div>                <div class="row" style="margin:20px">'

def extractURLs(pre, post, body):
    #try:
        body = " ".join(body.split())
        body = body.split(pre, 1)[1]
        body = body.split(post, 1)[0]
        #return extractlinks(body)
        #body.pop(0)
   # except:
    #    print "Error formatting exam overview"
def extractlinks(html):
    soup = BeautifulSoup(html,"html.parser")
    anchors = soup.findAll('a')
    links = []
    for a in anchors:
        links.append(a['href'])
    return links



extractURLs("swag","yolo","din mor" 	)