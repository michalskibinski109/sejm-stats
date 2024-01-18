import wikipedia

wikipedia.set_lang("pl")
page_name = wikipedia.search("Andrzej Duda")[0]
res = wikipedia.page(page_name)
print(res.summary)
print(res.sections)
