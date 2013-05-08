from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import iati2lod_navigation


# MainPage is a subclass of webapp.RequestHandler and overwrites the get method
class Main(webapp.RequestHandler):
    def get(self):
        
        nav, subnav = iati2lod_navigation.navigation()
        
        nav = nav.replace('<a href="/">', '<a id="select" href="/">')
        subnav = subnav['Home'].replace('<a href="/">', '<a id="select" href="/">')
        
        values = {"nav": nav,
                  "subnav": subnav}
        
        self.response.out.write(template.render('main.html', values))



# Register the URL with the responsible classes
application = webapp.WSGIApplication([('/', Main)], debug=True)

# Register the wsgi application to run
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main() 