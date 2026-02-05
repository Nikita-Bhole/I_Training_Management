from django import template

register = template.Library()

@register.filter
def get_teacher_for_subject(teachers, subject_id):
    for t in teachers:
        if t.subjects.filter(id=subject_id).exists():
            return t.id
    return ''
