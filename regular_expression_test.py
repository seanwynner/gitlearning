#coding=utf
import os
import re
import time

'''
执行时间统计实例
startTime=time.clock()
endTime=time.clock()
print ("Excute time==%s"%(endTime-startTime))
'''

a="When Harold Fry leaves home one morning to post a letter, with his wife hoovering upstairs, he has no idea that he is about to walk from one end of the country to the other. He has no hiking boots or map, let alone a compass, waterproof or mobile phone. All he knows is that he must keep walking. To save someone elses life."
b="mobil"
#b="keep"
#b="xxxxxxxx"



def search1(keyWord,txtLine):

	if len(keyWord)<=4:
		keyWordP1=keyWord
	else:
		keyWordP1=keyWord+"\S{0,4}"
		#keyWordP1=keyWord


	splitLen=20
		
	splitIndexList=[]
	txtLineSplitList=[]

	aInt=int(len(txtLine)/splitLen)

	for i in range(0,aInt+1):
		splitIndex=txtLine.find(" ",(i+1)*splitLen,(i+2)*splitLen)
		#print ("splitIndex==%s"%splitIndex)
		if splitIndex!=-1:
			splitIndexList.extend([splitIndex])

	splitIndexList=splitIndexList+[len(txtLine)]
		
	#print ("splitIndexList=%s"%splitIndexList)

	searchP1=re.compile("^"+keyWordP1+"\s",re.I)
	searchP2=re.compile("\s"+keyWordP1+"\s",re.I)
	searchP3=re.compile("\s"+keyWordP1+"$",re.I)
	#print ("searchp==%s"%searchP2)

	for i in range(0,len(splitIndexList)):
			if i>=1:
				beginIndex=splitIndexList[i-1]
			else:
				beginIndex=0
			endIndex=splitIndexList[i]
			
			#print("txline==%s"%txtLine)
			#print ("%s----%s"%(beginIndex,endIndex))
			
			
			r=searchP1.search(txtLine,beginIndex,endIndex)
			if r==None:
				r=searchP2.search(txtLine,beginIndex,endIndex)
				if r==None:
					r=searchP3.search(txtLine,beginIndex,endIndex)
			#r=searchP2.search(txtLine)
			#r=re.search(b,a)
			#print("r===%s"%r)
			
			if r!=None:
				break
					
	return r




def search2(keyWord,txtLine):

	if len(keyWord)<=4:
		keyWordP1=keyWord
	else:
		keyWordP1=keyWord+"\S{0,4}"
		#keyWordP1=keyWord
		#print ("splitIndexList=%s"%splitIndexList)

	searchP1=re.compile("^"+keyWordP1+"\s",re.I)
	searchP2=re.compile("\s"+keyWordP1+"\s",re.I)
	searchP3=re.compile("\s"+keyWordP1+"$",re.I)
	#print ("searchp==%s"%searchP2)

	
	r=None


	r=searchP1.search(txtLine)
	if r==None:
		r=searchP2.search(txtLine)
		if r==None:
			r=searchP3.search(txtLine)
	return r
	

def search3(keyWord,txtLine):
	searchResult=[]
	searchFlag=0
	keyWord=keyWord.lower()
	txtLineLower=txtLine.lower()
	
	i1=txtLineLower.find(keyWord)
	
	if i1==-1:
		return
		
	#logging.debug("i1===%s"%i1)
	if i1==0:
		searchHeadFlag=1
		#logging.debug ("i1===%s"%i1)
	else:
		if txtLine[i1-1].isalpha():
			searchHeadFlag=0
			return searchResult
		else:
			searchHeadFlag=1
			
	#logging.debug ("seraccHeadFlag==%s"%searchHeadFlag)		
	
	#判断是否是最后一个单词
	if (i1+len(keyWord))==len(txtLine):
		searchTailFlag=1
	else:
		i3=txtLineLower.find(" ",i1)
		#print("---i1---i3:%s---%s"%(i1,i3))
		#logging.debug("i3===%s"%i3)
		if i3==-1:	
			i3=len(txtLineLower)-1
		else:
			i3=i3-1
			
		#i3+1-i1为匹配到的单词长度
		a=i3+1-i1-len(keyWord)
		#print("i1---i3:%s---%s"%(i1,i3))
		#如果匹配词与keyword匹配长度相差在4个字母以内，认为匹配成功，否则认为失败。
		if a>=4:
			searchTailFlag=0
		else:
			#keyword在四个字母以上，认为匹配成功，如果在四个字母一下，需要全匹配才算成功
			if len(keyWord)>4:
				searchTailFlag=1
			else:
				if a==0:
					searchTailFlag=1
				else:
					searchTailFlag=0
					return searchResult

				
		#logging.debug ("searchTailFlag==%s"%searchTailFlag)		
		
		
		#print ("searchTailFlag==%s"%searchTailFlag)	
		if searchHeadFlag==1 and searchTailFlag==1:
			rString=txtLine[i1:i3+1]
			
			#logging.debug ("sTring==%s--%s--%s---%s"%rString,%txtLine,%i1,%i3)
			#logging.debug ("txtLine==%s"%txtLine)
			searchResult=[rString,i1,i3]
		else :
			searchResult=[]
	#logging.debug ("searchResult=%s"%searchResult)		
	return searchResult


