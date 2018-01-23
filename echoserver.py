from flask import Flask, request, render_template
import json
import requests
import basc_py4chan
import random

responseToUser = ''
isWorksafe = True
app = Flask(__name__)
app.debug = True
# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAAI1qYtqvqEBABquYwjOGmg8gZBxDm2mR0s7UE7dHDs9HybbTBgoQkIVZC2IWk6fjURxIZAStfMrsxs7KSKLfv8DG6hmKeruP4KIZAwDMWOKZBeof1gmjMk6ExIbexsE4FTW9oMVh2LVjXFZBuSqn1zDiZBYhcKaPO9uVdfcg9YDQZDZD'

@app.route('/privacy_policy', methods=['GET'])
def privacy_handle():
    return render_template("privacyPolicy.html")
	
@app.route('/terms_of_service', methods=['GET'])
def services_handle():
    return render_template("termsOfService.html")
	
@app.route('/home', methods=['GET'])
def home_handle():
    return render_template("home.html")

@app.route('/', methods=['GET'])
def handle_verification():
  print "Handling Verification."
  if request.args.get('hub.verify_token', '') == 'slava_bohom_a_predkom_nasim':
    print "Verification successful!"
    return request.args.get('hub.challenge', '')
  else:
    print "Verification failed!"
    return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
	print "Handling Messages"
	global responseToUser
	payload = request.get_data()
	print payload, "payload *****"
	for sender, message in messaging_events(payload):
		try:
			#print "Incoming from %s: %s" % (sender, message)
			initializeReply(message, 1, True)
			#print "Replying with string: %s" (responseToUser)
			print "trying to send message"
			send_message(PAT, sender, responseToUser)
		except Exception, e:
			print "some sending error", str(e)
	return "ok"

def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
  """Send the message text to recipient with id recipient.
  """
  print "sending message from function"
  print token
  print recipient
  print text 
  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text} #.decode('unicode_escape')
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print "why is this here"
    print r.text
######################################################################
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

def loadForbiddenWords():
	boards = open("forbidden.txt", "r")
	listOfBoards = boards.read()
	return listOfBoards.splitlines()
	
######################################################################
	
def isCorrectInput(inputFromUser, isBoardChosen):
	inputFromUser = inputFromUser.lower()
	try:
		if isinstance(inputFromUser, int) and False == isBoardChosen and inputFromUser != 3:
			return False
	except:
		print "input "+ inputFromUser + " seems to be wrong by user: " + userId + " isBoardChosen: " + isBoardChosen + "because of number being chosen as a board"
		return False
	return True
	
