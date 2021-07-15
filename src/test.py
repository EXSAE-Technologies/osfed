import api

document = api.Doc()

doctype = api.El()
doctype.name = "!DOCTYPE"
doctype.attributes.append({"key":"html", "value":""})
document.addChild(doctype)

html = api.El()
html.type = "closed"
html.name = "html"
document.addChild(html)

text = api.Text("Hello World")
html.addChild(text, document)

print(api.genereteDocument(document))
print(document.childObjects)