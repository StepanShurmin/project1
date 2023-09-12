from django.core.management import BaseCommand

from main.models import Student


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        student_list = [
            {'last_name': 'Petrov', 'first_name': 'Ivan'},
            {'last_name': 'Ivanov', 'first_name': 'Peter'},
            {'last_name': 'Semenov', 'first_name': 'Semen'},
            {'last_name': 'Sidorov', 'first_name': 'Sidor'},
        ]

        # for student_item in student_list:
        #     Student.objects.create(**student_item) # не подходит для большого количесива записей(студентов)

        students_for_create =[]
        for student_item in student_list:
            students_for_create.append(Student(**student_item))


        Student.objects.bulk_create(students_for_create)