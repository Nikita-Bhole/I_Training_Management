from django.contrib import admin
from .models import Subject, Course, Teacher, Student, Batch

admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Batch)
