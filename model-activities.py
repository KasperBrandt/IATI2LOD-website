## By Kasper Brandt
## Last updated on 08-05-2013

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import iati2lod_navigation

def get_contents():
    contents = [('<a name="activity"></a>iati:activity/{activity-id}', 
                 '''The main URI referencing an activity. The activity ID is required, meaning that activities 
                 without a IATI ID specified cannot be transformed into linked data URIs and will therefore be
                 ignored in the conversion process.''',
                 [('rdf:type', 'iati:activity'),
                  ('owl:sameAs', '{linked-data-uri}'),
                  ('rdfs:label', '{title}'),
                  ('iati:activity-id <font color="red">rdfs:subPropertyOf dct:identifier</font>', '{activity-id}'),
                  ('iati:activity-hierarchy', '{hierarchy}'),
                  ('iati:activity-reporting-org', '''<a href="#reporting-org">iati:activity/{activity-id}/reporting-org/{ref}</a><br>
                  or<br>
                  <a href="#reporting-org">iati:activity/{activity-id}/reporting-org{count}'''),
                  ('iati:activity-other-identifier', '<a href="#other-identifier">iati:activity/{activity-id}/other-identifier{count}</a>'),
                  ('iati:activity-website', '{website}'),
                  ('iati:activity-description', '<a href="#description">iati:activity/{activity-id}/description{count}</a>'),
                  ('iati:activity-status', 'iati:codelist/ActivityStatus/{code}'),
                  ('iati:start-actual-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{date}'),
                  ('iati:start-actual-date-text', '{text}'),
                  ('iati:end-actual-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{date}'),
                  ('iati:end-actual-date-text', '{text}'),
                  ('iati:start-planned-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{date}'),
                  ('iati:start-planned-date-text', '{text}'),
                  ('iati:end-planned-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{date}'),
                  ('iati:end-planned-date-text', '{text}'),
                  ('iati:activity-contact-info', '<a href="#contact-info">iati:activity/{activity-id}/contact-info{count}</a>'),
                  ('iati:activity-participating-org', '''<a href="#participating-org">iati:activity/{activity-id}/participating-org/{ref}</a><br>
                  or<br>
                  <a href="#participating-org">iati:activity/{activity-id}/participating-org{count}'''),
                  ('iati:activity-recipient-country', '<a href="#recipient-country">iati:activity/{activity-id}/recipient-country/{ref}</a>'),
                  ('iati:activity-recipient-region', '<a href="#recipient-region">iati:activity/{activity-id}/recipient-region/{ref}</a>'),
                  ('iati:activity-location', '<a href="#location">iati:activity/{activity-id}/location{count}</a>'),
                  ('iati:activity-sector', '<a href="#sector">iati:activity/{activity-id}/sector/{vocabulary}/{code}</a>'),
                  ('iati:activity-policy-marker', '<a href="#policy-marker">iati:activity/{activity-id}/policy-marker/{vocabulary}/{code}</a>'),
                  ('iati:activity-collaboration-type', 'iati:codelist/CollaborationType/{code}'),
                  ('iati:activity-default-finance-type', 'iati:codelist/FinanceType/{code}'),
                  ('iati:activity-default-flow-type', 'iati:codelist/FlowType/{code}'),
                  ('iati:activity-default-aid-type', 'iati:codelist/AidType/{code}'),
                  ('iati:activity-default-tied-status', 'iati:codelist/TiedStatus/{code}'),
                  ('iati:activity-budget', '<a href="#budget">iati:activity/{activity-id}/budget{count}</a>'),
                  ('iati:activity-planned-disbursement', '<a href="#planned-disbursement">iati:activity/{activity-id}/planned-disbursement{count}</a>'),
                  ('iati:activity-transaction', '''<a href="#transaction">iati:activity/{activity-id}/transaction/{ref}</a><br>
                  or<br>
                  <a href="#transaction">iati:activity/{activity-id}/transaction{count}'''),
                  ('iati:activity-document-link', '<a href="#document-link">iati:activity/{activity-id}/document-link{count}</a>'),
                  ('iati:related-activity', '<a href="#related-activity">iati:activity/{activity-id}/related-activity/{activity-ref}</a>'),
                  ('iati:activity-condition', '<a href="#condition">iati:activity/{activity-id}/condition{count}</a>'),
                  ('iati:activity-result', '<a href="#result">iati:activity/{activity-id}/result{count}</a>')]),
                
                ('''<a name="reporting-org"></a>iati:activity/{activity-id}/reporting-org/{ref}<br>
                or<br>
                iati:activity/{activity-id}/reporting-org{count}''',
                 '''The URI for indicating which organisation is reporting. When no official IATI reference for the reporting
                 organisation is specified, a counter will be added to the URI instead of the reference.''',
                 [('rdf:type', 'iati:organisation <font color="red">rdfs:subClassOf org:Organisation</font>'),
                  ('rdfs:label', '{name}'),
                  ('iati:organisation-code', 'iati:codelist/OrganisationIdentifier/{ref}'),
                  ('iati:organisation-type', 'iati:codelist/OrganisationType/{type}')]),
                
                ('<a name="other-identifier"></a>iati:activity/{activity-id}/other-identifier{count}',
                 '''A non-IATI identifier. Since multiple other identifiers can be specified, a counter is added to the URI to distinguish 
                 between the identifiers.''',
                 [('rdfs:label', '{name}'),
                  ('iati:other-identifier-owner-ref', 'iati:codelist/OrganisationIdentifier/{owner-ref}'),
                  ('iati:other-identifier-owner-name', '{owner-name}')]),
                
                ('<a name="description"></a>iati:activity/{activity-id}/description{count}',
                 '''A description of the activity. Since it is possible to have multiple descriptions and since each description 
                 also has a type, a counter is placed behind the URI to uniquely identify the description.''',
                 [('rdf:type', 'iati:description'),
                  ('iati:description-text <font color="red">rdfs:subPropertyOf dct:description</font>', '{description}'),
                  ('iati:description-type', 'iati:codelist/DescriptionType/{code}')]),
                
                ('<a name="contact-info"></a>iati:activity/{activity-id}/contact-info{count}',
                 '''The node for supplying contact information regarding the activity. Theoretically it is possible to have multiple contact 
                 information nodes and therefore a counter is placed behind the URI to uniquely identify the contact information nodes.''',
                 [('rdf:type', 'iati:contact-info <font color="red">rdfs:subClassOf foaf:Agent</font>'),
                  ('iati:contact-info-person-name <font color="red">rdfs:subPropertyOf foaf:name</font>', '{person-name}'),
                  ('iati:contact-info-organisation <font color="red">rdfs:subPropertyOf org:memberOf</font>', '{organisation}'),
                  ('iati:contact-info-telephone <font color="red">rdfs:subPropertyOf foaf:phone</font>', '{telephone}'),
                  ('iati:contact-info-email <font color="red">rdfs:subPropertyOf foaf:mbox</font>', '{email}'),
                  ('iati:contact-info-mailing-address', '{mailing-address}')]),
                
                ('''<a name="participating-org"></a>iati:activity/{activity-id}/participating-org/{ref}<br>
                or<br>
                iati:activity/{activity-id}/participating-org{count}''',
                 '''The URI for indicating which organisation is participating. When no official IATI reference for the participating
                 organisation is specified, a counter will be added to the URI instead of the reference.''',
                 [('rdf:type', 'iati:organisation <font color="red">rdfs:subClassOf org:Organisation</font>'),
                  ('rdfs:label', '{name}'),
                  ('iati:organisation-code', 'iati:codelist/OrganisationIdentifier/{ref}'),
                  ('iati:organisation-type', 'iati:codelist/OrganisationType/{type}'),
                  ('iati:organisation-role', 'iati:codelist/OrganisationRole/{role}')]),
                
                ('<a name="recipient-country"></a>iati:activity/{activity-id}/recipient-country/{ref}',
                 '''The node for specifying the country which receives funding. A reference is needed, otherwise the 
                 country is ignored in the conversion process.''',
                 [('rdf:type', 'iati:country <font color="red">rdfs:subClassOf geo:location</font>'),
                  ('rdfs:label', '{name}'),
                  ('iati:country-code', 'iati:codelist/Country/{ref}'),
                  ('iati:percentage', 'iati:percentage')]),
                
                ('<a name="recipient-region"></a>iati:activity/{activity-id}/recipient-region/{ref}',
                 '''The node for specifying the region which receives funding. A reference is needed, otherwise the 
                 region is ignored in the conversion process.''',
                 [('rdf:type', 'iati:region <font color="red">rdfs:subClassOf geo:location</font>'),
                  ('rdfs:label', '{name}'),
                  ('iati:region-code', 'iati:codelist/Region/{ref}'),
                  ('iati:percentage', 'iati:percentage')]),     

                ('<a name="location"></a>iati:activity/{activity-id}/location{count}',
                 '''Used for specifying a certain location. Since locations do not have a unique identifier, a
                 counter is placed behind the URI to distinguish between different locations.''',
                 [('rdf:type', 'iati:location <font color="red">rdfs:subClassOf geo:location</font>'),
                  ('rdfs:label', '{name}'),
                  ('iati:location-description', '<a href="#location-description">iati:activity/{activity-id}/location{count}/description{count}</a>'),
                  ('iati:location-type', 'iati:codelist/LocationType/{type}'),
                  ('iati:location-administrative', '<a href="#location-administrative">iati:activity/{activity-id}/location{count}/administative{count}</a>'),
                  ('iati:latitude <font color="red">rdfs:subPropertyOf geo:lat</font>', '{latitude}'),
                  ('iati:longitude <font color="red">rdfs:subPropertyOf geo:long</font>', '{longitude}'),
                  ('iati:coordinates-precision', 'iati:codelist/GeographicalPrecision/{code}'),
                  ('iati:gazetteer-entry', '<a href="#location-gazetteer-entry">iati:activity/{activity-id}/location{count}/gazetteer-entry{ref}</a>')]),
                 
                ('<a name="location-description"></a>iati:activity/{activity-id}/location{count}/description{count}',
                 '''A description of the location. Since it is possible to have multiple descriptions and since each description 
                 also has a type, a counter is placed behind the URI to uniquely identify the description.''',
                 [('rdf:type', 'iati:description'),
                  ('iati:description-text <font color="red">rdfs:subPropertyOf dct:description</font>', '{text}'),
                  ('iati:description-type', 'iati:codelist/DescriptionType/{type}')]),
                 
                ('<a name="location-administrative"></a>iati:activity/{activity-id}/location{count}/administrative{count}',
                 '''Used for administatrive indications of the location, such as the country, adm1 and adm2. However, the
                    codelists for the adm1 and adm2 attributes seem not to be implemented yet, therefore these attributes have been
                    modeled as literals.''',
                 [('iati:administrative-country', 'iati:codelist/Country/{code}'),
                  ('iati:administrative-country-text', '{text}'),
                  ('iati:administrative-adm1', '{adm1}'),
                  ('iati:administrative-adm2', '{adm2}')]),
                 
                 ('<a name="location-gazetteer-entry"></a>iati:activity/{activity-id}/location{count}/gazetteer-entry{ref}',
                  '''Used for indicating a Gazetteer entry, such as Geonames or Open Street Map. Unfortunately, none of the activities
                  have a gazetteer-entry element specified as of yet.''',
                  [('rdf:type', 'iati:gazetteer-entry'),
                   ('iati:gazetteer-ref', '{ref}'),
                   ('iati:gazetteer-entry', '{text}')]),
                 
                 ('<a name="sector"></a>iati:activity/{activity-id}/sector/{vocabulary}/{code}',
                  '''Indicating the sector of an activity. Since the codes are dependant of the indicated vocabulary for their
                  interpretation, the vocabulary has been integrating within the URI.''',
                  [('rdf:type', 'iati:sector'),
                   ('iati:rdfs:label', '{name}'),
                   ('iati:sector-code', '{code}'),
                   ('iati:sector-vocabulary', '{vocabulary}'),
                   ('iati:percentage', '{percentage}')]),
                 
                 ('<a name="policy-marker"></a>iati:activity/{activity-id}/policy-marker/{vocabulary}/{code}',
                  '''Indicating the policy-marker of an activity. Since the codes are dependant of the indicated vocabulary for their
                  interpretation, the vocabulary has been integrating within the URI.''',
                  [('rdf:type', 'iati:policy-marker'),
                   ('rdfs:label', '{name}'),
                   ('iati:policy-marker-code', '{code}'),
                   ('iati:policy-marker-vocabulary', '{vocabulary}'),
                   ('iati:significance', '{significance}')]),
                 
                 ('<a name="budget"></a>iati:activity/{activity-id}/budget{count}',
                  '''Used for specifying a budget of the activity. Since budgets don't have an identifier, a counter is added
                  to the URI for each budget to uniquely identify a budget.''',
                  [('rdf:type', 'iati:budget'),
                   ('iati:budget-type', 'iati:codelist/BudgetType/{type}'),
                   ('iati:start-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{start-date}'),
                   ('iati:start-date-text', '{start-date-text}'),
                   ('iati:end-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{end-date}'),
                   ('iati:end-date-text', '{end-date-text}'),
                   ('iati:value', '{value}'),
                   ('iati:value-currency', 'iati:codelist/Currency/{currency}'),
                   ('iati:value-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{value-date}')]),
                 
                 ('<a name="planned-disbursement"></a>iati:activity/{activity-id}/planned-disbursement{count}',
                  '''Used for specifying a planned disbursement of the activity. Since planned disbursements don't have an identifier, 
                  a counter is added to the URI for each budget to uniquely identify a planned disbursement.''',
                  [('rdf:type', 'iati:planned-disbursement'),
                   ('iati:updated <font color="red">rdfs:subPropertyOf dct:modified</font>', '{updated}'),
                   ('iati:start-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{start-date}'),
                   ('iati:start-date-text', '{start-date-text}'),
                   ('iati:end-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{end-date}'),
                   ('iati:end-date-text', '{end-date-text}'),
                   ('iati:value', '{value}'),
                   ('iati:value-currency', 'iati:codelist/Currency/{currency}'),
                   ('iati:value-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{value-date}')]),
                 
                 ('''<a name="transaction"></a>iati:activity/{activity-id}/transaction/{ref}<br>
                or<br>
                iati:activity/{activity-id}/transaction{count}''',
                  '''Used for specifying a transaction of the activity. If an identifier is specified for the transaction, then 
                  that identifier is used in the URI to specify the transaction. Otherwise, a counter is added to the URI to uniquely 
                  identify the transaction.''',
                  [('rdf:type', 'iati:transaction'),
                   ('iati:transaction-ref', '{ref}'),
                   ('iati:transaction-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{date}'),
                   ('iati:value', '{value'),
                   ('iati:value-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{value-date}'),
                   ('iati:aid-type', 'iati:codelist/AidType/{aid-type}'),
                   ('iati:disbursement-channel', 'iati:codelist/disbursementChannel/{disbursement-channel}'),
                   ('iati:finance-type', 'iati:codelist/FinanceType/{finance-type}'),
                   ('iati:flow-type', 'iati:codelist/FlowType/{flow-type}'),
                   ('iati:tied-status', 'iati:codelist/TiedStatus/{tied-status}'),
                   ('iati:transaction-type', 'iati:codelist/TransactionType/{transaction-type}'),
                   ('iati:transaction-description', '''<a href="#transaction-description">iati:activity/{activity-id}/transaction/{ref}/description{count}</a><br>
                  or<br>
                  <a href="#transaction-description">iati:activity/{activity-id}/transaction{count}/description{count}'''),
                   ('iati:provider-org', 'iati:codelist/OrganisationIdentifier/{ref}'),
                   ('iati:provider-org-name', '{provider-org-name}'),
                   ('iati:provider-org-activity-id', 'iati:activity/{activity-id}'),
                   ('iati:receiver-org', 'iati:codelist/OrganisationIdentifier/{ref}'),
                   ('iati:receiver-org-name', '{receiver-org-name}'),
                   ('iati:receiver-org-activity-id', 'iati:activity/{activity-id}')]),
                 
                 ('''<a name="transaction-description"></a>iati:activity/{activity-id}/transaction/{ref}/description{count}<br>
                  or<br>
                  iati:activity/{activity-id}/transaction{count}/description{count}''',
                  '''A description of the transaction. Since it is possible to have multiple descriptions and since each description 
                  also has a type, a counter is placed behind the URI to uniquely identify the description.''',
                  [('rdf:type', 'iati:description'),
                   ('iati:description-text', '{text}'),
                   ('iati:description-type', 'iati:codelist/DescriptionType/{type}')]),
                 
                 ('<a name="document-link"></a>iati:activity/{activity-id}/document-link{count}',
                  '''Used to indicate a link to a document. Since it is possible to have multiple links to documents, a counter 
                  is added to the URI.''',
                  [('rdf:type', 'iati:document-link'),
                   ('rdfs:label', '{title}'),
                   ('iati:url', '{url}'),
                   ('iati:format <font color="red">rdfs:subPropertyOf dct:hasFormat</font>', '{format}'),
                   ('iati:document-category', 'iati:codelist/DocumentCategory/{category}'),
                   ('iati:language <font color="red">rdfs:subPropertyOf dct:language</font>', '{language}'),
                   ('iati:language-text', '{language-text}')]),
                
                ('<a name="related-activity"></a>iati:activity/{activity-id}/related-activity/{activity-ref}',
                 '''Used for indicating a related activity. A reference to another activity is needed, otherwise this 
                 node is ignored during the conversion process.''',
                 [('iati:activity', 'iati:activity/{activity-ref}'),
                  ('rdfs:label', '{name}'),
                  ('iati:related-activity-id', '{activity-ref}'),
                  ('iati:related-activity-type', 'iati:codelist/RelatedActivityType/{type}')]),
                
                ('<a name="condition"></a>iati:activity/{activity-id}/condition{count}',
                 '''Used for indivating a condition of the activity. Since a condition does not have an identifier, a counter 
                 is placed behind the URI to uniquely identify the condition.''',
                 [('rdf:type', 'iati:condition'),
                  ('rdfs:label', '{text}'),
                  ('iati:condition-type', 'iati:codelist/ConditionType/{type}')]),
                
                ('<a name="result"></a>iati:activity/{activity-id}/result{count}',
                 '''Used to indicate a result of the activity. Since a result does not have an identifier, a counter 
                 is placed behind the URI to uniquely identify the result.''',
                 [('rdf:type', 'iati:result'),
                  ('rdfs:label', '{title}'),
                  ('iati:result-description', '<a href="#result-description">iati:activity/{activity-id}/result{count}/description{count}</a>'),
                  ('iati:result-indicator', '<a href="#result-indicator">iati:activity/{activity-id}/result{count}/indicator{count}</a>')]),
                
                ('<a name="result-description"></a>iati:activity/{activity-id}/result{count}/description{count}',
                 '''A description of the result. Since it is possible to have multiple descriptions and since each description 
                  also has a type, a counter is placed behind the URI to uniquely identify the description.''',
                  [('rdf:type', 'iati:description'),
                   ('iati:description-text <font color="red">rdfs:subPropertyOf dct:description</font>', '{text}'),
                   ('iati:description-type', 'iati:codelist/DescriptionType/{type}')]),
                
                ('<a name="result-indicator"></a>iati:activity/{activity-id}/result{count}/indicator{count}',
                 '''An indicator of the result. Since it is possible to have multiple indocators and since each indicator 
                  has multiple attributes, a counter is placed behind the URI to uniquely identify the indicator.''',
                  [('rdf:type', 'iati:indicator'),
                   ('rdfs:label', '{title}'),
                   ('iati:indicator-measure', 'iati:codelist/IndicatorMeasure/{code}'),
                   ('iati:indicator-ascending', '{ascending}'),
                   ('iati:indicator-description', '<a href="#indicator-description">iati:activity/{activity-id}/result{count}/indicator{count}/description{count}</a>'),
                   ('iati:indicator-period', '<a href="#indicator-period">iati:activity/{activity-id}/result{count}/indicator{count}/period{count}</a>'),
                   ('iati:baseline-value', '{baseline-value}'),
                   ('iati:baseline-year <font color="red">rdfs:subPropertyOf dct:date</font>', '{baseline-year}'),
                   ('iati:baseline-comment', '{baseline-comment}')]),
                
                ('<a name="indicator-description"></a>iati:activity/{activity-id}/result{count}/indicator{count}/description{count}',
                 '''A description of the indicator. Since it is possible to have multiple descriptions and since each description 
                  also has a type, a counter is placed behind the URI to uniquely identify the description.''',
                  [('rdf:type', 'iati:description'),
                   ('iati:description-text <font color="red">rdfs:subPropertyOf dct:description</font>', '{text}'),
                   ('iati:description-type', 'iati:codelist/DescriptionType/{type}')]),
                
                ('<a name="indicator-period"></a>iati:activity/{activity-id}/result{count}/indicator{count}/period{count}',
                 '''Used for indicating the period of an indicator. Since it is possible to have multiple periods and since each period 
                  has its own target and actual value, a counter is placed behind the URI to uniquely identify the period.''',
                  [('rdf:type', 'iati:period <font color="red">rdfs:subClassOf dct:PeriodOfTime</font>'),
                   ('iati:start-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{start-date}'),
                   ('iati:start-date-text', '{start-date-text}'),
                   ('iati:end-date <font color="red">rdfs:subPropertyOf dct:date</font>', '{end-date}'),
                   ('iati:end-date-text', '{end-date-text}'),
                   ('iati:target', '{target}'),
                   ('iati:actual', '{actual}')])                
                
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
class Activities(webapp.RequestHandler):
    def get(self):
        
        nav, subnav = iati2lod_navigation.navigation()
        
        nav = nav.replace('<a href="/model">', '<a id="select" href="/model">')
        subnav = subnav['Model'].replace('<a href="/model/activities">', '<a id="select" href="/model/activities">')
        
        contents = get_contents()
        
        index = create_index(contents)
        
        values = {"type":'Activities',
                  "contents": contents,
                  "index": index,
                  "nav": nav,
                  "subnav": subnav}
        
        self.response.out.write(template.render('model-description.html', values))

# Register the URL with the responsible classes
application = webapp.WSGIApplication([('/model/activities', Activities)], debug=True)

# Register the wsgi application to run
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main() 