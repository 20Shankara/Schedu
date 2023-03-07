from django.db import models
from portal import departments


class Student(models.Model):
    student_first_name = models.CharField(max_length=255)
    student_last_name = models.CharField(max_length=255)
    student_email = models.EmailField(max_length=255)
    FIRST_YEAR = '1Y'
    SECOND_YEAR = '2Y'
    THIRD_YEAR = '3Y'
    FOURTH_YEAR = '4Y'
    YEAR_IN_SCHOOL_CHOICES = [
        (FIRST_YEAR, 'FIRST YEAR'),
        (SECOND_YEAR, 'SECOND YEAR'),
        (THIRD_YEAR, 'THIRD YEAR'),
        (FOURTH_YEAR, 'FOURTH YEAR'),
    ]
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default='',
    )

    def __str__(self):
        return self.student_email


class Advisor(models.Model):
    advisor_first_name = models.CharField(max_length=255)
    advisor_last_name = models.CharField(max_length=255)
    advisor_email = models.EmailField(max_length=255)
    DEPARTMENT_CHOICES = departments.DEPARTMENTS
    advisor_department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        default=departments.AAS,
    )
