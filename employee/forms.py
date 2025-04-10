from django import forms

# from .models import Employee
# from django.contrib.auth.forms import UserCreationForm
# from .models import StorePosition, OfficePosition, RetailPosition


# class UserCreate(UserCreationForm):
    
#     positions = {
#         'Store': StorePosition.store_positions,
#         'Office': OfficePosition.office_position,
#         'Retail': RetailPosition.retail_position
#           }
    
#     username = forms.CharField(label="Name")
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     position = forms.ChoiceField(choices=positions)

#     class Meta:
#         model = Employee
#         fields = ['username', 'password1', 'password2', 'position']