import os
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from myuser import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Edit(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        template_values = {
            'myuser': myuser
        }

        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action == 'Update':
            user = users.get_curent_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            myuser.name = self.request.get('username')
            myuser.bio = self.request.get('userbio')
            myuser.put()

            self.redirect('/')
        elif self.request.get('button') == 'Cancel':
            self.redirect('/')
