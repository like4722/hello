#-*- coding:utf-8 -*-
import numpy as np
import pandas as pd 
import re,os
from datetime import datetime
from datetime import date
from datetime import timedelta
from tqdm import tqdm
#定义函数#
def process(x):
	x = x[:-1]
	for i in range(len(x)):
		if x[-1] == ' ' or x[-1] == '+':
			x = x[:-1]
		else:
			break
	return x
def trim(x):
	for i in range(len(x)):
		if x[0] == ' ':
			x = x[1:]
		else:
			break
	return x
def write(x):
	data.loc[x,'航班日期']=aimtime;data.loc[x,'航段']=route;
	data.loc[x,'机型']=ca[9:12];data.loc[x,'时刻']=ca[14:18];
	data.loc[x,'承运人']=ca[1:3];data.loc[x,'航班号']=str(ca[3:7]);
	data.loc[x,'下载日期']=downtime;dt=aimtime-downtime
	data.loc[x,'提前天数']=dt.days
	a=ca[21:];b=a.split('//');
	reference.loc[x,'运力']=b[0];reference.loc[x,'舱位']=b[1];


#文本清洗第一步#
a = ['CZ','ZH','CA','MU','FM','MF']
path='RBJ//'
lists=os.listdir(path)
alldata=pd.DataFrame(columns=['航班日期','航段','下载日期','承运人','航班号','提前天数','F', 'J', 'C', 'D', 'I',
       'O', 'W', 'S', 'Y', 'P', 'B', 'M', 'H', 'U', 'A', 'L', 'E', 'V', 'Z',
       'T', 'R', 'G', 'K', 'Q', 'N', 'X','座位数'])
for i in tqdm(lists):
	reference = pd.DataFrame(columns=['舱位','运力'])
	data = pd.DataFrame()
	df = open(path+i+'//rbj.log','r')	
	x = 0
	lines = df.readlines()
	df.close()
	for s in lines:
		s = process(s)
		if s.count(',') == 2:
			downstrp=s
			ttt=datetime.strptime(downstrp,'%Y %B %d, %A, %H:%M:%S')
			ttt=ttt-timedelta(1)
			downtime=ttt.date()
			continue
		if s[1:4] == 'RBJ':
			timestrp = s[4:11]
			tt=datetime.strptime(timestrp,'%d%b%y')
			aimtime=tt.date()
			route = s[11:17]
			continue
		if s[1:3] in a:
			c = [];c1 = []
			c1 = s
			c.append(c1)
			continue
		if not s[1:3] in a  and  '/' in s:
			c1 = trim(s)
			c.append(c1)
		if s[-2:] != '//':
			continue
		if len(c) == 2:
			ca = c[0]+c[1]
			write(x)
			x+=1		
		if len(c) == 3:
			ca = c[0]+c[1]+c[2] 
			write(x)
			x+=1		

	#第二布梳洗舱位#
	def f(x):
		x=x[-1]
		return x

	pattern1=re.compile(r'[A-Z]{1,2}')
	pattern2=re.compile(r'[0-9]{1,3}')
	c_fin=pd.DataFrame(index=range(len(reference)),columns=['F', 'J', 'C', 'D', 'I',
	       'O', 'W', 'S', 'Y', 'P', 'B', 'M', 'H', 'U', 'A', 'L', 'E', 'V', 'Z',
	       'T', 'R', 'G', 'K', 'Q', 'N', 'X'])
	c_fin=c_fin.fillna(0)
	y_fin=pd.DataFrame(index=range(len(reference)),columns=['F','J','W','Y'])
	y_fin=y_fin.fillna(0)
	offer=pd.DataFrame(index=range(len(reference)),columns=['座位数'])

	i=0
	while i < len(reference):
		cang=reference.loc[i,'舱位']
		c_class=pattern1.findall(cang)
		c_class=list(map(f,c_class))
		c_seats=pattern2.findall(cang)
		c_seats=list(map(int,c_seats));
		c=pd.DataFrame(c_seats,index=c_class,columns=[i])
		c=pd.DataFrame(c.T)
		c_fin.loc[i]=c.loc[i]
		i+=1

	i=0
	while i < len(reference):
		yun=reference.loc[i,'运力']
		y_class=pattern1.findall(yun)
		y_seats=pattern2.findall(yun)
		y_seats=list(map(int,y_seats));
		y=pd.DataFrame(y_seats,index=y_class,columns=[i])
		y=pd.DataFrame(y.T)
		y_fin.loc[i]=y.loc[i]
		offer.loc[i,'座位数']=sum(y_seats)
		i+=1

	data=data.combine_first(c_fin)
	data=data.combine_first(offer)
	data=data.fillna(0)
	data=data.drop_duplicates()
	alldata=pd.concat([alldata,data],ignore_index=True,axis=0)
	alldata.to_csv('rbj.csv',encoding='gbk',index=None,columns=['航班日期','航段','下载日期','承运人','航班号','提前天数','F', 'J', 'C', 'D', 'I',
       'O', 'W', 'S', 'Y', 'P', 'B', 'M', 'H', 'U', 'A', 'L', 'E', 'V', 'Z',
       'T', 'R', 'G', 'K', 'Q', 'N', 'X','座位数'])