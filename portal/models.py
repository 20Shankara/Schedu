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
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE, default="5")
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
        
class Department(models.Model):
    subject = models.CharField(max_length=255)
    descr = models.CharField(max_length=255)

    def __str__(self):
        return self.descr

class Class(models.Model):
    subject = models.CharField(max_length=255)
    subject_descr = models.CharField(max_length=255)
    catalog_nbr = models.CharField(max_length=255)
    descr = models.CharField(max_length=255)

    def __str__(self):
        return self.subject + '-' + self.catalog_nbr




