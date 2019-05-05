import os
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from myuser import MyUser
from usertweets import UserTweets
from profile import Profile
from edit import Edit
from edittweet import EditTweet


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        if user == None:
            template_values = {
                'login_url': users.create_login_url(self.request.url)
            }

            template = JINJA_ENVIRONMENT.get_template('loginpage.html')
            self.response.write(template.render(template_values))
            return
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser == None:
            myuser = MyUser(id=user.user_id())
            myuser.put()

            template_values = {
                'logout_url': users.create_logout_url(self.request.url)
            }

            template = JINJA_ENVIRONMENT.get_template('signup.html')
            self.response.write(template.render(template_values))
        else:
            self.response.headers['Content-Type'] = 'text/html'
            user = users.get_current_user()
            name = self.request.get('name')
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            storetweets = UserTweets().query().fetch()
            template_values = {
                'logout_url': users.create_logout_url(self.request.url),
                'usertweets': myuser.usertweets,
                'user': 'user',
                'myuser': 'myuser'
            }

            template = JINJA_ENVIRONMENT.get_template('twitterhome.html')
            self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action == 'SignUp':
            name = self.request.get('name')
            bio = self.request.get('bio')
            dateofbirth = self.request.get('dateofbirth')
            user = users.get_current_user

            stweets = UserTweets.query().fetch()

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            myuser = MyUser(id=user.user_id(), name=name, bio=bio, dateofbirth=dateofbirth, followers=[], following=[])
            myuser.put()
            usertweets_key = ndb.Key('UserTweets', name)
            gettweets = usertweets_key.get()
            self.redirect('/')
        elif self.request.get('button') == 'Search':
            temp = []
            count = []

            result = self.request.get('Search')

            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if result == '':
                self.redirect('/')
            else:
                name_search = MyUser.query(MyUser.name == result).fetch()
                search_tweet = UserTweets.query().fetch()

                if len(name_search) > 0 or len(search_tweet) > 0:

                    for tweet in search_tweet:
                        for i in tweet.tweets:
                            temp.append(i)
                    for i in range(len(temp)):
                        temp2 = temp[i].split(" ")
                        for j in temp2:
                            if (j in result):
                                response.append(temp[i])
                                break;

                    template_values = {
                        'search_tweet': response,
                        'name_search': name_search
                    }
                    template = JINJA_ENVIRONMENT.get_template('twitterhome.html')
                    self.response.write(template.render(template_values))

        elif self.request.get('button') == 'Tweet':
            tweets = self.request.get('tweets')

            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            new_tweet = UserTweets(name=myuser.name, tweets=tweets)
            myuser.usertweets.append(new_tweet)
            myuser.put()
            new_tweet.put()
            self.redirect('/')
        elif self.request.get('button') == 'Delete tweet':
            index = int(self.request.get('index'))
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            del myuser.usertweets[index]
            myuser.put()
            self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/profile', Profile),
    ('/edit', Edit),
    ('/edittweet', EditTweet)
], debug=True)
