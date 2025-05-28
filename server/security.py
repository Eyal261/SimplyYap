import bleach 

def contains_html_or_js(text):
    cleaned = bleach.clean(text)
    return cleaned != text