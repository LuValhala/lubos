# -*- coding: utf-8 -*-

import basc_py4chan
import random


def initializeBoardData():
	boards = basc_py4chan.get_all_boards()
	for i in boards:
		if i.is_worksafe:
			word = i.title #or i.name
			print word #or save to a txt file
	
def loadBoardShortName():
	boards = open("boardsShortName.txt", "r") 
	listOfBoards = boards.read()
	return listOfBoards.splitlines()
	
def loadBoardFullName():
	boards = open("boardsFullName.txt", "r")
	listOfBoards = boards.read()
	return listOfBoards.splitlines()

######	
	
def isCorrectInput(inputFromUser):
	try:
		if isinstance(inputFromUser, int) and False == isBoardChosen and inputFromUser != 3:
			return False
	except:
		print "input "+ inputFromUser + " seems to be wrong by user: " + userId + " isBoardChosen: " + isBoardChosen + "because of number being chosen as a board"
		return False
	return True
	
def containsMagicWords(inputFromUser):
	if inputFromUser == "help":
		reply("Hi, this is how to use me: \n" +\
		"name of the board separated by space and then words as topics you wish to see \n" +\
		"for example: i moon sun galaxy \n" +\
		"other commands are listed bellow: \n" +\
		"boards <- shows you all the Safe for work boards to choose from \n" +\
		"about <- tells you about me and about the creator of myself \n" +\
		"cheer <- i will cheer you up!")
		return True
	if inputFromUser == "boards":
		boardsShortName = loadBoardShortName()
		boardsFullName = loadBoardFullName()
		replyString = "Availible board(topics) are: \n"
		for i in range(len(boardsFullName)):
			replyString += boardsShortName[i]
			replyString += (" = ")
			replyString += (boardsFullName[i])
			replyString += ("\n")
		reply(replyString)
		return True
	if inputFromUser == "about":
		print "sas"
		reply("I am a bot invented as the last project in the CS50 course from Harward. My creator is Mgr. Lubos Valco from Slovakia. " + \
			"Please note that any replied text is only copied from administrated but still anonymous board. The filter is set to send only " +\
			"worksafe posts but it may still contain informations which anyone may find triggering or disturbing. Proceed with caution. I hope you will " +\
			"enjoy my work to its fullest potential :) L.")
		return True
	if inputFromUser == "quote":
		reply("not supported yet")
		return True
	if inputFromUser == "cheer":
		reply("Do your best today! :) I know you can achieve your dreams so good luck with whatever you wish to do. ^^ ")
		return True
	else:
		return False
		
def getBoard(inputFromUser, userId, isBoardChosen):
	
	splittedInput = inputFromUser.split(" ", 1)
	
	if splittedInput[0] == "board":
		handleBoardInput(inputFromUser, userId, isBoardChosen)
		return "board selection"
	
	if splittedInput[0] in boardsShortName:
		return splittedInput[0]
	else:
		print "input "+ inputFromUser + " seems to be wrong by user: " + userId + " isBoardChosen: " + isBoardChosen
		return False
		
def handleBoardInput(inputFromUser, userId, isBoardChosen):
#need inmemmory database, if exist, rewrite, otherwise creat db(if db is null) and store, db=[]
#vola sa to z getBoard()
	print "as "

def getMessage(inputFromUser):
	try:
		message = inputFromUser.split(" ")
		message.pop(0)
		return message
	except:
		print "cant get message from input :" + inputFromUser
		return []

def getFiveWordsFromListOfWords(listOfWords):
	returnList = []
	if len(listOfWords) >= 5:
		for i in range(5):
			theWord = random.choice(listOfWords)
			returnList.append(theWord)
			listOfWords.remove(theWord)
		return returnList
	else:
		return listOfWords

def getRandomThreadBasedOnSelectedWords(boardName, chosenWords, allThreadsFromChosenBoard):
	topics=[]
	for word in chosenWords:
		for thread in allThreadsFromChosenBoard:
			if thread.topic.text_comment != None:
				if word in thread.topic.text_comment:
					topics.append(thread) #thread.text_comment
	print topics, "**********************" #contains short chosen threads
	if not topics:
		return False
	chosenThreadShort = random.choice(topics)
	board = basc_py4chan.Board(boardName)
	chosenThread = board.get_thread(chosenThreadShort.id)
	print chosenThread
	return chosenThread
	
def tryToRespondCorrectly(boardName, message):
	allThreadsFromChosenBoard = basc_py4chan.Board(boardName).get_all_threads()

	# works print postsWithIds
	chosenWords = getFiveWordsFromListOfWords(message)
	print chosenWords
	#print postsWithIds.values()
	chosenThread = getRandomThreadBasedOnSelectedWords(boardName, chosenWords, allThreadsFromChosenBoard)
	if not chosenThread:
		return False
	replyToUser = ""
	posts = chosenThread.all_posts
	fivePosts = []
	if len(posts) > 5:
		while len(fivePosts)<5:
			post = random.choice(posts)
			if post not in fivePosts:
				fivePosts.append(post)
	else:
		fivePosts = posts
	for post in fivePosts:
		if post.name:
			replyToUser += post.name
		else:
			replyToUser += "Anonymous"
		replyToUser += " says:\n"
		replyToUser += post.text_comment
		replyToUser += "\n\n"
	return [fivePosts, replyToUser.encode('utf-8')]##################
	
def returnedBoardAndRepliedCorrectly(inputFromUser, userId, isBoardChosen):
	global responseToUser
	board = getBoard(inputFromUser, userId, isBoardChosen)
	if board == "board selection":
		return True
	if board == False:
		return False
	print "THE BOARD **************" + board
	message = getMessage(inputFromUser) 
	if not message:
		return False
	print "THE MESSAGE LIST **********"
	print message
	responded = tryToRespondCorrectly(board, message)	
	if responded:
		responseToUser=responded
		return True
	else:
		return False

def initializeReply(inputFromUser, userId, isBoardChosen):
	if not isCorrectInput(inputFromUser):
		print "does not have a correct input"
		return False
	if containsMagicWords(inputFromUser):
		print "contains magic words"
		return True
	#mozno check usera este?
	if returnedBoardAndRepliedCorrectly(inputFromUser, userId, isBoardChosen):
		return True
	else:
		print "should return a gif"
		#return >nice gif
	
global responseToUser
boardsShortName = loadBoardShortName()
boardsFullName = loadBoardFullName()
def reply(s):
	responseToUser = s

#inputFromUser1="x spooky scary skellington conspiracy bush trump"
#inputFromUser2="int spooky scary skellington conspiracy bush trump"
#inputFromUser3="156 spooky scary skellington conspiracy bush trump"
#inputFromUser4="☻♥☺♦♠◘•○♠♂"
#board = basc_py4chan.Board(getBoard(inputFromUser))#TODO:fix user input !!!! upravit help aby fungoval + upravit reply aby obsahoval 3params...
#print initializeReply(inputFromUser1, 1, True)