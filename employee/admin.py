from django.contrib import admin
from django.contrib.auth.models import User

from .models import (StoreEmployee, OfficeEmployee, RetailEmployee,
                     Store, District, Region, OficeDepartmens,
                     )



@admin.register(StoreEmployee)
class StoreEmployeeAdmin(admin.ModelAdmin):
    list_display  = ["full_name", "position"]
    fields = ["user", "position", "store"]

    def full_name(self, obj):
        return obj.user.get_full_name()


@admin.register(OfficeEmployee)
class OfficeEmployeeAdmin(admin.ModelAdmin):
    list_display  = ["full_name", "position"]
    fields = ["user", "position", "departament"]

    def full_name(self, obj):
        return obj.user.get_full_name()


@admin.register(RetailEmployee)
class RetailEmployeeAdmin(admin.ModelAdmin):
    list_display  = ["full_name", "position"]
    fields = ["user", "position", "district", "region"]

    def full_name(self, obj):
        return obj.user.get_full_name()




admin.site.register(Store)
admin.site.register(District)
admin.site.register(Region)
admin.site.register(OficeDepartmens)








# from .models import Employee, OfficePosition, StorePosition, RetailPosition, UserInfo
# # Register your models here.
# admin.site.register(Employee)
# admin.site.register(OfficePosition)
# admin.site.register(StorePosition)
# admin.site.register(RetailPosition)
# admin.site.register(UserInfo)

# from .models import Emploee, EmployeePosition, RegionPositions, DistrictPositions, OfficePositions, StorePositions, StorePositionsChoises

# from .models import Emploee, AllPositions

# @admin.register(RegionPositions)
# class RegionPositionsAdmin(admin.ModelAdmin):
#     fields = ["position"]

# @admin.register(DistrictPositions)
# class DistrictPositionsAdmin(admin.ModelAdmin):
#     fields = ["position"]

# @admin.register(OfficePositions)
# class OfficePositionsAdmin(admin.ModelAdmin):
#     fields = ["position"]

# @admin.register(StorePositions)
# class StorePositionsAdmin(admin.ModelAdmin):
#     fields = ["position"]


# class EmployeeAdminInline(admin.StackedInline):
#     model = Emploee
#     fields = ["user"]
#     readonly_fields = ["position"]
#     extra = 0

# @admin.register(EmployeePosition)
# class EmployeePositionAdmin(admin.ModelAdmin):
#     inlines = [EmployeeAdminInline]
#     fields = ["store_posions", "office_positions", "district_position", "region_positions"]



# @admin.register(Emploee)
# class EmployeeAdmin(admin.ModelAdmin):
#     list_display  = ["full_name", "position"]
#     fields = ["user", "position"]
#     readonly_fields = ["position"]
#     # readonly_fields = ["position"]

#     def full_name(self, obj):
#         return obj.user.get_full_name()

    

