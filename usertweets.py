from google.appengine.ext import ndb


class UserTweets(ndb.Model):
    name = ndb.StringProperty()
    tweets = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
