from django.db import models
from portal import departments

class Advisor(models.Model):
    # advisor_id = models.IntegerField(primary_key=True)
    advisor_first_name = models.CharField(max_length=255)
    advisor_last_name = models.CharField(max_length=255)
    advisor_email = models.EmailField(max_length=255)
    DEPARTMENT_CHOICES = departments.DEPARTMENTS
    advisor_department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        default='',
    )

    def __str__(self):
        return self.advisor_email

class Student(models.Model):
    student_first_name = models.CharField(max_length=255)
    student_last_name = models.CharField(max_length=255)
    student_email = models.EmailField(max_length=255)
    #advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    FIRST_YEAR = '1'
    SECOND_YEAR = '2'
    THIRD_YEAR = '3'
    FOURTH_YEAR = '4'
    YEAR_IN_SCHOOL_CHOICES = [
        (FIRST_YEAR, '1'),
        (SECOND_YEAR, '2'),
        (THIRD_YEAR, '3'),
        (FOURTH_YEAR, '4'),
    ]
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default='',
    )

    def __str__(self):
        return self.student_email

class Instructor(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

class Meeting(models.Model):
    days = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    facility_descr = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)

class Class(models.Model):
    crse_id = models.CharField(max_length=255)
    class_section = models.CharField(max_length=255)
    start_dt = models.CharField(max_length=255)
    end_dt = models.CharField(max_length=255)
    campus_descr = models.CharField(max_length=255)
    class_nbr = models.CharField(max_length=255)
    acad_career = models.CharField(max_length=255)
    component = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    subject_descr = models.CharField(max_length=255)
    catalog_nbr = models.CharField(max_length=255)
    acad_group = models.CharField(max_length=255)
    instruction_mode_descr = models.CharField(max_length=255)
    wait_tot = models.CharField(max_length=255)
    wait_cap = models.CharField(max_length=255)
    class_capacity = models.CharField(max_length=255)
    enrollment_total = models.CharField(max_length=255)
    enrollment_available = models.CharField(max_length=255)
    descr = models.CharField(max_length=255)
    units = models.CharField(max_length=255)
    enrl_stat_descr = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    instructors = models.ManyToManyField(Instructor)
    section_type = models.CharField(max_length=255)




