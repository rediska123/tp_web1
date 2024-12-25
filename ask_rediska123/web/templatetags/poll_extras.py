from django import template
from web.models import *
from django.core.cache import cache

register = template.Library()

@register.inclusion_tag('popular_tags.html')
def popular_tags():
    tags = cache.get("tags")
    if not tags:
        tags = tag.objects.popular_tags()
        cache.set("tags", tags, timeout=60*15) # Кэшируем на 15 минут
    return {'tags': tags}
        
@register.inclusion_tag('popular_profiles.html')
def popular_profiles():
    profiles = cache.get("profiles")
    if not profiles:
        profiles = profile.objects.popular_profiles()
        cache.set("profiles", profiles, timeout=60*15)  # Кэшируем на 15 минут
    return {'profiles': profiles}

