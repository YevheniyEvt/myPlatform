""""
The country is divided into Region. The Region are divided into District. Each district has n number of Stores.
There are employees who work in the store - StoreEmployee
They have positions - StorePositions.
There are employees who manage the districts, regions and the country - RetailEmployee.
They have positions - RetailPositions.
There are employees who work in the office (OficeDepartmens) - OfficeEmployee.
They have positions - OfficePositions.
"""


from django.db import models
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
    """Store employee positions"""
    position = models.CharField(max_length=50, choices=StorePositionsChoises, unique=True)

    def __str__(self):
            for choise in StorePositionsChoises.choices:
                    if self.position in choise:
                            return choise[1]


class OfficePositions(models.Model):
    """Office employee positions"""
    position = models.CharField(max_length=50, choices=OfficePositionsChoises, unique=True)

    def __str__(self):
            for choise in OfficePositionsChoises.choices:
                    if self.position in choise:
                            return choise[1]
                            
                
class RetailPositions(models.Model):
    """Retail employee positions"""
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
        
