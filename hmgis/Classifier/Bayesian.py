# _*_ coding: utf-8 _*_

from numpy import *
import jieba.posseg as pseg
import jieba

class Bayesian:
	def loadDataSet(self):
		postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
		               ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
		               ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
		               ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
		               ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
		               ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
		classVec = [0, 1, 0, 1, 0, 1]    #1 is abusive, 0 not
		return postingList, classVec

	## 寻找出单个文档，其中词汇不重复
	def createVocabList(self, dataSet):
		vocabSet = set([])  #create empty set
		for document in dataSet:
			vocabSet = vocabSet | set(document) #union of the two sets
		return list(vocabSet)

	## 计算一个字符串的单词在词包中的位置
	def setOfWords2Vec(self, vocabList, inputSet):
		returnVec = [0] * len(vocabList)
		for word in inputSet:
			if word in vocabList:
				returnVec[vocabList.index(word)] += 1
			else:
				print "the word: %s is not in my Vocabulary!" % word
		return returnVec

	## 计算先验概率
	## P(B|A) = P(B)P(A|B)/P(B)P(A|B) + P(C)P(A|C)
	def trainNB0(self, trainMatrix, trainCategory):
		numTrainDocs = len(trainMatrix)
		numWords = len(trainMatrix[0])
		## 先验概率
		pAbusive = sum(trainCategory) / float(numTrainDocs)
		p0Num = ones(numWords)
		p1Num = ones(numWords)      #change to ones()
		p0Denom = 2.0;
		p1Denom = 2.0                        #change to 2.0
		## 类型AB的先验概率是根据此类型中词汇在词包中出现的次数除以总次数
		for i in range(numTrainDocs):
			if trainCategory[i] == 1:
				p1Num += trainMatrix[i]
				p1Denom += sum(trainMatrix[i])
			else:
				p0Num += trainMatrix[i]
				p0Denom += sum(trainMatrix[i])
		p1Vect = log(p1Num / p1Denom)         #change to log()
		p0Vect = log(p0Num / p0Denom)          #change to log()
		return p0Vect, p1Vect, pAbusive

	## 比较概率
	def classifyNB(self, vec2Classify, p0Vec, p1Vec, pClass1):
	## 由于所有类型的全概率都是一样的（分母一样），因此可以纯比分子
		p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
		p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
		if p1 > p0:
			return 1
		else:
			return 0

	## 测试单个词汇的类型
	def testingNB(self):
	## 加载已有数据集
		listOPosts, listClasses = self.loadDataSet()
		myVocabList = self.createVocabList(listOPosts)
		trainMat = []
		for postinDoc in listOPosts:
			trainMat.append(self.setOfWords2Vec(myVocabList, postinDoc))
		## 计算已有数据集中的先验概率
		p0V, p1V, pAb = self.trainNB0(array(trainMat), array(listClasses))

		## 测试不同字符串的后验概率
		testEntry = ['love', 'my', 'dalmation']
		thisDoc = array(self.setOfWords2Vec(myVocabList, testEntry))
		print testEntry, '被分类为: ', self.classifyNB(thisDoc, p0V, p1V, pAb)
		testEntry = ['stupid', 'garbage']
		thisDoc = array(self.setOfWords2Vec(myVocabList, testEntry))
		print testEntry, '被分类为: ', self.classifyNB(thisDoc, p0V, p1V, pAb)

