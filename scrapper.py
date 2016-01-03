import requests, six #for scrapping
import lib2to3
import lxml.html as lh # web page readable by python
import pandas as pd 
import sys,urllib
from PyQt4 import QtGui,QtCore


def str_bracket(word):
	list =[x for x in word]
	for char_ind in range (1,len(list)):
		if list[char_ind].isupper():
			list[char_ind]=" " + list[char_ind]
	fin_list=''.join(list).split(' ')
	length=len(fin_list)
	if length>1:
		fin_list.insert(1,'(')
		fin_list.append(')')
	return ' '.join(fin_list)
def str_break(word):
	list= [x for x in word]
	for char_ind in range (1,len(list)):
		if list[char_ind].isupper():
			list[char_ind]=" " + list[char_ind]
	fin_list = ''.join(list).split(' ')
	return fin_list



url='http://pokemondb.net/pokedex/all'
page = requests.get(url) #Create a handle, page, to handle the contents of the website
doc = lh.fromstring(page.content) #Store the contents of the website under doc
tr_elements = doc.xpath('//tr') #Parse data that are stored between <tr>..</tr> of the site's HTML code

col=[]
i=0

for t in tr_elements[0]:
	i+=1
	name = t.text_content()
	print (i,":",name)
	col.append((name,[]))

for i in range(1,len(tr_elements)):
	temp = tr_elements[i]
	if len(temp)!=10:
		break
	j=0
	for k in temp.iterchildren():
		data=k.text_content()
		if(j>0):
			try:
				data=int(data)
			except:
				pass
		col[j][1].append(data)
		j+=1
for (title,C) in col:
	print (len(C))
Dict={title:column for (title,column) in col}
df = pd.DataFrame(Dict) 
df['Name'] = df['Name'].apply(str_bracket)
df['Type'] = df['Type'].apply(str_break)
df.to_json('Data.json')
df = pd.read_json('Data.json')
df = df.set_index(['#'])
print (df.head())
