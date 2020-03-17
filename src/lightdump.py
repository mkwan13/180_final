from lxml import etree
import lxml
import shutil
from py7zr import unpack_7zarchive
from collections import Counter

def getDump(context):
	cont = etree.iterparse(context, tag='{http://www.mediawiki.org/xml/export-0.10/}page', encoding='utf-8')
	page_num = 1
	for event, elem in context:
	    if page_num % 1 == 0:
	        revs = makeDump(elem)
	eds = checkRevisions(revs)
	return eds

def makeDump(elem):
    revs = []
    for revision in elem.findall("{http://www.mediawiki.org/xml/export-0.10/}revision"):
        flag = 0
        page = revision.getparent()
        title = page.find("{http://www.mediawiki.org/xml/export-0.10/}title")
#         if title.text == "Anarchism":
        if title.text not in revs:
            print(title.text)
            revs.append(title.text)
        text = revision.find("{http://www.mediawiki.org/xml/export-0.10/}text")
        timestamp = revision.find("{http://www.mediawiki.org/xml/export-0.10/}timestamp")
        contrib = revision.find("{http://www.mediawiki.org/xml/export-0.10/}contributor")
        user = contrib.find("{http://www.mediawiki.org/xml/export-0.10/}username")
        if user is None:
            user = contrib.find("{http://www.mediawiki.org/xml/export-0.10/}ip")
        rev = [timestamp.text, '0', text.text, user.text]
        revs.append(rev)
    return revs

def checkRevisions(revs):
    eds = []
    num_title = 0
    ind = 0
    for i, rev in enumerate(revs):
        flag = 0
        if type(rev) is not str:
            if rev[2] in eds:
                rev[1] = '1'
                rev[2] = eds.index(rev[2])-1
                flag = 1
            eds.append(rev[2])
            if flag == 0:
                rev[2] = ind-1
        else:
            eds = []
            ind = 0
        ind += 1
    return revs

