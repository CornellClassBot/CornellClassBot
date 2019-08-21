# Cornell Class Bot

A bot that gives you extra info about classes you're interested in! This is an open source project by the Cornell community for the Cornell community. Note: Cornell Class Bot could easily be adapted for other colleges.

## About
This bot aims to help with the large amount of users asking similar questions about common classes.

It uses RegEx to determine if a user of `r/Cornell` is asking about a class. Every five minutes, the bot checks the most recent 25 posts to determine if a person is asking about a class. If a post has been previously cached, the bot will skip over it.

If the bot determines that a post is about a class, then it parses through the most recent 1000 posts to the subreddit to determine if they are relevant to what the original post asked. The results are appended to a string and automatically commented by the bot account on Reddit! 

![A screenshot of the bot replying](https://i.imgur.com/PiZT7Vi.png)
###### The bot in action

## Can I help?
Absolutely! This is an open source project and contributions are welcome. All pull requests will be approved by the moderators of `r/Cornell` before being merged.

## Known Issues
The bot is a little trigger happy with responding to posts. This manifests in two main ways:
1. The bot responds with information about irrelevant classes
2. The bot's response is unwanted

Steps have been taken to help with the latter like removing comments automatically when they've been downvoted too much, but the former is trickier. Efforts at improving Cornell Class Bot should focus on the mitigating the first issue. Posts where people mention several classes prove trickiest, perhaps a more sophisticated algorithm like focusing on the class mentioned first/the most/after keywords would be more effective.


## To-do
- [ ] Clean up the code, not obvious at a glance what many variables do
- [ ] Prevent bot from responding about classes with too little useful information
- [ ] Improve algorithm to better handle posts that mention multiple classes
- [ ] Look to expand features of bot, are there other problems it could help with?
