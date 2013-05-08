def navigation():
    nav = '''<a href="/">Home</a> | 
                  <a href="/model">Model</a>'''
    
    subnav = {}
    
    subnav['Home'] = '<a href="/">Home</a>'
    
    subnav['Model'] = '''
    <a href="/model">Home</a> | 
    <a href="/model/activities">Activities</a> | 
    <a href="/model/organisations">Organisations</a> | 
    <a href="/model/codelists">Codelists</a> | 
    <a href="/model/provenance">Provenance</a> | 
    <a href="/model/visualizations">Visualizations</a> | 
    <a href="/model/examples">Examples</a>
    '''
    
    return nav, subnav