def search4(keyWord,txtLine):
	searchResult=[]
	searchFlag=0
	keyWord=keyWord.lower()
	txtLineLower=txtLine.lower()

	i1=txtLineLower.find(keyWord)
	
	
	#----------------------------------------------
	#没找到，返回
	if i1==-1:
		searchResult=[]
		return searchResult
		
	#logging.debug("i1===%s"%i1)
	
	#如果找到，处于行首，不在需要匹配头部
	if i1==0:
		searchHeadFlag=1
		#logging.debug ("i1===%s"%i1)
	
	
	if i1>0: 
		#否则判断前面一个字符是否是字母，如果是，则说明是从中间匹配的，这种情况也不成功，需要返回
		if txtLine[i1-1].isalpha():
			searchHeadFlag=0
			searchResult=[]
			return searchResult
		else:
			searchHeadFlag=1
			
	#logging.debug ("seraccHeadFlag==%s"%searchHeadFlag)		
	
	#接下来匹配尾部
	
	#判断这个单词后是否还有其他字符，如果没有，说明是最后一个单词，尾部也匹配
	if (i1+len(keyWord))==len(txtLine):
		searchTailFlag=1
		searchResult=[txtLine[i1:len(txtLine)],i1,len(txtLine)-1]
		return searchResult
	#如果长度不等，说明后面还有字符，则寻周后面第一个空白，字符，进行截取	
	else:
		i3=txtLineLower.find(" ",i1)
		#print("---i1---i3:%s---%s"%(i1,i3))
		#logging.debug("i3===%s"%i3)
		if i3==-1:	
			i3=len(txtLineLower)-1
		else:
			i3=i3-1
			
		txtLineWord=txtLine[i1:i3+1]
		#print("txtLineWord==%s"%txtLineWord)
		#匹配keyWord和txtLineWord
		
		#如果完全相等，说明匹配
		if keyWord.lower()==txtLineWord.lower():
			searchTailFlag=1
			searchResult=[txtLineWord,i1,i3]
			return searchResult
		
		#否则进行正则比较，看后面是否匹配
		
		keyWordP1=keyWord+"[a-z]*"
		
		#keyWordP1=keyWord
		#print ("splitIndexList=%s"%splitIndexList)

		keyWordP1=re.compile(keyWordP1,re.I)
		
		#提取keyword+后续连续的所有字母组成的字符串
		r=keyWordP1.search(txtLineWord)
		if r==None:
			searchResult=[]
			return searchResult		
		
		#如果字符串长度比keyword还长四个字符以上，说明匹配太长了，作为匹配不成功处理
		if len(r.group(0))-4>=len(keyWord):
			searchResult=[]
			return searchResult		
		#如果相差四个字符以内，说明是匹配的，但如果keyWord本身太短，在4个及4个字母内，也有可能是前缀之类误匹配，这种情况下需要完全匹配
		else:
			if len(keyWord)<=4:
				if r.group(0).lower()!=keyWord.lower():
					searchResult=[]
					return searchResult
			
			searchResult=[r.group(0),i1,i1+len(r.group(0))-1]
			return searchResult		
		
