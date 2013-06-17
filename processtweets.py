
import sys
import json
import re


"""
Process All Tweets and generate summaries
"""

# global counter variabls
users_dict = dict()
tweet_ids = dict()
tweet_counts = dict()
retweet_counts = dict()
follower_counts = dict()
favorites_counts = dict()
friends_counts = dict()
tweet_words = dict()
tweet_hashtags = dict()
tweet_mentions = dict()
tweet_ids_text =dict()
tweet_ids_user = dict()
user_name_id = dict()
tweet_retweet = dict()

def genrate_top100_list(dic):
    sorted_list = list()
    for key in sorted(dic, key=dic.get, reverse=True):
        sorted_list.append((key.encode('utf-8'), dic[key]))
    top_100 = list()
    for i in range(100):        
        top_100.append(sorted_list[i])
    return top_100

def genrate_top100_tweets(dic):
    sorted_list = list()
    for key in sorted(dic, key=dic.get, reverse=True):
        sorted_list.append((tweet_ids_user[key].encode('utf-8'), dic[key], tweet_ids_text[key].encode('utf-8'))) # I am returning Tweeter's name
    top_100 = list()
    for i in range(100):        
        top_100.append(sorted_list[i])
    return top_100


def print_summary(search_phrases):

    global users_dict
    global tweet_ids
    global tweet_counts
    global retweet_counts
    global follower_counts
    global favorites_counts
    global friends_counts
    global tweet_words
    global tweet_hashtags
    global tweet_mentions
    global tweet_ids_text
    global tweet_ids_user
    global user_name_id
    global tweet_retweet

    print '%50s' % 'Results Summary\n'
 
    print 'Search Terms used:'    
    terms = list()
    for term in search_phrases:
        terms.append(term)
    print terms

    print '\n\n'
    print '%60s' % "Totals"
    print  '%50s' % 'Users', '\t', 'Tweets', '\t', 'Retweets'
    user_count = 0
    tweet_count = 0
    retweet_count = 0
    for name in users_dict.keys():
        user_count+=1
        tweet_count += tweet_counts[name]
        retweet_count += retweet_counts[name]
    print '%50s' % user_count, '%10d' % tweet_count, '%10d' % retweet_count
    


    print '\n\n'
    print 'Top 100 Tweeted Words: (Word, Count)'
    print genrate_top100_list(tweet_words)


    print '\n\n'
    print 'Top 100 Hashtags: (Hahtag, Count)'
    print genrate_top100_list(tweet_hashtags)


    print '\n\n'
    print 'Top 100 User Mentions: (User Mentions, Count)'
    print genrate_top100_list(tweet_mentions)

    print '\n\n'
    print 'Top 100 Tweeting Users: (Tweeter Name, Tweet Count)' 
    print genrate_top100_list(tweet_counts)
    
    


    print '\n\n'
    print 'Top 100 Retweeted Users: (Tweeter Name, Retweet Count)'
    print genrate_top100_list(retweet_counts)

    print '\n\n'
    print 'Top 100 Retweeted Tweets: (Tweeter Name, Retweet Count, Tweet Text)'
    print genrate_top100_tweets(tweet_retweet)
    

    print '\n\n'
    print '%25s' % 'User Name', '%31s' % 'Location',  '   ', 'Tweets', 'Retweets', 'Followers', 'Favorites', 'Friends'
    for name in users_dict.keys():
        tc  = []
        rtc = []
        ftc = []
        fac = []
        frc = []
        loc = users_dict[name]
        if name in tweet_counts:
            tc = tweet_counts[name]
        if name in retweet_counts:
            rtc = retweet_counts[name]
        if name in follower_counts:
            ftc = follower_counts[name]
        if name in favorites_counts:
            fac = favorites_counts[name]
        if name in friends_counts:
            frc = friends_counts[name]
        print '%25s' % name.encode('utf-8'), '\t', '%25s' % loc.encode('utf-8'), '\t', tc, '\t', rtc
    return

def is_url(s): # if it is a URL(s) returns URL array otherwise []
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', s)


def count_words(text):
    global tweet_words
    stop_words = ['able','about','across','after','all','almost','also','am','among',
                 'an','and','any','are','as','at','be','because','been','but','by','can',
                 'cannot','could','dear','did','do','does','either','else','ever','every',
                 'for','from','get','got','had','has','have','he','her','hers','him','his',
                 'how','however','i','if','in','into','is','it','its','just','least','let',
                 'like','likely','may','me','might','most','must','my','neither','no','nor',
                 'not','of','off','often','on','only','or','other','our','own','rather','said',
                 'say','says','she','should','since','so','some','than','that','the','their',
                 'them','then','there','these','they','this','tis','to','too','twas','us',
                 'wants','was','we','were','what','when','where','which','while','who',
                 'whom','why','will','with','would','yet','you','your', '-', '&amp;',  ':',
                  'The', 'via',  'de', 'up', "i'm", 'en', '!',  '|' ]

    words = text.split()
    for word in words:
        word = word.lower()
        if len(word) > 1:
            if word not in stop_words: # not a stop word
                if is_url(word) == []:
                    if word in tweet_words:
                        tweet_words[word] += 1  
                    else:
                        tweet_words[word] = 1
    return


            
