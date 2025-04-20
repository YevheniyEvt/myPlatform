
from django.contrib.auth.models import User



from employee.utils import get_user_location

from employee.models import (
    RetailPositions, StorePositions,
    Store, District, Region,
    OficeDepartmens, StoreEmployee, RetailEmployee,
    StorePositionsChoises, RetailPositionsChoises,
    )



def employee_tasks_allowed_locations(current_user):
    location = get_user_location(current_user)
    if isinstance(location, Store):
        return StoreEmployee.objects.filter(store = location), 'users'
    if isinstance(location, District):
        return Store.objects.filter(district=location), 'stores'
    if isinstance(location, Region):
        return District.objects.filter(region=location), 'districts'
    if isinstance(location, OficeDepartmens):
        return District.objects.all(), 'districts'
    


def  get_users_from_location(recipients_id, recipients):

    if isinstance(recipients, StoreEmployee):
        return [StoreEmployee.objects.get(id=user_id).user for user_id in recipients_id]
    
    elif isinstance(recipients, Store):
        employees = []
        for store_id in recipients_id:
            store=Store.objects.get(id=store_id)
            employees.extend([employee for employee in StoreEmployee.objects.filter(store=store)])
        return [employee.user for employee in employees]
    
    elif isinstance(recipients, District):
        employees = []
        for districts_id in recipients_id:
            districts=District.objects.get(id=districts_id)
            for store in districts.store_set.all():
                employees.extend([employee for employee in StoreEmployee.objects.filter(store=store)])
        return [employee.user for employee in employees]
    
    elif isinstance(recipients, Region):
        
        region = Region.objects.get(id = recipients_id[0])
        districts = region.district_set.all()
        return get_users_from_location(recipients_id=[district.id for district in districts], recipients=districts[0])
    return []



def users_to_tasks_create(recipients_list, recipients_type):

    if recipients_list[0] == StorePositionsChoises.STORE_MANAGER:
        position = StorePositions.objects.get(position=StorePositionsChoises.STORE_MANAGER)
        employees_obj = StoreEmployee.objects.filter(position=position)
        return [employee.user for employee in employees_obj]
    
    elif recipients_list[0] == StorePositionsChoises.DEPUTY_STORE_MANAGER:
        position = StorePositions.objects.get(position=StorePositionsChoises.DEPUTY_STORE_MANAGER)
        employees_obj = StoreEmployee.objects.filter(position=position)
        return [employee.user for employee in employees_obj]
    
    elif recipients_list[0] == RetailPositionsChoises.REGION_MENAGER:
        position = RetailPositions.objects.get(position=RetailPositionsChoises.REGION_MENAGER)
        employees_obj = RetailEmployee.objects.filter(position=position)
        return [employee.user for employee in employees_obj]
    
    elif recipients_list[0] == RetailPositionsChoises.DISTRICT_MANAGER:
        position = RetailPositions.objects.get(position=RetailPositionsChoises.DISTRICT_MANAGER)
        employees_obj = RetailEmployee.objects.filter(position=position)
        return [employee.user for employee in employees_obj]

    users = get_users_from_location(recipients_id=recipients_list, recipients=recipients_type)
    return users
