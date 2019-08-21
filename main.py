# Import needed packages
import praw
import time
import re
import passwords # Custom file with the 3 variables specified below

# Creates an instance of a reddit account
thisUser = 'Cornell_class_Bot'

reddit = praw.Reddit(client_id=passwords.client_id,
                     client_secret=passwords.client_secret,
                     username=thisUser,
                     password=passwords.password,
                     user_agent='Made by /u/DubitablyIndubitable')

subreddit = reddit.subreddit('Cornell')

# Declares neccesary global variables
checkedPosts = []
checkedComment = []
count = 0
commentCount = 0
output = ""

# Common 4-digit numbers mentioned in posts that could create a false-positive
invalidNums = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1999', '2000', '2001', '2002', '2003',
               '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
               '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '1000', '3000', '4000',
               '5000', '6000']

# Removes duplicate numbers from lists. Used incase the class number is mentioned multiple times in a post
def remove_duplicates(x):
    return list(set(x))

# Removes the commonly mentioned 4-digit numbers listed above from the numbers detected to be classes
def remove_nums(x):
    for num in x:
        if num in invalidNums:
            x.remove(num)
    return x

# Finds posts containing the same class mentioned in the original post by ensuring
# the class number appears in the to-be recommended post's title and comment section
def find_posts(classes, url, num):
    global checkedPosts
    global checkedComment
    global count
    global commentCount
    global output
    output = ""
    print("Searching for related material")
    for archive in reddit.subreddit('cornell').new(limit=None):
        for classNums in classes:
            if classNums in archive.title + " " + archive.selftext:
                for comment in archive.comments:
                    if classNums in comment.body and archive.url != url and archive.url not in output and num < 5:
                        output = output + "[" + archive.title + "](" + archive.url + ")" + "\n\n"
                        num = num + 1
                        break
    return output

# Function to check if the comments of a post contain a comment by this bot
def hasCommented(post):
    for comment in post.comments:
        if comment.author == thisUser:
            return True
    return False

# Function to check if the bot has replied to a comment
def hasReplied(comment):
    for reply in comment.replies:
        if reply.author == thisUser:
            return True
    return False


# Reply to all comments invoking classbot
def reply():
    global checkedPosts
    global checkedComment
    global count
    global commentCount
    global output
    for submission in reddit.subreddit('cornell').new(limit=500):
        for comment in submission.comments:
            if "!classBot" in comment.body and (not hasReplied(comment)):
                keyphrase = remove_nums(remove_duplicates(re.findall(r'\d{4}', comment.body)))
                if len(keyphrase):
                    output = find_posts(keyphrase, submission.url, count)
                    count = 0
                    if len(output) != 0:
                        comment.reply("I noticed you asked about a specific class! Here are some possibly useful links: \n\n" + output)
                        commentCount = commentCount + 1
                        print("This is the " + str(commentCount) + "th comment!")
                    output = ""

# Comment on most recent posts containing a 4-digit number
def comment():
    global checkedPosts
    global checkedComment
    global count
    global commentCount
    global output
    for submission in reddit.subreddit('cornell').new(limit=25):
        if not hasCommented(submission):
            keyphrase = remove_nums(remove_duplicates(re.findall(r'\d{4}',
                                    submission.title + " " + submission.selftext)))
            if len(keyphrase) != 0 and submission.url not in checkedPosts:
                checkedPosts = [submission.url] + checkedPosts
                if (len(checkedPosts) > 30):
                    del checkedPosts[-1]
                output = find_posts(keyphrase, submission.url, count)
                count = 0
            if len(output) != 0:
                submission.reply(
                    "I noticed you asked about a specific class! Here are some possibly useful links: \n\n" + output)
                commentCount = commentCount + 1
                print("This is the " + str(commentCount) + "th comment!")
            output = ""

# Remove comments from the past num_to_check with a score below threshold.
# Set num_to_check to None to check all comments
def remove_bad_comments(threshold=0, num_to_check=15):
    user = reddit.redditor(thisUser)
    for comment in user.comments.new(limit=num_to_check):
        if comment.score < threshold:
            comment.delete()

# Loop to constantly check the most recent 25 posts to see if it's neccesary for the bot to comment
while True:
    comment()
    reply()
    remove_bad_comments()
    print("Sleeping now")
    time.sleep(300)
