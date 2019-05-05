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


class Profile(webapp2.RequestHandler):
    def get(self):
        self.request.headers['Content-Type'] = 'text/html'
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

        name = self.request.get('name')

        userbio = MyUser.query(MyUser.name == name).fetch()
        list_tweets = MyUser.UserTweets.query(UserTweets.name == name).fetch()

        twitter_key = ndb.Key('UserTweets', myuser.name)
        twitter = twitter_key.get()
        usertweets_new = myuser.usertweets

        followBool = True

        if userbio[0]:
            logging.info(myuser.following)
            if userbio[0].name in myuser.following:
                followBool = False

        template_values = {
            'logout_url': users.create_logout_url(self.request.url),
            'userbio': userbio,
            'tweets': list_tweets,
            'usertweets': myuser.usertweets,
            'followBool': followBool,
            'currentuser_name': myuser.name
        }

        template = JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')
        if action == 'Follow':
            following = self.request.get('following')
            name = self.request.get('name')
            bio = self.request.get('bio')
            tweetname = self.request.get('tweetname')

            user = users.get_current_user()

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            usertweets_new = myuser.usertweets
            myuser.name
            if following not in myuser.following:
                if len(myuser.following) == 0:
                    myuser.following = [following]
                    myuser.put()
                    self.redirect('/')
                else:
                    myuser.following.append(following)
                    myuser.put()
                    self.redirect('/')

            elif self.request.get('button') == 'Unfollow':
                index = int(self.request.get('index'))

                user = users.get_current_user()
                myuser_key = ndb.Key('MyUser', user.user_id())
                myuser = myuser_key.get()

                del myuser.following[index]
                myuser.put()

                self.redirect('/')
