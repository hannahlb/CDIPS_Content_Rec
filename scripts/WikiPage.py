import xml.etree.ElementTree as ET
import pandas as pd

class WikiPage(ET.Element):
    '''
    Easily access Wikipedia page information from xml.

    INPUT
    -----
    xml.etree.ElementTree.Element
      page from XML Wikipedia data


    METHODS
    -------
    page :  xml.etree.ElementTree.Element
      page from XML Wikipedia data
    children : list 
      list of page's children, type xml.etree.ElementTree.Element
    title : str
      page title
    id : str
      xml id
    text_raw : str
      xml text content
    text_id : str
      xml id of the page text
    text_parentid : str
      xml id of the parent page
    text_timestamp : str
      timestamp of page update/creation
    text_format : str
      wikipedia xml format style
    data : pandas.DataFrame
      DataFrame with information about the page id, title, and raw_text
    webpage : str
      url
    page_type : str
      type of wiki page, e.g. article, category, file, image, list, etc
    '''
    def __init__(self, page):
        ET.Element.__init__(self, page)
                
        self.page = page
        self.children = self.page.getchildren()
        
        def get_xml_field(xml_data):
            '''returns field from xml'''
            return xml_data.tag.split('}')[1]
        
        for child in self.children:
            if get_xml_field(child) == 'title':
                self.title = child.text
            elif get_xml_field(child) == 'id':
                self.id = child.text
            elif get_xml_field(child) == 'revision':
                for gchild in child.getchildren():
                    if get_xml_field(gchild) == 'text':
                        self.text_raw = gchild.text
                    elif get_xml_field(gchild) == 'id':
                        self.text_id = gchild.text
                    elif get_xml_field(gchild) == 'parentid':
                        self.text_parentid = gchild.text
                    elif get_xml_field(gchild) == 'timestamp':
                        self.text_timestamp = gchild.text
                    elif get_xml_field(gchild) == 'format':
                        self.text_format = gchild.text
        self.website = 'https://en.wikipedia.org/wiki/%s' % (self.title.replace(' ', '_'))

        def get_page_type(title):
            if 'Category:' in title:
                return 'category'
            elif 'Portal:' in title:
                return 'portal'
            elif 'List of' in title:
                return 'list'
            elif 'File:' in title:
                return 'file'
            else:
                return 'article'
        self.page_type = get_page_type(self.title)

        self.data = pd.DataFrame(columns=['website', 'page_type', 'text_raw'])
        self.data.loc[self.id] = [self.website, self.page_type, self.text_raw]