def count_hashtags(tag):
    global tweet_hashtags
    if tag not in tweet_hashtags:
        tweet_hashtags[tag] = 1 # found hashtag first time
    else:
        tweet_hashtags[tag] +=1
    return
    
def count_user_mentions(name):
    global tweet_mentions
    if name not in tweet_mentions:
        tweet_mentions[name] = 1 # found name mention first time
    else:
        tweet_mentions[name] +=1
    return       
    

def update_user(name, location):
    global users_dict
    if name not in users_dict:
        users_dict[name] = location
    return

def update_tweet_count(name, id):
    global tweet_ids
    global tweet_counts
    if id not in tweet_ids: # first time we are seeing this tweet        
        if name in tweet_counts:            
            tweet_counts[name] +=1
        else:
            tweet_counts[name] = 1 # first tweet for the user
    else:
        tweet_ids[id] = name
    return
        
def update_retweet_count(name, count):
    global retweet_counts
    if name in retweet_counts:
        retweet_counts[name] +=count
    else:
        retweet_counts[name] = count # first re_tweet for the user
    return

def update_follower_count(name, count):
    global follower_counts
    if name in follower_counts:
        follower_counts[name] +=count
    else:
        follower_counts[name] = count # first follower for the tweet for the user
    return

def update_favorites_count(name, count):
    global favorites_counts
    if name in favorites_counts:
        favorites_counts[name] +=count
    else:
        favorites_counts[name] = count # first favorite for the tweet for the user
    return

def update_friends_count(name, count):
    global friends_counts
    if name in friends_counts:
        friends_counts[name] +=count
    else:
        friends_counts[name] = count # first favorite for the tweet for the user
    return

def update_tweet_info(tweet):
    global tweet_ids_text
    global tweet_ids_user
    global user_name_id
    global tweet_retweet
    
    if 'id' in tweet:
        id = tweet['id']
        if id not in tweet_ids_text: # we have not seen this tweet before
            if 'text' in tweet:
                tweet_ids_text[id] = tweet['text']
                count_words(tweet['text']) # update the word count
                if 'user' in tweet:                    
                    user = tweet['user']
                    if 'name' in user:
                        name = user['name']
                        tweet_ids_user[id] = name
                        if 'id_str' in name:
                            user_name_id[name] = name['id_str']
                        location = ''
                        if 'location' in user:                            
                            location = user['location']
                        update_user(name, location)
                        if 'id' in tweet:
                            update_tweet_count(name, tweet['id'])
                        if 'retweet_count' in tweet:
                            update_retweet_count(name, tweet['retweet_count'])                     
                        if 'followers_count' in tweet:
                            update_follower_count(name, tweet['followers_count'])
                        if 'favourites_count' in tweet:
                            update_favorites_count(name, tweet['favourites_count'])
                        if 'friends_count' in tweet:
                            update_friends_count(name, tweet['friends_count'])
                else:
                    tweet_ids_user[id] = '' # Need to see why we had this situation
        if 'retweet_count' in tweet:
            tweet_retweet[id] = tweet['retweet_count']  
    return                
    
            

# =============================
if __name__ == '__main__':

  search_phrases = list()
 
 
  f_terms = open('search_terms.txt', 'rU')
  for line in f_terms: #each line will have a serach term
    search_file= line.rstrip('\n')
#   print 'search term from serach file: ', search_file
    par_dir = 'DSdata\\' # Storing serach results
    file_name = par_dir+search_file+'.json' 
    tweets_file = open(file_name, 'rU')
    
    serach_term = tweets_file.readline()
    serach_term = serach_term.rstrip('\n')    
    search_phrases.append(serach_term)
#   print "search_term from tweet file: ", search_term
    for line in tweets_file:
        tweet = json.loads(line)
        update_tweet_info(tweet) # update tweet and user specific
        if 'entities' in tweet:  # update Hash Tags and User Mentions
            entities = tweet['entities']
            if 'hashtags' in entities:  
                hashtags = entities['hashtags']
                for hashtag in hashtags:
                    count_hashtags(hashtag['text'])
            if 'user_mentions' in entities:  
                user_mentions = entities['user_mentions']
                for user_mention in user_mentions:
                    count_user_mentions(user_mention['name'])
    tweets_file.close() # we are done with current tweet file

  print_summary(search_phrases)

  f_terms.close() 
    
