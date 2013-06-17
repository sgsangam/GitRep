import oauth2 as oauth
import urllib2 as urllib
import json

"""
gettweets.py:
Author: S. G. Sangameswara
Contact: sgsangam@gmail.com
Created for: Coursera Data Science Coursolve Project
Uasge: python27\python 'gettweets.py' 'serach_terms.txt',
       where serach_terms is any file containg serach keywords, one perline
       Make sure to create 'DaData' folder whre results files will be created.
"""

# See Assignment 1 instructions or README for how to get these credentials
access_token_key = "28579396-UFCJTFjfG0hzAPTao0YnGXB5Mymrhi0DxMlaPR5W4"
access_token_secret = "RSsCkI1a2HyidwOO1ZV3EtsHpw4xY8lXeNAGxKbd6E"

consumer_key = "EqCbo91Tc5oa9PwbNAwBWQ"
consumer_secret = "YbvnXbPTvUTFHVc8Hv4IVgjQtJ857iLDmB31Bkyio"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchtweets(): 

#  search_terms = ['edxOnline', 'edx', 'agarwaledu', 'coursera', 'udacity', 'MOCC', 'learning online', 'elearning', 'khan academy']
#  search_terms = ['edxOnline',  'coursera', 'udacity',  'khan academy']
  api_url = "https://api.twitter.com/1.1/search/tweets.json?q="
  f_terms = open('search_terms.txt', 'r') # This file will have search terms, one per line
  
#  for search_term in search_terms:
  for line in f_terms: #each line will have a serach term
    search_term = line.rstrip('\n')
    print 'search term: ', search_term
    par_dir = 'DSdata\\' # Storing serach results
    f_res = open(par_dir+search_term+'.json', 'w') # Open file 'serach_trem' as name
    f_res.write(search_term+'\n') # write the serach term into results file
    process_next_url = False
    since_id = -1
    max_id = -1
    req_since_id_str = ''
    req_max_id_str = ''
    loop_count = 0
    while process_next_url == False:      
      req_url = api_url+search_term+'&count=100'
      if since_id != -1:
        req_since_id_str = '&since_id='+str(since_id)
      if max_id != -1:
        req_max_id_str = '&max_id='+str(max_id)
      req_url = api_url+search_term+'&count=100'+req_max_id_str # why it is not taking since_id
      print "Processing Serach Term: ", search_term
      print req_url
      parameters = []

      response = twitterreq(req_url, "GET", parameters) # Make the request
      jresp = json.load(response) # Load the JSON response
      if "errors" in jresp:
        print "while processing serach term:", search_term
        print jresp["errors"]
        f_res.close() #close the current results file and exit
        exit()

      if "statuses" in jresp: # Get serach results
        tweets = jresp["statuses"]
        tweet_count = 0
        
        for tweet in tweets: # got another tweet          
          f_res.write(json.dumps(tweet))
          f_res.write('\n')
          if 'id' in tweet:
            if tweet_count == 99:
              max_id = tweet['id']
              max_id_str = str(max_id-1) 
          tweet_count +=1 # end of processing a tweet info
            
        loop_count +=1 #debug only 
        if tweet_count == 100 : # Little silly, AP does not care for 'count' parameter           
          if 'search_metadata' in jresp:
            meta_data = jresp['search_metadata']
            if 'max_id' in meta_data:
               since_id = meta_data['max_id']   # we are setting since id to max_id
        else:
          process_next_url = True
        print "Tweet_count,  Loop count, since_id, max_id, Process_next_URL: ", tweet_count, loop_count, since_id, max_id, process_next_url
        print "\n"
      else:
        print "Did not get statuses, Fishy"
        process_next_url = True
        
      if process_next_url == True:
        f_res.close() # close the current results file
        print "\n\n"
    # we are still in while loop  
  f_terms.close() # we are done
  print "We are done for now\n"
 

if __name__ == '__main__':
  fetchtweets()

