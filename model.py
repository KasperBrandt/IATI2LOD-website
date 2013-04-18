from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

def get_model_names():
    '''Returns the names of all models and corresponding pages.
    
    Returns
    @activities: A list of entity, page tuples.
    @organisations: A list of entity, page tuples.
    @codelists: A list of entity, page tuples.'''
    
    activities = [('overview', 'overview'),
                  ('iati-identifier', 'activity-basics'),
                  ('activity-website', 'activity-basics'),
                  ('title', 'activity-basics'),
                  ('activity-status', 'activity-basics'),
                  ('collaboration-type', 'activity-basics'),
                  ('finance-type', 'activity-basics'),
                  ('flow-type', 'activity-basics'),
                  ('aid-type', 'activity-basics'),
                  ('tied-status', 'activity-basics'),
                  ('reporting-org', 'activity-organisations'),
                  ('participating-org', 'activity-organisations'),
                  ('other-identifier', 'activity-meta1'),
                  ('description', 'activity-meta1'),
                  ('contact-info', 'activity-meta2'),
                  ('document-link', 'activity-meta2'),
                  ('start-actual', 'activity-dates'),
                  ('end-actual', 'activity-dates'),
                  ('start-planned', 'activity-dates'),
                  ('end-planned', 'activity-dates'),
                  ('recipient-country', 'activity-recipients'),
                  ('recipient-region', 'activity-recipients'),
                  ('location', 'activity-location'),
                  ('sector', 'activity-sector-and-policy'),
                  ('policy-marker', 'activity-sector-and-policy'),
                  ('budget', 'activity-budget'),
                  ('planned-disbursement', 'activity-disbursement'),
                  ('transaction', 'activity-transaction'),
                  ('related-activity', 'activity-related-and-conditions'),
                  ('conditions', 'activity-related-and-conditions'),
                  ('result', 'activity-result')]
    
    return activities
    

# MainPage is a subclass of webapp.RequestHandler and overwrites the get method
class Model(webapp.RequestHandler):
    def get(self):

        activities = get_model_names()
        
        model = self.request.get_all("model")
        
        if model == []:
            model = ['overview']
        
        values = {"activities":activities, "model":model}
        
        self.response.out.write(template.render('model.html', values))

# Register the URL with the responsible classes
application = webapp.WSGIApplication([('/model', Model)], debug=True)

# Register the wsgi application to run
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main() 