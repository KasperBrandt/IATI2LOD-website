## By Kasper Brandt
## Last updated on 08-05-2013

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import iati2lod_navigation

# MainPage is a subclass of webapp.RequestHandler and overwrites the get method
class Examples(webapp.RequestHandler):
    def get(self):
        
        nav, subnav = iati2lod_navigation.navigation()
        
        nav = nav.replace('<a href="/model">', '<a id="select" href="/model">')
        subnav = subnav['Model'].replace('<a href="/model/examples">', '<a id="select" href="/model/examples">')
        
        values = {"type":'Examples',
                  "nav": nav,
                  "subnav": subnav}
        
        self.response.out.write(template.render('model-examples.html', values))

# Register the URL with the responsible classes
application = webapp.WSGIApplication([('/model/examples', Examples)], debug=True)

# Register the wsgi application to run
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main() 