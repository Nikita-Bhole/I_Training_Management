from django.urls import path
from . import views
from .views import e_get_subject_teacher

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('courses/', views.course_list, name='course_list'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('students/', views.student_list, name='student_list'),
    path('batches/', views.batch_list, name='batch_list'),
    path('ajax/get-subjects/', views.get_subjects, name='get_subjects'),
    path('ajax/get-teachers/', views.get_teachers, name='get_teachers'),
    path('get_subject_teacher/', views.e_get_subject_teacher, name='get_subject_teacher'),
    path('batches/get-batch-subject-teacher-map/', views.e_get_subject_teacher, name='get_batch_subject_teacher_map'),

]



