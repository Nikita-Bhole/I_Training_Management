from django.urls import path
from . import views
from .views import e_get_subject_teacher
from django.conf import settings
from django.conf.urls.static import static

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
    path('batches/<int:batch_id>/students/', views.batch_students, name='batch_students'),
    path('student/<int:student_id>/result/', views.student_result, name='student_result'),
    path('student/<int:student_id>/view/', views.student_view, name='student_view'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),




]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])



