## By Kasper Brandt
## Last updated on 08-05-2013

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import iati2lod_navigation

def get_contents():
    contents = [('<a name="organisation"></a>iati:organisation/{organisation-id}', 
                 '''The main URI referencing an organisation. The organisation ID is required, meaning that organisations 
                 without a IATI ID specified cannot be transformed into linked data URIs and will therefore be
                 ignored in the conversion process. Since some organisations have specified the 'iati-identifier' element as 
                 'identifier', this node is taken into account regarding the IATI ID as well. The organisation is linked to 
                 their corresponding codelist by means of an owl:sameAs relation.''',
                 [('rdf:type', 'iati:organisation <font color="red">rdfs:subClassOf org:Organisation</font>'),
                  ('owl:sameAs', 'iati:codelist/OrganisationIdentifier/{organisation-id}'),
                  ('rdfs:label', '{name}'),
                  ('iati:iati-identifier <font color="red">rdfs:subPropertyOf dct:identifier</font>', '{iati-identifier}'),
                  ('iati:organisation-id <font color="red">rdfs:subPropertyOf dct:identifier</font>', '{identifier}'),
                  ('iati:organisation-reporting-org', '''<a href="#reporting-org">iati:organisation/{organisation-id}/reporting-org/{ref}</a><br>
                  or<br>
                  <a href="#reporting-org">iati:organisation/{organisation-id}/reporting-org{count}'''),
                  ('iati:organisation-total-budget', '<a href="#total-budget">iati:organisation/{organisation-id}/total-budget{count}</a>'),
                  ('iati:organisation-recipient-org-budget', '<a href="#recipient-org-budget">iati:organisation/{organisation-id}/recipient-org-budget{count}</a>'),
                  ('iati:organisation-recipient-country-budget', '<a href="#recipient-country-budget">iati:organisation/{organisation-id}/recipient-country-budget{count}</a>'),
                  ('iati:organisation-document-link', '<a href="#document-link">iati:organisation/{organisation-id}/document-link{count}</a>')]),
                
                ('''<a name="reporting-org"></a>iati:organisation/{organisation-id}/reporting-org/{ref}<br>
                or<br>
                iati:organisation/{organisation-id}/reporting-org{count}''',
                 '''The URI for indicating which organisation is reporting. When no official IATI reference for the reporting
                 organisation is specified, a counter will be added to the URI instead of the reference.''',
                 [('rdf:type', 'iati:organisation <font color="red">rdfs:subClassOf org:Organisation</font>'),
                  ('rdfs:label', '{name}'),
                  ('iati:organisation-code', 'iati:codelist/OrganisationIdentifier/{ref}'),
                  ('iati:organisation-type', 'iati:codelist/OrganisationType/{type}')]),
                
                ('<a name="total-budget"></a>iati:organisation/{organisation-id}/total-budget{count}',
                 '''Used for specifying the total budget of the organisation. It is possible to specify a budget for multiple periods, 
                 therefore a counter has been added to the URI in order to uniquely identify the budget.''',
                 [('rdf:type', 'iati:budget'),
                  ('iati:start-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{start-date}'),
                  ('iati:start-date-text', '{start-date-text}'),
                  ('iati:end-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{end-date}'),
                  ('iati:end-date-text', '{end-date-text}'),
                  ('iati:value', '{value}'),
                  ('iati:value-currency', 'iati:codelist/Currency/{currency}'),
                  ('iati:value-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{value-date}')]),     
                
                ('<a name="recipient-org-budget"></a>iati:organisation/{organisation-id}/recipient-org-budget{count}',
                 '''Used for specifying the budget for a receiving organisation. It is possible to specify a budget for multiple periods, 
                 therefore a counter has been added to the URI in order to uniquely identify the budget.''',
                 [('rdf:type', 'iati:budget'),
                  ('iati:recipient-org', 'iati:codelist/OrganisationIdentifier/{ref}'),
                  ('iati:recipient-org-ref', '{ref}'),
                  ('iati:start-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{start-date}'),
                  ('iati:start-date-text', '{start-date-text}'),
                  ('iati:end-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{end-date}'),
                  ('iati:end-date-text', '{end-date-text}'),
                  ('iati:value', '{value}'),
                  ('iati:value-currency', 'iati:codelist/Currency/{currency}'),
                  ('iati:value-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{value-date}')]),   
                
                ('<a name="recipient-country-budget"></a>iati:organisation/{organisation-id}/recipient-country-budget{count}',
                 '''Used for specifying the budget for a receiving country. It is possible to specify a budget for multiple periods, 
                 therefore a counter has been added to the URI in order to uniquely identify the budget.''',
                 [('rdf:type', 'iati:budget'),
                  ('iati:recipient-country', 'iati:codelist/Country/{ref}'),
                  ('iati:recipient-country-ref', '{ref}'),
                  ('iati:start-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{start-date}'),
                  ('iati:start-date-text', '{start-date-text}'),
                  ('iati:end-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{end-date}'),
                  ('iati:end-date-text', '{end-date-text}'),
                  ('iati:value', '{value}'),
                  ('iati:value-currency', 'iati:codelist/Currency/{currency}'),
                  ('iati:value-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{value-date}')]),
                
                ('<a name="document-link"></a>iati:organisation/{organisation-id}/document-link{count}',
                  '''Used to indicate a link to a document. Since it is possible to have multiple links to documents, a counter 
                  is added to the URI.''',
                  [('rdf:type', 'iati:document-link'),
                   ('rdfs:label', '{title}'),
                   ('iati:url', '{url}'),
                   ('iati:format <font color="red">rdfs:subPropertyOf dct:hasFormat</font>', '{format}'),
                   ('iati:document-category', 'iati:codelist/DocumentCategory/{category}'),
                   ('iati:language <font color="red">rdfs:subPropertyOf dct:language</font>', '{language}'),
                   ('iati:language-text', '{language-text}')])
                
                ]
                
    return contents

def create_index(contents):
    '''Creates the index based on the contents.
    
    Parameters
    @contents: A nested list of contents.
    
    Returns
    @index: A list items.'''
    
    index = []
    
    for content in contents:
        index_item = content[0].replace('<a name="', '<a href="#').replace('</a>', '')
        
        item = index_item + '</a>'
        
        index.append(item)
        
    return index

# MainPage is a subclass of webapp.RequestHandler and overwrites the get method
class Organisations(webapp.RequestHandler):
    def get(self):
        
        nav, subnav = iati2lod_navigation.navigation()
        
        nav = nav.replace('<a href="/model">', '<a id="select" href="/model">')
        subnav = subnav['Model'].replace('<a href="/model/organisations">', '<a id="select" href="/model/organisations">')
        
        contents = get_contents()
        
        index = create_index(contents)
        
        values = {"type":'Organisations',
                  "contents": contents,
                  "index": index,
                  "nav": nav,
                  "subnav": subnav}
        
        self.response.out.write(template.render('model-description.html', values))

# Register the URL with the responsible classes
application = webapp.WSGIApplication([('/model/organisations', Organisations)], debug=True)

# Register the wsgi application to run
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main() 