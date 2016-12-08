from django import template

register = template.Library()

@register.filter(name="duration")
def duration(duration):
    seconds = int(duration.total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if hours > 24:
        days = (seconds % 3600) // 24
        hours = (seconds - (days * 3600 * 24)) // 60

    if days:
        return '{} hours {} minutes and {} seconds'.format(hours, minutes, seconds)
    else:
        return '{} days, {} hours {} minutes and {} seconds'.format(days, hours, minutes, seconds)
