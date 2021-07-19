import api

document = api.Doc()

doctype = api.El(name="!DOCTYPE", type="open", attributes=[api.Attribute("html")])
document.addChild(doctype)

html = api.El("html", attributes=[api.Attribute("class", "no-js"), api.Attribute("id", "d01")])
document.addChild(html)

html.addChild(api.Text("Hello World"), document)
html.addChild(api.Text("Hello Fundu"), document)
html.addChild(api.Text("Hello Shangs"), document)

def show():
    global document
    global api
    return api.generateDocument(document)

print(show())