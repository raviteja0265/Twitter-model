from google.appengine.ext import ndb
from usertweets import UserTweets


class MyUser(ndb.Model):
    name = ndb.StringProperty()
    bio = ndb.StringProperty()
    dateofbirth = ndb.DateProperty()
    followers = ndb.StringProperty(repeated=True)
    following = ndb.StringProperty(repeated=True)
    usertweets = ndb.StructuredProperty(UserTweets, repeated=True)
