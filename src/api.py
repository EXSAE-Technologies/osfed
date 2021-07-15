class Doc:
    def __init__(self):
        self.children = []
        self.childObjects = []
    
    def __str__(self):
        return "Document"
    
    def addChild(self, element):
        index = len(self.childObjects)
        obj = {"index": index, "el": element}
        self.childObjects.append(obj)
        self.children.append(index)

class El:
    def __init__(self):
        self.type = "open"
        self.children = []
        self.name = ""
        self.classes = []
        self.attributes = []

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
            html += attribute["key"]
            if attribute["value"] == "":
                pass
            else:
                html += "='" + attribute["value"] + "' "
        
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

