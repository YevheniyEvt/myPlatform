from django.conf import settings
from django.db import models
from django.contrib import admin

from django.contrib.auth.models import User



       

class StorePositionsChoises(models.TextChoices):
    STORE_MANAGER = "SM", "Store Manager"
    STORE_MANAGER_TRAINEE = "SMT", "Store Manager Trainee"
    DEPUTY_STORE_MANAGER = "DepSm", "DeputyStoreManager"
    AREA_RESPONSIBLE = "AR", "Area Responsible"
    LOGISTIC_RESPONSIBLE = "LR", "Logistic Responsible"
    SALES_ASSISTENCE = "SA", "Sails Assistens"

class RetailPositionsChoises(models.TextChoices):
    DISTRICT_MANAGER = "DM", "District Manager"
    DISTRICT_MANAGER_TRAINEE = "DMT", "District Manager Tranee"
    REGION_MANAGER_TRANEE = "RMT", "Region Manager Trainee"
    REGION_MENAGER = "RM", "Region Manager"
    COUNTRY_MANAGER = "CM", "Country Manager"

class OfficePositionsChoises(models.TextChoices):
    STORE_BOOKKEPER = "BKS", "Bookkeper Store"
    LOGISTIC_BOOKKEPER = "BKL", "Bookkeper Logistic"
    EMPLOYEE_BOOKKEPER = "BKE", "Bookkeper Employee"
    MAIN_BOOKKEPER = "BKM", "Bookkeper Main"
    LOGISTIC_SUPPORT = "LS", "Logigstic Supporter"
    HELP_DESK = "IT", "IT Admin"
    AUDITOR = "AU", "Auditor Internal"
    FASILITY = "FA", "Facility Management"
        

class StorePositions(models.Model):
    position = models.CharField(max_length=50, choices=StorePositionsChoises, unique=True)

    def __str__(self):
            for choise in StorePositionsChoises.choices:
                    if self.position in choise:
                            return choise[1]

class OfficePositions(models.Model):
    position = models.CharField(max_length=50, choices=OfficePositionsChoises, unique=True)

    def __str__(self):
            for choise in OfficePositionsChoises.choices:
                    if self.position in choise:
                            return choise[1]
                            
                
        

class RetailPositions(models.Model):
    position = models.CharField(max_length=50, choices=RetailPositionsChoises, unique=True)

    def __str__(self):
            for choise in RetailPositionsChoises.choices:
                    if self.position in choise:
                            return choise[1]
            return self.position

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
                return self.name


class District(models.Model):
    name = models.CharField(max_length=100, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
                return self.name


class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=30, unique=True)
    city = models.CharField(max_length=50)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
                return self.short_name
    

