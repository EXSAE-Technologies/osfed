class Doc:
    def __init__(self, name="index"):
        self.children = []
        self.childObjects = []
        self.name = name
    
    def __str__(self):
        return "Document"
    
    def addChild(self, element):
        index = len(self.childObjects)
        obj = {"index": index, "el": element}
        self.childObjects.append(obj)
        self.children.append(index)

class Attribute:
    def __init__(self, key, value=""):
        self.key = key
        self.value = value
    
    def __str__(self):
        return "Attribute"

class El:
    def __init__(self, name="p", type="closed", attributes=[]):
        self.type = type
        self.children = []
        self.name = name
        self.classes = []
        self.attributes = attributes

    def __str__(self):
        return "Element"
        
    def addChild(self, element, document):
        index = len(document.childObjects)
        obj = {"index": index, "el": element}
        document.childObjects.append(obj)
        self.children.append(index)

class Text:
    def __init__(self, value=""):
        self.value = value
    
    def __str__(self):
        return "Text"

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

def generateElement(elementIndex, document):
    element = document.childObjects[elementIndex]["el"]
    if element.__str__() == "Element":
        html = "<" + element.name + " "

        if element.classes: 
            html += " class='"
            for _class in element.classes:
                html += _class + " "
            html += "' "

        for attribute in element.attributes:
            html += attribute.key
            if attribute.value == "":
                pass
            else:
                html += "='" + attribute.value + "' "
        
        html += ">"

        for child in element.children:
            html += generateElement(child, document)

        if element.type == "closed":
            html += "</" + element.name + ">"
    
    else:
        html = element.value

    return html

def genereteDocument(document):
    html = ""

    for child in document.children:
        html += generateElement(child, document)

    return html

#print(genereteDocument(new_document()))