from django import template
from django.utils.safestring import mark_safe
import re 

register = template.Library()

@register.filter
def highlight_search(text,search_query):
    if not text or not search_query:
        return text
    
    pattern = re.compile(r'('+re.escape(search_query)+r')', re.IGNORECASE)
    highlighted_text = pattern.sub(r'<span class="highlight">\1</span>',text)
    return mark_safe(highlighted_text)