def containsMagicWords(inputFromUser):
	inputFromUser = inputFromUser.lower()
	if inputFromUser == "gif":
		url = returnRandomGifUrl()
		reply("here is a totaly random gif or video for you " + url)
		return True
	if inputFromUser == "bug":
		reply("Let me know at lubos.valco@gmail.com with a screenshot and a description of your problem.")
		return True
	if inputFromUser == "help":
		reply("Hi, this is how to use me: \n" +\
        "1. Short name of the board separated by space 2. Then words as topics you wish to check. \n" +\
        "For example: o volvo tesla  \n" +\
        "If you can't get an answer: 1. try to include more words as topic. 2. Use the keyword of the board to get anything random. For example: 'o car', 'diy do it yourself', 'vg game'. " +\
        "Or just try again, if it still doesn't work, please, use the bug command. \n" +\
        "Other commands are listed bellow: \n" +\
        "boards <- shows you all the 'Safe for work' boards to choose from \n" +\
        "about <- tells you about me, the bot and about the creator of myself \n" +\
        "cheer <- I will cheer you up! \n" +\
        "gif <- I will give you a totaly random .gif or a video! You never know what you receive. ^^ \n" +\
        "bug <- Found a bug?")
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
		reply("I am a bot invented as the last project in the Harward's CS50 course. My creator is Mgr. Lubos Valco from Slovakia. " + \
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
	return False
		
def getBoard(inputFromUser, userId, isBoardChosen):
	boardsShortName = loadBoardShortName()
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
#need inmemmory database for ids of users and their boards, if exist, rewrite, otherwise creat db(if db is null) and store, db=[]
	pass
	
def getMessage(inputFromUser):
	try:
		message = inputFromUser.split(" ")
		message.pop(0)
		return message
	except:
		print "cant get message from input: " + inputFromUser
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
	if not topics:
		return False
	chosenThreadShort = random.choice(topics)
	board = basc_py4chan.Board(boardName)
	chosenThread = board.get_thread(chosenThreadShort.id)
	return chosenThread

def isPostForbidden(message):
	global isWorksafe
	if not isWorksafe:
		return True
	allWords = message.split(" ")
	forbiddenWords = loadForbiddenWords()
	for forbiddenWord in forbiddenWords:
		if forbiddenWord in allWords:
			return True
	return False
			
	
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
	OP = posts[0].text_comment
	fivePosts = []
	#get five posts that are not rude
	if len(posts) > 5:
		counter = 0
		while len(fivePosts)<5:
			if len(posts) == 0:
				break
			post = random.choice(posts)
			if isPostForbidden(post.text_comment):
				posts.remove(post)
				continue
			fivePosts.append(post)
	else:
		fivePosts = posts
	
	if len(fivePosts) < 2:
		url = returnRandomGifUrl()
		reply("Something weird happened, here is a gif for you as an apology: " + url)
		return False
	
	replyToUser += "Original poster said: \n"
	replyToUser += OP
	replyToUser += "\n\n"
	for post in fivePosts:
		if post.name:
			replyToUser += post.name
		else:
			replyToUser += "Anonymous"
		replyToUser += " says:\n"
		replyToUser += post.text_comment
		replyToUser += "\n\n"
	return [fivePosts, replyToUser.encode('utf-8')]##################

def returnRandomGifUrl():
	topics=[]
	board = basc_py4chan.Board('wsg').get_all_threads()
	goodGifThreads = ['chill', 'music', 'nostalgia', 'fun', 'ylyl']
	for word in goodGifThreads:
		for thread in board:
			if thread.topic.text_comment != None:
				if word in thread.topic.text_comment:
					topics.append(thread)
	if not topics:
		reply("I had problems searching for reply, contact the author to fix this, thank you")
	
	chosenThreadShort = random.choice(topics)
	board = basc_py4chan.Board('wsg')
	chosenThread = board.get_thread(chosenThreadShort.id)
	isRandomlyChosen = False
	for post in chosenThread.all_posts: #randomly skips and if it didnt find anything, take OP
		if post.is_op:
			chosenPost = post
		if 5 == random.randint(0, 5) and not isRandomlyChosen:
			if post.has_file:
				chosenPost = post
	url = chosenPost.file.file_url
	return url

def returnedBoardAndRepliedCorrectly(inputFromUser, userId, isBoardChosen):
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
		reply(responded[1])
		print "i did respond"
		return True
	else:
		return False
		print "i did not respond"

def initializeReply(inputFromUser, userId, isBoardChosen):
	inputFromUser = inputFromUser.lower()
	if not isCorrectInput(inputFromUser, isBoardChosen):
		print "does not have a correct input"
		return False
	if containsMagicWords(inputFromUser):
		print "contains magic words"
		return True
	if returnedBoardAndRepliedCorrectly(inputFromUser, userId, isBoardChosen):
		print "replied correctly"
		return True
	else:
		print "didnt find anything, trying to give giff"
		url = returnRandomGifUrl
		reply("Well well, i tried my best but i didn't find a good reply. Here is a gif for you" + url)
		return False
def reply(s):
	global responseToUser
	responseToUser = s
	return

if __name__ == '__main__':
  app.run()
