from .models import RetailEmployee, OfficeEmployee, StoreEmployee, StorePositionsChoises, RetailPositionsChoises





def get_user_district(curent_user):
    employee_retail = RetailEmployee.objects.filter(user=curent_user).first()
    if employee_retail is not None and employee_retail.district is not None:
        return employee_retail.district
    elif employee_retail is not None and employee_retail.region is not None:
        return employee_retail.region
    employee_store = StoreEmployee.objects.filter(user=curent_user).first()
    if employee_store is not None:
        return employee_store.store.district
    employee_office = OfficeEmployee.objects.filter(user=curent_user).first()
    if employee_office is not None:
        return employee_office.departament
    
def get_user_store(curent_user):
    employee_store = StoreEmployee.objects.filter(user=curent_user).first()
    if employee_store is not None:
        return employee_store.store
    
def get_user_location(current_user):
    location = get_user_store(current_user)
    if location is None:
        location = get_user_district(current_user)
    return location

def get_user_employee(user):
    if (store_employee := StoreEmployee.objects.filter(user=user).first()) is not None:
        return store_employee
    if (retail_employee := RetailEmployee.objects.filter(user=user).first()) is not None:
        return retail_employee
    if (office_employee := OfficeEmployee.objects.filter(user=user).first()) is not None:
        return office_employee

def get_districts_employee_as_user():
    ...

def get_all_employee_as_user():
    ...

def get_regions_employee_as_user():
    ...


def get_management_positions():
    return [
        StorePositionsChoises.STORE_MANAGER, StorePositionsChoises.DEPUTY_STORE_MANAGER,
        RetailPositionsChoises.DISTRICT_MANAGER, RetailPositionsChoises.REGION_MENAGER
        ]