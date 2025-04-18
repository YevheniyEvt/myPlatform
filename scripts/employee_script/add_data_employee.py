"""Add data to fill database"""

import random
from collections import deque
from django.contrib.auth.models import User

from scripts.employee_script import data

from employee import models as employee_models


COUNT_RETAIL_EMPLOYEES = 15
COUNT_OFFICE_EMPLOYEES = 10
COUNT_STORE_EMPLOYEES = 60
COUNT_USERS = COUNT_RETAIL_EMPLOYEES + COUNT_OFFICE_EMPLOYEES + COUNT_STORE_EMPLOYEES
COUNT_STORES = COUNT_STORE_EMPLOYEES / 5
ID_RETAIL_EMPLOYEES = range(1, COUNT_RETAIL_EMPLOYEES + 1)
ID_OFFICE_EMPLOYEES = range(COUNT_RETAIL_EMPLOYEES + 1, COUNT_RETAIL_EMPLOYEES + COUNT_OFFICE_EMPLOYEES + 1)
ID_STORE_EMPLOYEES = range(COUNT_OFFICE_EMPLOYEES + COUNT_RETAIL_EMPLOYEES + 1, COUNT_OFFICE_EMPLOYEES + COUNT_RETAIL_EMPLOYEES + COUNT_STORE_EMPLOYEES + 1)

SLICE_RETAIL_EMPLOYEES = (0, COUNT_RETAIL_EMPLOYEES)
SLICE_OFFICE_EMPLOYEES = (COUNT_RETAIL_EMPLOYEES, COUNT_RETAIL_EMPLOYEES + COUNT_OFFICE_EMPLOYEES)
SLICE_STORE_EMPLOYEES = (COUNT_OFFICE_EMPLOYEES + COUNT_RETAIL_EMPLOYEES , COUNT_OFFICE_EMPLOYEES + COUNT_RETAIL_EMPLOYEES + COUNT_STORE_EMPLOYEES)


def add_employee_positions():
    for store_pos in employee_models.StorePositionsChoises.values:
        employee_models.StorePositions.objects.create(position=store_pos)
    
    for retail_pos in employee_models.RetailPositionsChoises.values:
        employee_models.RetailPositions.objects.create(position=retail_pos)

    for office_pos in employee_models.OfficePositionsChoises.values:
        employee_models.OfficePositions.objects.create(position=office_pos)


def add_regions():
    for region in data.REGIONS:
        employee_models.Region.objects.create(name=region)


def add_districts():
    for district in data.DISTRICTS:
        employee_models.District.objects.create(
            name=district.get('name'),
            region=employee_models.Region.objects.get(name=district.get('region'))
            )


def add_office_departments():
    for office_dep in employee_models.OfficePositionsChoises.labels:
        employee_models.OficeDepartmens.objects.get_or_create(name=office_dep.split()[0])


def add_stores():
    for store_data in data.create_store_data(count=COUNT_STORES):
        employee_models.Store.objects.create(
            name=store_data.get('name'),
            short_name=store_data.get('short_name'),
            city=store_data.get('city'),
            district=employee_models.District.objects.get(name=store_data['district'].get('name'))
        )

def add_superuser():
    User.objects.create_superuser(
        username='admin',
        email='Genya421@gmail.com',
        password=str(1234),
        first_name='Super',
        last_name='User',
    )

def add_users(count=COUNT_USERS):
    for user_data in data.create_user_data(count=count - 1):
        User.objects.create(
            username=user_data.get('username'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            password=user_data.get('password'),
            email='Genya4211@gmail.com'
        )


def add_office_employee():
    departaments = {}
    for office_position in employee_models.OfficePositionsChoises.choices:
        departaments[office_position[0]] = office_position[1].split()[0]

    users = User.objects.all()[SLICE_OFFICE_EMPLOYEES[0]:SLICE_OFFICE_EMPLOYEES[1]]
    all_positions = deque(employee_models.OfficePositions.objects.all())
    for user in users:
        user_db = user
        office_position_db = all_positions[0]
        departament = departaments.get(office_position_db.position)
        departament_db = employee_models.OficeDepartmens.objects.get(name=departament)

        employee_models.OfficeEmployee.objects.create(
            user=user_db,
            position=office_position_db,
            departament=departament_db,
        )
        all_positions.reverse()

def add_retail_employee():
    all_positions = deque(employee_models.RetailPositions.objects.all())
    all_district = deque(employee_models.District.objects.all())
    users = User.objects.all()[SLICE_RETAIL_EMPLOYEES[0]:SLICE_RETAIL_EMPLOYEES[1]]
    for user in users:
        user_db = user
        position_db = all_positions[0]
        district_db = all_district[0]
        region_db = district_db.region

        employee_models.RetailEmployee.objects.create(
            user=user_db,
            position=position_db,
            district=district_db,
            region=region_db,
        )
        all_positions.reverse()
        all_district.reverse()

def add_store_employee():
    all_positions = list(employee_models.StorePositions.objects.all())
    all_stores = list(employee_models.Store.objects.all())
    users = User.objects.all()[SLICE_STORE_EMPLOYEES[0]:SLICE_STORE_EMPLOYEES[1]]
    for user in users:
        user_db = user
        if not all_positions:
            all_positions = list(employee_models.StorePositions.objects.all())
            all_stores.pop()
        position_db = all_positions.pop()
        store_db = all_stores[-1]

        employee_models.StoreEmployee.objects.create(
            user=user_db,
            position=position_db,
            store=store_db,
        )

def database_is_empty():
    return not User.objects.all()


def employee_run():
    if database_is_empty():
        print('Start create employee data...', end=' ')
        add_employee_positions()
        add_regions()
        add_districts()
        add_office_departments()
        add_stores()
        add_superuser()
        add_users()
        add_office_employee()
        add_retail_employee()
        add_store_employee()
        print('Ok')
    else:
        print('Employee data - Ok')

    