def search41(keyWord,txtLine):
	searchResult=[]
	searchFlag=0
	keyWord=keyWord.lower()
	txtLineLower=txtLine.lower()

	i1=txtLineLower.find(keyWord)
	
	
	#----------------------------------------------
	#没找到，返回
	if i1==-1:
		searchResult=[]
		return searchResult
		
	#logging.debug("i1===%s"%i1)
	
	#如果找到，处于行首，不在需要匹配头部
	if i1==0:
		searchHeadFlag=1
		#logging.debug ("i1===%s"%i1)
	
	
	if i1>0: 
		#否则判断前面一个字符是否是字母，如果是，则说明是从中间匹配的，这种情况也不成功，需要返回
		if txtLine[i1-1].isalpha():
			searchHeadFlag=0
			searchResult=[]
			return searchResult
		else:
			searchHeadFlag=1
			
	#logging.debug ("seraccHeadFlag==%s"%searchHeadFlag)		
	
	#接下来查找匹配单词尾部
	
	#判断这个单词后是否还有其他字符，如果没有，说明是最后一个单词，尾部也匹配
	if (i1+len(keyWord))==len(txtLine):
		searchTailFlag=1
		searchResult=[txtLine[i1:len(txtLine)],i1,len(txtLine)-1]
		return searchResult
	#如果长度不等，说明后面还有字符，则寻周后面第一个空白，字符，进行截取	
	else:
		txtLineLower1=txtLineLower[i1:len(txtLineLower)]
		#print("i1----------======%s"%i1)
		#print("txtLineLower1----------======%s"%txtLineLower1)
		r=re.search("[^a-z]",txtLineLower1)
		
		#print("r=====%s"%r)	
		#i3=r.start()
		
		#print("---i1---i3:%s---%s"%(i1,i3))
		#logging.debug("i3===%s"%i3)
		if r==None:	
			i3=len(txtLineLower)-1
		else:
			i3=r.start()-1+i1
		
		txtLineWord=txtLine[i1:i3+1]
		#print("txtLineWord==%s"%txtLineWord)
		#匹配keyWord和txtLineWord
		
		txtLineWordLen=i3-i1
		#print("txtkeyWord---txtLineWordLen--%s------%s"%(txtLineWord,txtLineWordLen))
		#如果字符串长度比keyword还长四个字符以上，说明匹配太长了，作为匹配不成功处理
		if txtLineWordLen-4>=len(keyWord):
			searchResult=[]
			return searchResult		
		#如果相差四个字符以内，说明是匹配的，但如果keyWord本身太短，在4个及4个字母内，也有可能是前缀之类误匹配，这种情况下需要完全匹配
		else:
			if len(keyWord)<=4:
				if txtLineWordLen!=len(keyWord):
					searchResult=[]
					return searchResult
			
			searchResult=[txtLineWord,i1,i1+len(txtLineWord)-1]
			return searchResult				
def search5(keyWord,txtLine):
	searchResult=[]
	searchFlag=0
	keyWord=keyWord.lower()
	txtLineLower=txtLine.lower()

	i1=txtLineLower.find(keyWord)
	
	if len(keyWord)<=4:
		p=keyWord
	else:
		p=keyWord+"[a-z]*"
		
	p="(^|[^a-z])"+p
	#p=keyWord
	p=re.compile(p)
	
	r=p.search(txtLine)
	
	return r
	
def search6(keyWord,txtLine):
	searchResult=[]
	searchFlag=0
	keyWord=keyWord.lower()
	txtLineLower=txtLine.lower()

	i1=txtLineLower.find(keyWord)
	
	
	#----------------------------------------------
	#没找到，返回
	if i1==-1:
		return None
	
	if len(keyWord)<=4:
		p=keyWord
	p=keyWord+"[a-z]*"
		
	p="(^|[^a-z])"+p
	#p=keyWord
	p=re.compile(p)
	
	r=p.search(txtLine,i1-1)		
	return r
			
flooptimes=10000
#------------------------------------------------------
startTime=time.clock()

for kkk in range(flooptimes):
	r=search1(b,a)

endTime=time.clock()
print ("111Excute time==%s"%(endTime-startTime))

print("r===%s"%r)

#------------------------------------------------------
startTime=time.clock()

for kkk in range(flooptimes):
	r=search2(b,a)

endTime=time.clock()
print ("222Excute time==%s"%(endTime-startTime))

print("r===%s"%r)

#------------------------------------------------------
startTime=time.clock()

for kkk in range(flooptimes):
	r=search3(b,a)

endTime=time.clock()
print ("333Excute time==%s"%(endTime-startTime))

print("r===%s"%r)

for kkk in range(flooptimes):
	r=search4(b,a)

endTime=time.clock()
print ("4444Excute time==%s"%(endTime-startTime))

print("r===%s"%r)


for kkk in range(flooptimes):
	r=search41(b,a)

endTime=time.clock()
print ("41414141Excute time==%s"%(endTime-startTime))

print("r===%s"%r)

for kkk in range(flooptimes):
	r=search5(b,a)

endTime=time.clock()
print ("5555Excute time==%s"%(endTime-startTime))

print("r===%s"%r)

for kkk in range(flooptimes):
	r=search6(b,a)

endTime=time.clock()
print ("6666Excute time==%s"%(endTime-startTime))

print("r===%s"%r)