class OficeDepartmens(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
                return self.name


                  
        
class StoreEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    position = models.ForeignKey(StorePositions, on_delete=models.SET_NULL, blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
            return self.user.get_full_name()

    @property
    def district(self):
            if self.store:
                return self.store.district.name

    @property
    def region(self):
            return self.store.region.name
       

       

class RetailEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    position = models.ForeignKey(RetailPositions, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
            return self.user.get_full_name()
       

class OfficeEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    position = models.ForeignKey(OfficePositions, on_delete=models.SET_NULL, blank=True, null=True)
    departament = models.ForeignKey(OficeDepartmens, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
            return self.user.get_full_name()
        








# class DistrictPositions(models.Model):
#         position = models.CharField(max_length=50, choices=RetailPositionsChoises, unique=True)

#         def __str__(self):
#                 return self.position

# class RegionPositions(models.Model):
#         position = models.CharField(max_length=50, choices=RetailPositionsChoises, unique=True)

#         def __str__(self):
#                 return self.position
        

        
# class EmployeePosition(models.Model):
#         store_posions = models.ForeignKey(StorePositions, on_delete=models.SET_NULL, max_length=50, blank=True, null=True)
#         office_positions = models.ForeignKey(OfficePositions, on_delete=models.SET_NULL, max_length=50, blank=True, null=True)
#         district_position = models.ForeignKey(DistrictPositions, on_delete=models.SET_NULL, max_length=50, blank=True, null=True)
#         region_positions = models.ForeignKey(RegionPositions, on_delete=models.SET_NULL, max_length=50, blank=True, null=True)
        
        
#         def __str__(self):
#             if self.store_posions:
#                    return self.store_posions.position
#             elif self.office_positions:
#                    return self.office_positions.position
#             elif self.district_position:
#                    return self.district_position.position
#             elif self.region_positions:
#                    return self.region_positions.position
        
# class EmployeePosition(models.Model):
#         name = models.ForeignKey(AllPositions, on_delete=models.CASCADE)
        

# class Emploee(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
#     position = models.OneToOneField(EmployeePosition, on_delete=models.SET_NULL, blank=True, null=True)

#     def __str__(self):
#             return self.user.username
    




"""
class StorePosition(TextChoises):

class ReatilPosition(TextChoises):

class OfficePosition(TextChoises): 

class Emploee:
    user = Username
    position = EmployeePosition
    location = Location

    def full_name:
    
    def email:

    def get_employee_location

    def get_position

    def get_store

    def get_district

    def get_region

    def get_department:
    
    def is_store_employee:
        empl = StoreEmployee.get(self.user.id)
    def is_office_employee:
    
    def is_district employee:
    
    def is_region_employee:
    
class Location:
    store = Store
    district = District
    region = Region

    

class EmployeePosition:
    all_position = Positions
    

class Positions:
    store_posions = StorePositions
    office_positions = OfficePositions
    district_position = DistrictPositions
    region_positions = RegionPositions


class StorePositions:
    position = StorePositionChoises


class OfficePositions:
    position = OfficePositionChoises


class DistrictPositions:
    position = ReatilPositionChoises


class RegionPositions:
    position = ReatilPositionChoises

    
class Store:
    name =
    short_name =
    location = 
    district = District
    

class District:
    name = 
    region = Region


class Region:
    name = 
    country =

class OficeDepartmens:
    name =
    

"""

# class UserInfo(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.user.username


# class StorePosition(models.Model):
#     store_positions = {
#         "SM": "Store Manager",
#         "SMT": "Store Manager Trainee",
#         "DepSm": "DeputyStoreManager",
#         "AR": "Area Responsible",
#         "LR": "Logistic Responsible",
#         "SA": "Sails Assistens",
#     }
    
#     position_name = models.CharField(max_length=50, choices=store_positions)
#     user_store_position = models.OneToOneField(UserInfo, null=True, on_delete=models.SET_NULL)

#     def __str__(self):
#         return self.user_store_position.user.username
    

# class RetailPosition(models.Model):
#     retail_position = {
#         "DM": "District Manager",
#         "DMT": "District Manager Tranee",
#         "RMT": "Region Manager Trainee",
#         "RM": "Region Manager",
#         "CM": "Country Manager",
#     }
    
#     position_name = models.CharField(max_length=50, choices=retail_position)
#     user_retail_position = models.OneToOneField(UserInfo, null=True, on_delete=models.SET_NULL)
#     def __str__(self):
#         return self.user_retail_position.user.username


# class OfficePosition(models.Model):
#     office_position = {
#         "BK": "Bookkeper",
#         "LS": "Logigstic Support",
#         "IT": "Sys Admin",
#         "AU": "Auditor",
#     }
    
#     position_name = models.CharField(max_length=50, choices=office_position)
#     user_office_position = models.OneToOneField(UserInfo, null=True, on_delete=models.SET_NULL)
#     def __str__(self):
#         return self.user_office_position.user.username

# class Employee(User):

#     class Meta:
#         proxy = True

#     def set_position(self, position: str):
#         userinfo = UserInfo(user=self)
#         if position in StorePosition.store_positions.keys():
#             position_todb = StorePosition(position_name=position, user_store_position=userinfo)
#         elif position in OfficePosition.office_position.keys():
#             position_todb = OfficePosition(position_name=position, user_office_position=userinfo)
#         elif position in RetailPosition.retail_position.keys():
#             position_todb = RetailPosition(position_name=position, user_retail_position=userinfo)
#         else:
#             return f"Position {position} does not exist"
#         userinfo.save()
#         position_todb.save()

#     def get_position(self):
#         if hasattr(self.userinfo, 'storeposition'):
#             return StorePosition.store_positions.get(self.userinfo.storeposition.position_name)
#         elif hasattr(self.userinfo, 'officeposition'):
#             return OfficePosition.office_position.get(self.userinfo.officeposition.position_name)
#         elif hasattr(self.userinfo, 'retailposition'):
#             return RetailPosition.retail_position.get(self.userinfo.retailposition.position_name)
#         else:
#             return 'User does not have position yet'


# class Position:
#     office_position = models.ForeignKey(OfficePosition, null=True, on_delete=models.SET_NULL)
#     retail_position = models.ForeignKey(RetailPosition, null=True, on_delete=models.SET_NULL)
#     store_position = models.ForeignKey(StorePosition, null=True, on_delete=models.SET_NULL)


# class Employee(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     position = models.OneToOneField(Position, on_delete=models.CASCADE, related_name='position')

# class Store:
#     pass


# class District:
#     pass    


# class Retail:
#     pass


# class Country:
#     pass
