from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import iati2lod_navigation

def get_model_names():
    '''Returns the names of all models and corresponding pages.
    
    Returns
    @activities: A list of entity, page tuples.
    @organisations: A list of entity, page tuples.
    @codelists: A list of entity, page tuples.'''
    
    activities = [('Activity basics', ['iati-identifier',
                                       'activity-website',
                                       'title',
                                       'activity-status',
                                       'collaboration-type',
                                       'finance-type',
                                       'flow-type',
                                       'aid-type',
                                       'tied-status']),
                   
                   ('Activity organisations', ['reporting-org',
                                               'participating-org']),
                    
                   ('Activity meta1', ['other-identifier',
                                       'description']),
                  
                   ('Activity meta2', ['contact-info',
                                       'document-link']),
                  
                   ('Activity dates', ['start-actual',
                                       'end-actual',
                                       'start-planned',
                                       'end-planned']),
                  
                   ('Activity recipients', ['recipient-country',
                                            'recipient-region']),
                  
                   ('Activity location', ['location']),
                   
                   ('Activity sector and policy', ['sector',
                                                   'policy-marker']),
                  
                   ('Activity budget', ['activity-budget']),
                   
                   ('Activity disbursement', ['planned-disbursement']),
                   
                   ('Activity transaction', ['activity-transaction']),
                   
                   ('Activity related and conditions', ['related-activity',
                                                        'conditions']),
                  
                   ('Activity result', ['result'])]
    
    organisations = [('Organisation basics', ['iati-identifier',
                                              'identifier',
                                              'name']),
                     
                     ('Organisation reporting organisation', ['reporting-org']),
                     
                     ('Organisation total budget', ['total-budget']),
                     
                     ('Organisation recipient organisation budget', ['recipient-org-budget']),
                     
                     ('Organisation recipient country budget', ['recipient-country-budget']),
                     
                     ('Organisation document link', ['document-link'])]
    
    codelists = [('Codelists', ['codelist',
                                'codelist-code',
                                'codelist-category'])]
    
    provenance = [('Provenance', ['last-updated',
                                  'version',
                                  'source-document-maintainer',
                                  'source-document-author']),
                  
                  ('Provenance source document1', ['source-document']),
                  
                  ('Provenance source document2', ['source-document',
                                                   'source-document-extras']),
                  
                  ('Provenance source document resources', ['source-document-resources'])]
    
    return activities, organisations, codelists, provenance
    

# MainPage is a subclass of webapp.RequestHandler and overwrites the get method
class Model(webapp.RequestHandler):
    def get(self):

        nav, subnav = iati2lod_navigation.navigation()
        
        nav = nav.replace('<a href="/model">', '<a id="select" href="/model">')
        subnav = subnav['Model'].replace('<a href="/model/visualizations">', '<a id="select" href="/model/visualizations">')

        activities, organisations, codelists, provenance = get_model_names()
        
        model = self.request.get_all("viz")
        
        if model == []:
            values = {"activities": activities,
                      "organisations": organisations,
                      "codelists": codelists,
                      "provenance": provenance,
                      "nav": nav,
                      "subnav": subnav}
            
            self.response.out.write(template.render('model-visualizations.html', values))
            
        else:
            values = {"modelname": model[0],
                      "model": model[0].replace(" ","-"),
                      "nav": nav,
                      "subnav": subnav}
            
            self.response.out.write(template.render('model-viz.html', values))

# Register the URL with the responsible classes
application = webapp.WSGIApplication([('/model/visualizations', Model)], debug=True)

# Register the wsgi application to run
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main() 