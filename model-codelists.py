## By Kasper Brandt
## Last updated on 08-05-2013

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import iati2lod_navigation

def get_contents():
    contents = [('<a name="codelist"></a>iati:codelist/{codelist}', 
                 '''A codelist scheme. From this codelist all related codes can be found. The codelists are linked to a SKOS 
                 scheme in order to make a small thesaurus of each codelist.''',
                 [('rdf:type', 'iati:codelist <font color="red">rdfs:subClassOf skos:conceptScheme</font>'),
                  ('rdfs:label', '{codelist}'),
                  ('iati:codelist-member', '<a href=#codelist-code>iati:codelist/{codelist}/{code}</a>')]),
                
                ('<a name="codelist-code"></a>iati:codelist/{codelist}/{code}',
                 '''A code in a codelist, used to identify a standardized concept in the IATI schemes. The category of the code
                 is not included in the URI, since this allows for linking activity elements to codelist codes as none of the 
                 codelist codes in the activities contain a category. However, the category of the code can be looked up using 
                 the 'iati:in-category' relation.''',
                 [('rdf:type', 'iati:codelist-code <font color="red">rdfs:subClassOf skos:Concept</font>'),
                  ('rdfs:label', '{name}'),
                  ('rdfs:comment', '{description}'),
                  ('iati:member-of-codelist <font color="red">rdfs:subPropertyOf skos:inScheme</font>', '<a href=#codelist>iati:codelist/{codelist}</a>'),
                  ('iati:in-category <font color="red">rdfs:subPropertyOf skos:broader</font>', '<a href=#codelist-category>iati:codelist/{codelist}/category/{category-code}</a>'),
                  ('iati:code', '{code}'),
                  ('iati:abbreviation', '{abbreviation}')]),
                
                ('<a name="codelist-category"></a>iati:codelist/{codelist}/category/{category-code}',
                 '''A category of a codelist-code, used to identify a standardized category of concepts in the IATI schemes. 
                 All codes belonging to this category can be looked up using the 'iati:has-member' relation.''',
                 [('rdf:type', 'iati:codelist-category <font color="red">rdfs:subClassOf skos:Concept</font>'),
                  ('rdfs:label', '{name}'),
                  ('rdfs:comment', '{description}'),
                  ('iati:has-member <font color="red">rdfs:subPropertyOf skos:narrower</font>', '<a href=#codelist-code>iati:codelist/{codelist}/{code}</a>'),
                  ('iati:code', '{code}')])               
                
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
class Codelists(webapp.RequestHandler):
    def get(self):
        
        nav, subnav = iati2lod_navigation.navigation()
        
        nav = nav.replace('<a href="/model">', '<a id="select" href="/model">')
        subnav = subnav['Model'].replace('<a href="/model/codelists">', '<a id="select" href="/model/codelists">')
        
        contents = get_contents()
        
        index = create_index(contents)
        
        values = {"type":'Codelists',
                  "contents": contents,
                  "index": index,
                  "nav": nav,
                  "subnav": subnav}
        
        self.response.out.write(template.render('model-description.html', values))

# Register the URL with the responsible classes
application = webapp.WSGIApplication([('/model/codelists', Codelists)], debug=True)

# Register the wsgi application to run
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main() 