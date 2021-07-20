from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
import os

class Doc:
    def __init__(self, name="index", json=None):
        self.children = []
        self.childObjects = []
        self.name = name

        if json != None:
            self.new_from_json(json)
    
    def __str__(self):
        return "Document"
    
    def deleteChild(self, index):
        for a in self.childObjects:
            for b in a.children:
                if int(b) == int(index):
                    a.children.remove(b)
    
    def addChild(self, element):
        index = len(self.childObjects)
        element.osfed = str(index)
        self.childObjects.append(element)
        self.children.append(index)
    
    def new_from_json(self, json):
        obj = JSONDecoder().decode(json)
        self.name = obj["name"]
        self.children = obj["children"]
        self.childObjects = []
        for child in obj["childObjects"]:
            elem = El(json=JSONEncoder().encode(child))
            self.childObjects.append(elem)
    
    def to_dict(self):
        obj = dict()
        obj["name"] = self.name
        obj["children"] = self.children
        obj["childObjects"] = list()
        for childObject in self.childObjects:
            obj["childObjects"].append(childObject.to_dict())
        
        return obj

class Attribute:
    def __init__(self, key="", value="", json=None):
        self.key = key
        self.value = value

        if json != None:
            obj = JSONDecoder().decode(json)
            self.key = obj["key"]
            self.value = obj["value"]
    
    def __str__(self):
        return "Attribute"
    
    def to_dict(self):
        obj = dict()
        obj["key"] = self.key
        obj["value"] = self.value
        return obj

class El:
    def __init__(self, name="p", type="closed", attributes=[], json=None):
        self.type = type
        self.children = []
        self.name = name
        self.classes = []
        self.attributes = attributes
        self.osfed = ""
        self.innerHTML = ""

        if json != None:
            self.new_from_json(json)

    def __str__(self):
        return "Element"
    
    def to_dict(self):
        obj = dict()
        obj["osfed"] = self.osfed
        obj["type"] = self.type
        obj["name"] = self.name
        obj["classes"] = self.classes
        obj["attributes"] = list()
        obj["innerHTML"] = self.innerHTML
        obj["children"] = self.children

        for attribute in self.attributes:
            obj["attributes"].append(attribute.to_dict())
        
        return obj
        
    def addChild(self, element, document):
        index = len(document.childObjects)
        element.osfed = str(index)
        document.childObjects.append(element)
        self.children.append(index)

    def add_class(self, class_name, document):
        self.classes.append(class_name)
    
    def new_from_json(self, json):
        obj = JSONDecoder().decode(json)
        self.osfed = obj["osfed"]
        self.type = obj["type"]
        self.name = obj["name"]
        self.classes = obj["classes"]
        self.attributes = []
        self.innerHTML = obj["innerHTML"]
        self.children = obj["children"]
        for attribute in obj["attributes"]:
            attr = Attribute(json=JSONEncoder().encode(attribute))
            self.attributes.append(attr)

class Text(El):
    def __init__(self, value=""):
        El.__init__(self, "span")
        self.innerHTML = value
    
    def __str__(self):
        return super().__str__()

def new_document(name="new"):
    document = Doc(name)

    doctype = El(name="!DOCTYPE", type="open", attributes=[Attribute("html")])
    document.addChild(doctype)

    html = El(name="html")
    document.addChild(html)

    body = El(name="body")
    html.addChild(body, document)

    h1 = El(name="h1")
    body.addChild(h1, document)

    text = Text("Hellow World")
    h1.addChild(text, document)

    return document

def open_from_file(filepath):
    file = open(filepath, "r")
    return Doc(json=file.read())

def export_to_json(filepath, document):
    file = open(filepath, "w")
    obj = document.to_dict()
    json = JSONEncoder().encode(obj)
    file.write(json)

def generateElement(elementIndex, document):
    element = document.childObjects[elementIndex]
    if element.__str__() == "Element":
        html = "<" + element.name + " osfed='" + element.osfed + "' "

        if element.classes: 
            html += " class='"
            for _class in element.classes:
                html += _class + " "
            html += "' "

        for attribute in element.attributes:
            html += attribute.key
            if attribute.value == "":
                html += " "
            else:
                html += "='" + attribute.value + "' "
        
        html += ">" + element.innerHTML

        for child in element.children:
            html += generateElement(child, document)

        if element.type == "closed":
            html += "</" + element.name + ">"
    
    else:
        html = element.value

    return html

def generateDocument(document):
    html = ""

    for i in range(len(document.children)):
        html += generateElement(i, document)

    return html

#document = open_from_file(os.path.dirname(__file__)+"/tmp/template.json")
#document = new_document(name="sample")
#export_to_json(os.path.dirname(__file__)+"/tmp/template.json", document)
#print(generateDocument(document))