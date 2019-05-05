import os
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import logging

from myuser import MyUser
from usertweets import UserTweets


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class EditTweet(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        if user == None:
            template_values = {
                'login_url': users.create_login_url(self.request.url)
            }

            template = JINJA_ENVIRONMENT.get_template('twitterhome.html')
            self.response.write(template.render(template_values))
            return
        usertweet = self.request.get('usertweet')
        usertweet_key = ndb.Key('UserTweet', usertweet)
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        i = usertweet_key.get()
        template_values = {
            'i': i,
            'usertweets': myuser.usertweets
        }

        template = JINJA_ENVIRONMENT.get_template('edittweet.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if self.request.get('button') == 'Update':
            usertweet = self.request.get('usertweet')
            usertweet_key = ndb.Key('MyUser', user.user_id())
            i = usertweet_key.get()
            i.usertweets = self.request.get('usertweet')
            i.put()
            self.redirect('/')