class RSSBayesian:
	## 解析RSS源，返回实际的RSS数量
	def loadRSS(self, webpage, file):
		#OUT = "data/bayesian/rss/rss_junshi.txt"
		f = open(file,"w")

		import feedparser
		#mil = feedparser.parse('http://mil.sohu.com/rss/junshi.xml')
		mil = feedparser.parse(webpage)

		count = 0
		for entry in mil["entries"]:
			title = entry["title"]
			title = title.replace('\n','')
			txt = entry["summary_detail"]["value"]
			txt = txt.replace('\n','')
			if len(txt)>1 :
				f.writelines(title + '。' + txt + "\n")
				count = count + 1
		f.close()
		return count

	## 预处理从RSS源获得的数据
	def preProcess(self, filepath, classtag):
		import re
		sentences = [line for line in file(filepath) if len(line)>1]
		jieba.load_userdict("lib/userdict")
		## 使用jieba对文本进行分词
		texts_tokenized = [[word for word in pseg.cut(document) if word.flag in ['n','nr','ns','nt','nz','nl','ng','eng','x'] ] for document in sentences]
		## 停用词
		chnstopwordoc = [line.strip() for line in file('lib/chinesestopwords.txt')]
		stoplist = [course for course in chnstopwordoc]
		## 剔除停用词
		texts_tokenized = [[word for word in document if not word.word in stoplist] for document in texts_tokenized]
		## 剔除长度为1的词汇
		wordlist = [[word.word for word in document if len(word.word)>1 ] for document in texts_tokenized]
		print len(wordlist)
		labels = []
		for i in range(0, len(wordlist)):
			labels.append(classtag)

		return wordlist, labels

	def getData(self, filepath):
		sentences = [line for line in file(filepath)]
		return sentences


	def testEntryProcess(self, text):
		## 使用jieba对文本进行分词
		texts_tokenized = [word for word in pseg.cut(text) if word.flag in ['n','nr','ns','nt','nz','nl','ng','eng','x']]
		## 停用词
		chnstopwordoc = [line.strip() for line in file('lib/chinesestopwords.txt')]
		stoplist = [course for course in chnstopwordoc]
		## 剔除停用词
		texts_tokenized = [t.word for t in texts_tokenized if not t.word in stoplist]
		## 剔除长度为1的词汇
		wordlist = [document for document in texts_tokenized if len(document)>1]
		return wordlist

		## 寻找出单个文档，其中词汇不重复
	def createVocabList(self, dataSet):
		vocabSet = set([])  #create empty set
		for document in dataSet:
			vocabSet = vocabSet | set(document) #union of the two sets
		return list(vocabSet)

	## 计算一个字符串的单词在词包中的位置
	def setOfWords2Vec(self, vocabList, inputSet):
		returnVec = [0] * len(vocabList)
		for word in inputSet:
			if word in vocabList:
				returnVec[vocabList.index(word)] += 1
			else:
				print "词汇: %s is 不在词典中!" % word
		return returnVec

	## 计算先验概率
	## P(B|A) = P(B)P(A|B)/P(B)P(A|B) + P(C)P(A|C)
	def trainNB0(self, trainMatrix, trainCategory):
		numTrainDocs = len(trainMatrix)
		numWords = len(trainMatrix[0])
		## 先验概率
		pAbusive = sum(trainCategory) / float(numTrainDocs)
		p0Num = ones(numWords)
		p1Num = ones(numWords)      #change to ones()
		p0Denom = 2.0;
		p1Denom = 2.0                        #change to 2.0
		## 类型AB的先验概率是根据此类型中词汇在词包中出现的次数除以总次数
		for i in range(numTrainDocs):
			if trainCategory[i] == 1:
				p1Num += trainMatrix[i]
				p1Denom += sum(trainMatrix[i])
			else:
				p0Num += trainMatrix[i]
				p0Denom += sum(trainMatrix[i])
		p1Vect = log(p1Num / p1Denom)         #change to log()
		p0Vect = log(p0Num / p0Denom)          #change to log()
		return p0Vect, p1Vect, pAbusive

	## 比较概率
	def classifyNB(self, vec2Classify, p0Vec, p1Vec, pClass1, labels):
	## 由于所有类型的全概率都是一样的（分母一样），因此可以纯比分子
		p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
		p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
		if p1 > p0:
			return labels[1]
		else:
			return labels[0]

	def classifyNB2(self, vec2Classify, p0Vec, p1Vec, pClass1):
	## 由于所有类型的全概率都是一样的（分母一样），因此可以纯比分子
		p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
		p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
		if p1 > p0:
			return 1
		else:
			return 0

	def loadProcessedData(self):
		dataMat0,labels0 = self.preProcess('data/bayesian/rss/rss_junshi.txt',0)
		dataMat1,labels1 = self.preProcess('data/bayesian/rss/rss_tiyu.txt',1)
		dataMat = dataMat0 + dataMat1
		labels = labels0 + labels1
		print dataMat
		print labels

		myVocabList = self.createVocabList(dataMat)
		## 建立bag of words 矩阵
		trainMat = []
		for postinDoc in dataMat:
			trainMat.append(self.setOfWords2Vec(myVocabList, postinDoc))
		return myVocabList, trainMat, labels

	def SingleClassifier(self):
		## 加载RSS源并将其保存为文本文件
		## 除非是生成新数据，否则不执行这段代码
		#juns_count = rss.loadRSS('http://mil.sohu.com/rss/junshi.xml','data/bayesian/rss/rss_junshi.txt')
		#tiyu_count = rss.loadRSS('http://rss.news.sohu.com/rss/sports.xml','data/bayesian/rss/rss_tiyu.txt' )
		#print juns_count
		#print tiyu_count

		dataMat0,labels0 = self.preProcess('data/bayesian/rss/rss_junshi.txt',0)
		dataMat1,labels1 = self.preProcess('data/bayesian/rss/rss_tiyu.txt',1)
		dataMat = dataMat0 + dataMat1
		labels = labels0 + labels1
		print dataMat
		print labels

		myVocabList = self.createVocabList(dataMat)
		## 建立bag of words 矩阵
		trainMat = []
		for postinDoc in dataMat:
			trainMat.append(self.setOfWords2Vec(myVocabList, postinDoc))
		## 计算已有数据集中的先验概率
		p0V, p1V, pAb = self.trainNB0(array(trainMat), array(labels))

		## 测试不同字符串的后验概率
		testText = "美国军队的军舰今天访问了巴西港口城市，并首次展示了核潜艇攻击能力，飞机，监听。他们表演了足球。"
		testEntry = self.testEntryProcess(testText)
		thisDoc = array(self.setOfWords2Vec(myVocabList, testEntry))
		clabels = ['军事','体育']
		print testText, 'classified as: ', self.classifyNB(thisDoc, p0V, p1V, pAb, clabels)

	## 交叉分类验证
	## 从51个样本中选出41个培训集，10个测试集
	def crossValidClassifier(self):
		data1 = self.getData('data/bayesian/rss/rss_junshi.txt')
		data2 = self.getData('data/bayesian/rss/rss_tiyu.txt')
		data = data1 + data2

		dataMat0,labels0 = self.preProcess('data/bayesian/rss/rss_junshi.txt',0)
		dataMat1,labels1 = self.preProcess('data/bayesian/rss/rss_tiyu.txt',1)
		dataMat = dataMat0 + dataMat1
		labels = labels0 + labels1
		print dataMat
		print labels

		myVocabList = self.createVocabList(dataMat)
		trainingSet = range(51);
		testSet = []           #create test set
		for i in range(10):
			randIndex = int(random.uniform(0, len(trainingSet)))
			testSet.append(trainingSet[randIndex])
			del (trainingSet[randIndex])
		trainMat = [];
		trainClasses = []
		for docIndex in trainingSet:#train the classifier (get probs) trainNB0
			trainMat.append(self.setOfWords2Vec(myVocabList, dataMat[docIndex]))
			trainClasses.append(labels[docIndex])
		p0V, p1V, pSpam = self.trainNB0(array(trainMat), array(trainClasses))

		clabels = ['军事','体育']
		errorCount = 0
		for docIndex in testSet:        #classify the remaining items
			wordVector = self.setOfWords2Vec(myVocabList, dataMat[docIndex])
			type = self.classifyNB2(array(wordVector), p0V, p1V, pSpam)
			if type != labels[docIndex]:
				errorCount += 1
				print "判断类型：", clabels[type]
				print "classification error", data[docIndex]
				print "---------------------------------------"
		print 'the error rate is: ', float(errorCount) / len(testSet)

	## 使用scikti代码进行GaussianNB训练
	def scikitNBClassfier(self):
		myVocabList, trainMat, trainClasses = self.loadProcessedData()
		from sklearn.naive_bayes import GaussianNB
		gnb = GaussianNB()
		X = array(trainMat)
		y = trainClasses

		testText = "美国军队的军舰今天访问了巴西港口城市，并首次展示了核潜艇攻击能力，飞机，监听。他们表演了足球。"
		testEntry = self.testEntryProcess(testText)
		thisDoc = array(self.setOfWords2Vec(myVocabList, testEntry))
		## 拟合并预测
		y_pred = gnb.fit(X, y).predict(thisDoc)
		clabels = ['军事','体育']
		y_pred = gnb.fit(X, y).predict(X)
		print("Number of mislabeled points : %d" % (trainClasses != y_pred).sum())

