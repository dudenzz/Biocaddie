__author__ = 'Jakub Dutkiewicz'

from xml.etree import ElementTree as ET

class MeshItem:
    def __init__(self, xml):
        self.id = xml[0].text
        self.name = xml[1][0].text
        self.additional_names = []
        for i in xml:
            if i.tag == 'ConceptList':
                self.additional_names.append(i[1][0].text)
class Mesh:
    def __init__(self, file):
        self.tree = ET.parse(file)
        self.root = self.tree.getroot()
        self.items = []
    def parseItems(self):
        for item in self.root:
            self.items.append(MeshItem(item))
    def synonyms(self):
        ret = ''
        for item in self.items:
            ret += item.name
            for k in item.additional_names:
                ret += ' ' + k
        return ret


m = Mesh('//mnt/raid0/kuba/trec_data/scripts/mesh-qe/desc2016.xml')
m.parseItems()
print m.synonyms()