from django.db import models
from django.contrib.postgres.fields import ArrayField
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
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE, blank=True, null=True, default='')
    shopping_cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE, blank=True, null=True, default='')
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


class ClassSection(models.Model):
    class_nbr = models.CharField(max_length=255)
    class_section = models.CharField(max_length=255)
    class_capacity = models.CharField(max_length=255)
    enrollment_total = models.CharField(max_length=255)
    enrollment_available = models.CharField(max_length=255)
    units = models.CharField(max_length=255)
    days = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)
    facility_descr = models.CharField(max_length=255)
    catalog_nbr = models.CharField(max_length=255, default='')
    season = models.CharField(max_length=255)
    # new fields
    subject = models.CharField(max_length=255, null=True)
    subject_descr = models.CharField(max_length=255, null=True)
    descr = models.CharField(max_length=255, null=True)
    section_type = models.CharField(max_length=255, null=True)


class Schedule(models.Model):
    season = models.CharField(max_length=255)
    classes = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        null=True,
    )
    def credit_count(self):
        creditCount = 0
        for c in self.classes:
            curClass = ClassSection.objects.get(pk=c)
            creditCount += int(curClass.units[0])
        return creditCount


class ShoppingCart(models.Model):
    season = models.CharField(max_length=255)
    classes = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        null=True,
    )