from surv import app
from surv.utils.helpers import htmlify2

@app.template_filter('linkify')
def linkify(thing):
    try:
        return htmlify2(thing)
    except:
        return thing
