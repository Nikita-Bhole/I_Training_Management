from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from S_CRUD.models import Course, Subject, Teacher, Student, Batch, BatchSubject
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
import json
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from .models import StudentResult

def subject_list(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if 'delete_id' in request.POST:
            subject = get_object_or_404(Subject, id=request.POST.get('delete_id'))
            subject.is_archived = True
            subject.save()
            return JsonResponse({'status': 'success', 'message': 'Deleted Successfully!'})
        elif request.POST.get('id'):
            subject = get_object_or_404(Subject, id=request.POST.get('id'), is_archived=False)
            subject.name = request.POST.get('name')
            subject.code = request.POST.get('code')
            subject.save()
            return JsonResponse({'status': 'success', 'id': subject.id, 'name': subject.name, 'code': subject.code})
        else:
            subject = Subject.objects.create(
                name=request.POST.get('name'),
                code=request.POST.get('code'),
                is_archived=False
            )
            return JsonResponse({'status': 'success', 'id': subject.id, 'name': subject.name, 'code': subject.code})
    elif request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        page_number = request.GET.get('page', 1)
        subjects = Subject.objects.filter(is_archived=False).order_by('id')
        paginator = Paginator(subjects, 5)
        page_obj = paginator.get_page(page_number)
        return render(request, 'subjects/subject_table.html', {'subjects': page_obj, 'page_obj': page_obj})
    return render(request, 'subjects/index.html')


def course_list(request):
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        if 'delete_id' in request.POST:
            course = get_object_or_404(Course, id=request.POST.get('delete_id'), is_archived=False)
            course.is_archived = True
            course.save()
            return JsonResponse({'status': 'success', 'message': 'Course deleted successfully'})

        
        elif request.POST.get('id'):
            course = get_object_or_404(Course, id=request.POST.get('id'), is_archived=False)
            course.course_id = request.POST.get('course_id')
            course.name = request.POST.get('name')
            course.subjects.set(request.POST.getlist('subjects[]'))
            course.save()
            return JsonResponse({'status': 'success', 'message': 'Course updated successfully'})

        
        else:
            course = Course.objects.create(
                course_id=request.POST.get('course_id'),
                name=request.POST.get('name'),
                is_archived=False
            )
            course.subjects.set(request.POST.getlist('subjects[]'))
            return JsonResponse({'status': 'success', 'message': 'Course added successfully'})

    
    elif request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        page_number = request.GET.get('page', 1)
        course_ids = request.GET.getlist('course_ids[]')  

        courses = Course.objects.filter(is_archived=False).order_by('id')

        if course_ids:  
            courses = courses.filter(id__in=course_ids)

        paginator = Paginator(courses, 5)  
        page_obj = paginator.get_page(page_number)
        return render(request, 'courses/course_table.html', {'courses': page_obj, 'page_obj': page_obj})

    subjects = Subject.objects.filter(is_archived=False)
    courses = Course.objects.filter(is_archived=False).order_by('id')
    return render(request, 'courses/course.html', {'subjects': subjects, 'courses': courses})



def teacher_list(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if 'delete_id' in request.POST:
            teacher = get_object_or_404(Teacher, id=request.POST.get('delete_id'))
            teacher.is_archived = True
            teacher.save()
            return JsonResponse({'status': 'success', 'message': 'Teacher deleted successfully'})
        elif request.POST.get('id'):
            teacher = get_object_or_404(Teacher, id=request.POST.get('id'), is_archived=False)
            teacher.teacher_id = request.POST.get('teacher_id')
            teacher.name = request.POST.get('name')
            teacher.subjects.set(request.POST.getlist('subjects[]'))
            teacher.save()
            return JsonResponse({'status': 'success', 'message': 'Teacher updated successfully'})
        else:
            teacher = Teacher.objects.create(
                teacher_id=request.POST.get('teacher_id'),
                name=request.POST.get('name'),
                is_archived=False
            )
            teacher.subjects.set(request.POST.getlist('subjects[]'))
            return JsonResponse({'status': 'success', 'message': 'Teacher added successfully'})
    elif request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        page_number = request.GET.get('page', 1)
        subject_filter = request.GET.get('subject')
        teachers = Teacher.objects.filter(is_archived=False)
        if subject_filter:
            teachers = teachers.filter(subjects__id=subject_filter)
        teachers = teachers.distinct().order_by('id')
        paginator = Paginator(teachers, 5)
        page_obj = paginator.get_page(page_number)
        return render(request, 'teachers/teacher_table.html', {'teachers': page_obj, 'page_obj': page_obj})
    subjects = Subject.objects.filter(is_archived=False)
    return render(request, 'teachers/teacher.html', {'subjects': subjects})


def student_list(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if 'delete_id' in request.POST:
            student = get_object_or_404(Student, id=request.POST.get('delete_id'))
            student.is_archived = True
            student.save()
            return JsonResponse({'status': 'success', 'message': 'Student deleted successfully'})

        elif request.POST.get('id'):
            student = get_object_or_404(Student, id=request.POST.get('id'), is_archived=False)
            student.name = request.POST.get('name')
            batch_id = request.POST.get('batch')
            student.batch = Batch.objects.get(id=batch_id) if batch_id else None
            student.courses.set(request.POST.getlist('courses[]'))
            student.subjects.set(request.POST.getlist('subjects[]'))
            student.save()
            return JsonResponse({'status': 'success', 'message': 'Student updated successfully'})

        else:
            name = request.POST.get('name')
            batch_id = request.POST.get('batch')
            batch = Batch.objects.get(id=batch_id) if batch_id else None
            student = Student.objects.create(name=name, batch=batch, is_archived=False)
            student.courses.set(request.POST.getlist('courses[]'))
            student.subjects.set(request.POST.getlist('subjects[]'))
            return JsonResponse({'status': 'success', 'message': 'Student added successfully'})

    elif request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        page_number = request.GET.get('page', 1)
        selected_names = request.GET.getlist('student_names[]')  # names from multi-select

        students_qs = Student.objects.filter(is_archived=False).order_by('id')

        if selected_names:
            students_qs = students_qs.filter(name__in=selected_names)

        paginator = Paginator(students_qs, 5)
        page_obj = paginator.get_page(page_number)
        return render(request, 'students/student_table.html', {'students': page_obj, 'page_obj': page_obj})

    
    students = Student.objects.filter(is_archived=False).order_by('name')
    batches = Batch.objects.filter(is_archived=False)
    courses = Course.objects.filter(is_archived=False)
    subjects = Subject.objects.filter(is_archived=False)
    
    student_names = Student.objects.filter(is_archived=False).values_list('name', flat=True).distinct()

    return render(request, 'students/student.html', {
        'students': student_names,  
        'batches': batches,
        'courses': courses,
        'subjects': subjects
    })



def batch_list(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        
        if 'delete_id' in request.POST:
            batch = get_object_or_404(Batch, id=request.POST.get('delete_id'))
            batch.is_archived = True
            batch.save()
            return JsonResponse({'status': 'success', 'message': 'Batch deleted successfully'})

        
        batch_id = request.POST.get("id")
        name = request.POST.get("name")
        course_id = request.POST.get("course")
        start_date = request.POST.get("start_date")
        duration = request.POST.get("duration")
        assignments_json = request.POST.get("subject_teachers")
        assignments = json.loads(assignments_json) if assignments_json else {}

        if batch_id:  
            batch = get_object_or_404(Batch, id=batch_id, is_archived=False)
            batch.name = name
            batch.course_id = course_id
            batch.start_date = start_date
            batch.duration = duration
            batch.save()
        else:  
            batch = Batch.objects.create(
                name=name,
                course_id=course_id,
                start_date=start_date,
                duration=duration,
                is_archived=False
            )

        BatchSubject.objects.filter(batch=batch).delete()
        for subject_id, teacher_id in assignments.items():
            if teacher_id:
                BatchSubject.objects.create(
                    batch=batch,
                    subject_id=int(subject_id),
                    teacher_id=int(teacher_id)
                )

        subject_teacher_map = {
            int(subject_id): int(teacher_id) if teacher_id else None
            for subject_id, teacher_id in assignments.items()
        }

        return JsonResponse({
            "status": "success",
            "subject_teacher_map": subject_teacher_map
        })

    
    batches_qs = Batch.objects.filter(is_archived=False).prefetch_related(
        'batch_subjects__subject', 'batch_subjects__teacher'
    ).select_related('course').order_by('id')

    
    course_filter = request.GET.get('course')
    subject_filter = request.GET.get('subject')
    teacher_filter = request.GET.get('teacher')

    if course_filter:
        batches_qs = batches_qs.filter(course_id=course_filter)
    if subject_filter:
        batches_qs = batches_qs.filter(batch_subjects__subject_id=subject_filter)
    if teacher_filter:
        batches_qs = batches_qs.filter(batch_subjects__teacher_id=teacher_filter)

    batches_qs = batches_qs.distinct()  

    
    page_number = request.GET.get('page', 1)
    paginator = Paginator(batches_qs, 5)
    page_obj = paginator.get_page(page_number)

    courses = Course.objects.filter(is_archived=False)
    subjects = Subject.objects.filter(is_archived=False)
    teachers = Teacher.objects.filter(is_archived=False)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(
            request,
            "batches/batch_table.html",
            {'batches': page_obj, 'page_obj': page_obj}
        )

    return render(
        request,
        "batches/batch.html",
        {
            "batches": page_obj,
            "page_obj": page_obj,
            "courses": courses,
            "subjects": subjects,
            "teachers": teachers
        }
    )
    
    

def get_subjects(request):
    course_id = request.GET.get('course_id')
    subjects_data = []
    if course_id:
        course = Course.objects.filter(id=course_id, is_archived=False).first()
        if course:
            subjects = course.subjects.filter(is_archived=False)
            subjects_data = list(subjects.values('id', 'name'))
    return JsonResponse({'subjects': subjects_data})


def get_teachers(request):
    subject_ids = request.GET.getlist('subject_ids[]')
    teachers_data = []
    if subject_ids:
        teachers = Teacher.objects.filter(subjects__id__in=subject_ids, is_archived=False).distinct()
        teachers_data = list(teachers.values('id', 'name'))
    return JsonResponse({'teachers': teachers_data})


@require_GET
def e_get_subject_teacher(request):
    
    course_id = request.GET.get('course_id')
    if not course_id:
        return JsonResponse({'error': 'course_id is required'}, status=400)

    course = Course.objects.filter(id=course_id, is_archived=False).first()
    if not course:
        return JsonResponse({'error': 'Course not found'}, status=404)

    subjects = course.subjects.filter(is_archived=False)
    subjects_data = []

    for sub in subjects:
        teachers = sub.teacher_set.filter(is_archived=False)
        subjects_data.append({
            'id': sub.id,
            'name': sub.name,
            'teachers': [{'id': t.id, 'name': t.name} for t in teachers]
        })

    return JsonResponse({'course': course.name, 'subjects': subjects_data})


def batch_students(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id, is_archived=False)
    students = Student.objects.filter(batch=batch, is_archived=False).order_by('id')
    
    return render(request, "batches/batch_students.html", {
        "batch": batch,
        "students": students
    })


def student_result(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    subjects = student.batch.subjects.all()

    if request.method == "POST":
        for sub in subjects:
            marks = request.POST.get(f"marks_{sub.id}")
            if marks:
                marks = int(marks)
                marks = min(max(marks, 0), 100)  
                result, created = StudentResult.objects.update_or_create(
                    student=student, subject=sub,
                    defaults={'marks': marks}
                )
        return redirect(
            'batch_students', 
            batch_id=student.batch.id
            )

    
    existing_results = {r.subject_id: r.marks for r in student.results.all()}
    return render(request, 'students/student_result.html', {
        'student': student,
        'subjects': subjects,
        'existing_results': existing_results
    })


def student_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    results = student.results.select_related('subject')
    total_marks = sum(r.marks for r in results)
    average = total_marks / results.count() if results.exists() else 0

    return render(request, 'students/student_view.html', {
        'student': student,
        'results': results,
        'total_marks': total_marks,
        'average': average,
    })


    
    
    