## 电子邮件测试器
class emailClassfier:
	def textParse(self, bigString):
		import re

		listOfTokens = re.split(r'\W*', bigString)
		return [tok.lower() for tok in listOfTokens if len(tok) > 2]

	def spamTest(self, bayesian):
		docList = [];
		classList = [];
		fullText = []
		for i in range(1, 26):
			wordList = self.textParse(open('data/bayesian/email/spam/%d.txt' % i).read())
			docList.append(wordList)
			fullText.extend(wordList)
			classList.append(1)
			wordList = self.textParse(open('data/bayesian/email/ham/%d.txt' % i).read())
			docList.append(wordList)
			fullText.extend(wordList)
			classList.append(0)
		vocabList = bayesian.createVocabList(docList)#create vocabulary
		trainingSet = range(50);
		testSet = []           #create test set
		for i in range(10):
			randIndex = int(random.uniform(0, len(trainingSet)))
			testSet.append(trainingSet[randIndex])
			del (trainingSet[randIndex])
		trainMat = [];
		trainClasses = []
		for docIndex in trainingSet:#train the classifier (get probs) trainNB0
			trainMat.append(bayesian.setOfWords2Vec(vocabList, docList[docIndex]))
			trainClasses.append(classList[docIndex])
		p0V, p1V, pSpam = bayesian.trainNB0(array(trainMat), array(trainClasses))
		errorCount = 0
		for docIndex in testSet:        #classify the remaining items
			wordVector = bayesian.setOfWords2Vec(vocabList, docList[docIndex])
			if bayesian.classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
				errorCount += 1
				print "分类错误", docList[docIndex]
		print '错误率是: ', float(errorCount) / len(testSet)
		#return vocabList,fullText