from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Course(models.Model):
    course_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject, blank=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Batch(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateField()
    duration = models.PositiveIntegerField()
    is_archived = models.BooleanField(default=False)

    subjects = models.ManyToManyField(
        Subject, through='BatchSubject', related_name='batches'
    )
    teachers = models.ManyToManyField(
        Teacher, through='BatchSubject', related_name='batches'
    )

    def __str__(self):
        return self.name



class BatchSubject(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('batch', 'subject')  

    def __str__(self):
        return f"{self.subject.name} - {self.teacher.name} ({self.batch.name})"

class Student(models.Model):
    name = models.CharField(max_length=100)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, related_name='students')
    subjects = models.ManyToManyField(Subject, blank=True)
    courses = models.ManyToManyField(Course, blank=True)
    is_archived = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.name} - {self.batch.name}"
    
class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField(default=0)  

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.marks}"



    


