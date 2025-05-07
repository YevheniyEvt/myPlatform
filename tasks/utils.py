from typing import List, Union, Tuple

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from employee.utils import get_user_location
from employee.models import (
    RetailPositions, StorePositions,
    Store, District, Region,
    OficeDepartmens, StoreEmployee, RetailEmployee,
    )



def employee_tasks_allowed_locations(current_user: User)->Union[
                                    Tuple[List[StoreEmployee], str] | Tuple[List[Store], str] | Tuple[List[District], str] | None
                                    ]:
    """Get instance User. Return list of recipietns and type recipient for task"""
    location = get_user_location(current_user)
    if isinstance(location, Store):
        return StoreEmployee.objects.filter(store=location), 'users'
    if isinstance(location, District):
        return Store.objects.filter(district=location), 'stores'
    if isinstance(location, Region):
        return District.objects.filter(region=location), 'districts'
    if isinstance(location, OficeDepartmens):
        return District.objects.all(), 'districts'
    


def  get_users_from_location(recipients_id: List[int],
                             recipients: Union[StoreEmployee| Store | District | Region])->Union[List[User], None]:
    """Get list of employees id and instance of location
    return list of instance Users from that location
    """
    if isinstance(recipients, StoreEmployee):
        users = User.objects.exclude(storeemployee=None).filter(storeemployee__id__in=recipients_id)
        return users

    elif isinstance(recipients, Store):
        users = User.objects.exclude(storeemployee=None).filter(storeemployee__store__id__in=recipients_id)
        return users
    
    elif isinstance(recipients, District):
        stores = Store.objects.filter(district__id__in=recipients_id)
        users = User.objects.exclude(storeemployee=None).filter(storeemployee__store__in=stores)
        return users
    
    elif isinstance(recipients, Region):
        districts = District.objects.filter(region__id__in=recipients_id)
        stores = Store.objects.filter(store__district__in=districts)
        users = User.objects.exclude(storeemployee=None).filter(storeemployee__store__in=stores)
        return users



def users_to_tasks_create(recipients_list: Union[List[str], List[int]],
                          recipients_type: Union[StoreEmployee| Store | District | Region])->List[User]:
    """Get list of users id or list with position(position always one, len(List[str]) == 1)
    return list instance users who get task"""
    recipient = recipients_list[0]

    try:
        position = StorePositions.objects.get(position=recipient)
        return User.objects.filter(storeemployee__position=position)
    
    except StorePositions.DoesNotExist:
        try:
            position = RetailPositions.objects.get(position=recipient)
            return User.objects.filter(storeemployee__position=position)
        
        except RetailPositions.DoesNotExist:
            return get_users_from_location(recipients_id=recipients_list, recipients=recipients_type)


