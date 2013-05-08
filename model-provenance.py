## By Kasper Brandt
## Last updated on 08-05-2013

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import iati2lod_navigation

def get_contents():
    contents = [('<a name="graph"></a>iati:graph/{entity}/{entity-id}', 
                 '''A named graph for storing all provenance related to the source of the data. The entity is related to the 
                 source of the data as well, being either 'activity', 'organisation' or 'codelist' in case of IATI data. In case 
                 of external data, such as Geonames, the entity corresponds to the name of this source.''',
                 [('rdf:type', 'iati:graph'),
                  ('rdfs:label', '{name}'),
                  ('iati:last-updated <font color="red">rdfs:subPropertyOf dct:modified</font>', '{last-updated}'),
                  ('iati:version <font color="red">rdfs:subPropertyOf dct:hasVersion</font>', '{version}'),
                  ('iati:source-document-maintainer <font color="red">rdfs:subPropertyOf dct:contributor</font>', '<a href="#maintainer">iati:graph/{entity}/{entity-id}/maintainer</a>'),
                  ('iati:source-document-author <font color="red">rdfs:subPropertyOf dct:creator</font>', '<a href="#author">iati:graph/{entity}/{entity-id}/author</a>'),
                  ('iati:source-document-id <font color="red">rdfs:subPropertyOf dct:identifier</font>', '{func-id}'),
                  ('iati:source-document-metadata-created', '{metadata-created}'),
                  ('iati:source-document-metadata-modified', '{metadata-modified}'),
                  ('iati:source-document-license <font color="red">rdfs:subPropertyOf cc:license</font>', '{license}'),
                  ('iati:source-document-download-url <font color="red">rdfs:subPropertyOf dct:source</font>', '{download-url}'),
                  ('iati:source-document-state', '{state}'),
                  ('iati:source-document-version <font color="red">rdfs:subPropertyOf dct:hasVersion</font>', '{func-version}'),
                  ('iati:source-document-license-id', '{license-func-id}'),
                  ('iati:source-document-tag', '{tag}'),
                  ('iati:source-document-relationship', '{relationship}'),
                  ('iati:resources-cache-last-updated', '{cache-last-updated}'),
                  ('iati:resources-mimetype <font color="red">rdfs:subPropertyOf dct:format</font>', '{mimetype}'),
                  ('iati:resources-resource-group-id', '{resource-group-id}'),
                  ('iati:resources-hash', '{hash}'),
                  ('iati:resources-description <font color="red">rdfs:subPropertyOf dct:description</font>', '{description}'),
                  ('iati:resources-format', '{format}'),
                  ('iati:resources-url', '{url}'),
                  ('iati:resources-cache-url', '{cache-url}'),
                  ('iati:resources-webstore-url', '{webstore-url}'),
                  ('iati:resources-package-id', '{package-id}'),
                  ('iati:resources-mimetype-inner', '{mimetype-inner}'),
                  ('iati:resources-webstore-last-updated', '{webstore-last-updated}'),
                  ('iati:resources-last-modified', '{last-modified}'),
                  ('iati:resources-position', '{position}'),
                  ('iati:resources-size', '{size}'),
                  ('iati:resources-id', '{id}'),
                  ('iati:resources-type', '{type}'),
                  ('iati:resources-name', '{name}'),
                  ('iati:source-document-group', '{group}'),
                  ('iati:source-document-isopen', '{isopen}'),
                  ('iati:source-document-notes-rendered', '{notes-rendered}'),
                  ('iati:source-document-url', '{source-document-url}'),
                  ('iati:source-document-ckan-url', '{ckan-url}'),
                  ('iati:source-document-notes', '{notes}'),
                  ('iati:source-document-title', '{title}'),
                  ('iati:source-document-ratings-average', '{rating-average}'),
                  ('iati:source-document-ratings-count', '{rating-count}'),
                  ('iati:source-document-revision-id', '{revision-id}'),
                  ('iati:extras-publisher-iati-id <font color="red">rdfs:subPropertyOf dct:publisher</font>', 'iati:codelist/OrganisationIdentifier/{code}'),
                  ('iati:extras-activity-period-from', '[activity-period-from}'),
                  ('iati:extras-activity-period-to', '{activity-period-to}'),
                  ('iati:extras-archive-file', '{archive-file}'),
                  ('iati:extras-verified', '{verified}'),
                  ('iati:extras-publisher-organization-type', 'iati:codelist/OrganisationType/{code}'),
                  ('iati:extras-language <font color="red">rdfs:subPropertyOf dct:language</font>', '{language}'),
                  ('iati:extras-country', 'iati:codelist/Country/{code}'),
                  ('iati:extras-filetype', '{filetype}'),
                  ('iati:extras-record-updated', '{record-updated}'),
                  ('iati:extras-publisher-country', 'iati:codelist/Country/{code}'),
                  ('iati:extras-data-updated', '{data-updated}'),
                  ('iati:extras-publishertype', '{publishertype}'),
                  ('iati:extras-donor', '{donor}'),
                  ('iati:extras-donor-country', '{donor-country}'),
                  ('iati:extras-donor-type', '{donor-type}'),
                  ('iati:extras-department', '{department}')]),
                
                ('<a name="maintainer"></a>iati:graph/{entity}/{entity-id}/maintainer',
                 '''The URI for indicating who is maintaining the source document.''',
                 [('rdf:type', 'iati:maintainer <font color="red">rdfs:subClassOf foaf:Agent</font>'),
                  ('iati:maintainer-name <font color="red">rdfs:subPropertyOf foaf:name</font>', '{maintainer-name}'),
                  ('iati:maintainer-email <font color="red">rdfs:subPropertyOf foaf:mbox</font>', '{maintainer-email}')]),
                
                ('<a name="author"></a>iati:graph/{entity}/{entity-id}/author',
                 '''The URI for indicating the author of the source document.''',
                 [('rdf:type', 'iati:author <font color="red">rdfs:subClassOf foaf:Agent</font>'),
                  ('iati:author-name <font color="red">rdfs:subPropertyOf foaf:name</font>', '{author-name}'),
                  ('iati:author-email <font color="red">rdfs:subPropertyOf foaf:mbox</font>', '{author-email}')]),
                
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
class Provenance(webapp.RequestHandler):
    def get(self):
        
        nav, subnav = iati2lod_navigation.navigation()
        
        nav = nav.replace('<a href="/model">', '<a id="select" href="/model">')
        subnav = subnav['Model'].replace('<a href="/model/provenance">', '<a id="select" href="/model/provenance">')
        
        contents = get_contents()
        
        index = create_index(contents)
        
        values = {"type":'Provenance',
                  "contents": contents,
                  "index": index,
                  "nav": nav,
                  "subnav": subnav}
        
        self.response.out.write(template.render('model-description.html', values))

# Register the URL with the responsible classes
application = webapp.WSGIApplication([('/model/provenance', Provenance)], debug=True)

# Register the wsgi application to run
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main() 