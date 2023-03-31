from django.core.management.base import BaseCommand, CommandError
import requests
from ...models import *

class Command(BaseCommand):

    def updateDepartments(self):
        r = requests.get(
            'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1232')
        if r.json() != []:
            Department.objects.all().delete()
            for key, value in r.json().items():
                if key == 'subjects':
                    for v in value:
                        descr = v['descr']
                        subject = v['subject']
                        new_department = Department(subject=subject, descr=descr)
                        new_department.save()

    def addClasses(self, url):
        page = 1
        baseurl = url
        url += str(page)
        r = requests.get(
            url
        )

        # Keep requesting pages until a page returns an empty json
        while r.json() != []:
            for item in r.json():
                # If the class doesn't already exist, then add the class to the database
                if not Class.objects.filter(subject=item['subject'], subject_descr=item['subject_descr'], catalog_nbr=item['catalog_nbr'], descr=item['descr']).exists():
                    c = Class(
                        subject=item['subject'],
                        subject_descr=item['subject_descr'],
                        catalog_nbr=item['catalog_nbr'],
                        descr=item['descr'],
                    )
                    c.save()
            page += 1
            r = requests.get(baseurl + str(page))

    def handle(self, *args, **kwargs):
        # Delete all preexisting rows in the database
        Class.objects.all().delete()
        Department.objects.all().delete()
        self.updateDepartments()

        # Create requests for every department that was fetched above
        for department in Department.objects.all():
            subject = department.subject
            year = '23'
            seasons = ['2', '8']

            # Find all classes for both the Fall and Spring semesters
            for season in seasons:
                term = '1' + year + season
                baseurl = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term='
                url = baseurl + term + '&subject=' + subject + '&page='
                self.addClasses(url)