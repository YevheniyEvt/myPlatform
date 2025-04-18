import random

REGIONS = ['Region1', 'Region2']

DISTRICTS = [
{'name': 'South', 'region': 'Region1'},
{'name': 'Dnipro', 'region': 'Region2'},
{'name': 'Center', 'region': 'Region1'},
{'name': 'West', 'region': 'Region2'},
{'name': 'Volyn', 'region': 'Region1'},
{'name': 'Podil', 'region': 'Region2'},
    ]

NAMES = [
    'Alabama', 'Olivia', 'Charlotte', 'Amelia', 'Ava', 'Elizabeth', 'Alaska', 'Charlotte', 'Aurora', 'Amelia', 'Hazel', 'Emma', 'Arizona', 'Olivia', 'Emma', 'Mia', 'Isabella', 'Sophia',
 'Arkansas', 'Olivia', 'Amelia', 'Charlotte', 'Emma', 'Evelyn', 'California', 'Olivia', 'Mia', 'Camila', 'Emma', 'Isabella', 'Colorado', 'Charlotte', 'Olivia', 'Sophia', 'Emma',
 'Amelia', 'Connecticut', 'Olivia', 'Charlotte', 'Mia', 'Emma', 'Amelia', 'Delaware', 'Charlotte', 'Isabella', 'Emma', 'Olivia', 'Sophia', 'Dist.', 'of', 'Columbia', 'Charlotte',
 'Olivia', 'Naomi', 'Sophia', 'Maya', 'Florida', 'Olivia', 'Emma', 'Isabella', 'Mia', 'Sophia', 'Georgia', 'Olivia', 'Charlotte', 'Amelia', 'Emma', 'Ava', 'Hawaii', 'Isla', 'Mia',
 'Olivia', 'Luna', 'Ava', 'Idaho', 'Olivia', 'Charlotte', 'Evelyn', 'Amelia', 'Emma', 'Illinois', 'Olivia', 'Emma', 'Mia', 'Sophia', 'Charlotte', 'Indiana', 'Charlotte', 'Amelia',
 'Olivia', 'Eleanor', 'Evelyn', 'Iowa', 'Charlotte', 'Olivia', 'Amelia', 'Harper', 'Evelyn', 'Kansas', 'Amelia', 'Charlotte', 'Olivia', 'Evelyn', 'Emma', 'Kentucky', 'Amelia',
 'Charlotte', 'Emma', 'Olivia', 'Evelyn', 'Louisiana', 'Amelia', 'Olivia', 'Charlotte', 'Ava', 'Harper', 'Maine', 'Charlotte', 'Evelyn', 'Olivia', 'Eleanor', 'Harper', 'Maryland',
 'Olivia', 'Emma', 'Charlotte', 'Sophia', 'Mia', 'Massachusetts', 'Charlotte', 'Olivia', 'Emma', 'Sophia', 'Isabella', 'Michigan', 'Charlotte', 'Amelia', 'Olivia', 'Sophia', 'Emma',
 'Minnesota', 'Charlotte', 'Olivia', 'Evelyn', 'Emma', 'Amelia', 'Mississippi', 'Ava', 'Amelia', 'Olivia', 'Charlotte', 'Harper', 'Missouri', 'Charlotte', 'Olivia', 'Amelia', 'Eleanor',
 'Harper', 'Montana', 'Charlotte', 'Emma', 'Hazel', 'Olivia', 'Amelia', 'Nebraska', 'Charlotte', 'Olivia', 'Sophia', 'Amelia', 'Evelyn', 'Nevada', 'Olivia', 'Isabella', 'Mia', 'Sophia', 
 'Charlotte', 'New', 'Hampshire', 'Charlotte', 'Olivia', 'Evelyn', 'Amelia', 'Emma', 'New', 'Jersey', 'Olivia', 'Emma', 'Mia', 'Sophia', 'Isabella', 'New', 'Mexico', 'Olivia', 'Amelia', 
 'Mia', 'Isabella', 'Emma', 'New', 'York', 'Emma', 'Olivia', 'Sophia', 'Mia', 'Amelia', 'North', 'Carolina', 'Olivia', 'Amelia', 'Charlotte', 'Emma', 'Sophia', 'North', 'Dakota', 
 'Evelyn', 'Charlotte', 'Amelia', 'Harper', 'Olivia', 'Ohio', 'Charlotte', 'Amelia', 'Olivia', 'Sophia', 'Evelyn', 'Oklahoma', 'Olivia', 'Amelia', 'Emma', 'Sophia', 'Charlotte', 
 'Oregon', 'Olivia', 'Amelia', 'Evelyn', 'Charlotte', 'Emma', 'Pennsylvania', 'Charlotte', 'Olivia', 'Emma', 'Sophia', 'Amelia', 'Rhode', 'Island', 'Charlotte', 'Sophia', 'Olivia', 
 'Amelia', 'Emma', 'South', 'Carolina', 'Olivia', 'Charlotte', 'Amelia', 'Emma', 'Ava', 'South', 'Dakota', 'Ava', 'Charlotte', 'Nora', 'Amelia', 'Evelyn', 'Tennessee', 'Charlotte', 
 'Olivia', 'Amelia', 'Emma', 'Ava', 'Texas', 'Emma', 'Olivia', 'Camila', 'Mia', 'Isabella', 'Utah', 'Charlotte', 'Olivia', 'Emma', 'Evelyn', 'Lucy', 'Vermont', 'Amelia', 'Eleanor', 
 'Charlotte', 'Evelyn', 'Sophia', 'Virginia', 'Charlotte', 'Olivia', 'Emma', 'Sophia', 'Amelia', 'Washington', 'Olivia', 'Amelia', 'Emma', 'Sophia', 'Evelyn', 'West', 'Virginia', 
 'Amelia', 'Charlotte', 'Harper', 'Olivia', 'Willow', 'Wisconsin', 'Charlotte', 'Olivia', 'Evelyn', 'Amelia', 'Emma', 'Wyoming', 'Evelyn', 'Amelia', 'Olivia', 'Harper', 'Charlotte'
    ]

CITYIES = ['Kyiv', 'Kharkiv', 'Odesa', 'Dnipro', 'Donetsk', 'Lviv', 'Zaporizhzhia', 'Kryvyi', 'Rih', 'Mykolaiv']

STORES_SHORT_NAME = [
    'J022', 'J010', 'J079', 'J087', 'J061', 'J045', 'J080', 'J007', 'J003', 'J052', 'J017', 'J082', 'J066', 'J049', 'J075', 'J057', 'J001', 'J012', 'J060', 'J047', 'J053', 'J015',
    'J042', 'J056', 'J005', 'J024', 'J054', 'J014', 'J097', 'J029', 'J008', 'J032', 'J068', 'J025', 'J021', 'J074', 'J037', 'J002', 'J055', 'J039', 'J016', 'J030', 'J043', 'J072',
    'J089', 'J086', 'J088', 'J027', 'J034', 'J026', 'J044', 'J035', 'J051', 'J059', 'J063', 'J046', 'J040', 'J031', 'J071', 'J077', 'J065', 'J028', 'J058', 'J092', 'J011', 'J096',
    'J036', 'J019', 'J004', 'J091', 'J050', 'J023', 'J064', 'J048', 'J090', 'J083', 'J009', 'J093', 'J062', 'J070', 'J041', 'J033', 'J095', 'J038', 'J078', 'J013', 'J094', 'J081',
    ]

OFFICE_DEPARTMENT = ['Bookkeper', 'Logigstic', 'IT', 'Auditor', 'Facility']

def create_store_data(count=10):
    """
    Generet data for store. Count is number of stores
    Return dict with: short_name, name, city, district.
    """
    all_districts = DISTRICTS.copy()
    all_names = set(NAMES)
    all_city = CITYIES.copy()
    all_short_name = STORES_SHORT_NAME.copy()
    while count > 0:
        if not all_short_name:
            all_short_name = STORES_SHORT_NAME.copy()
        short_name = all_short_name.pop()
        if not all_city:
            all_city = CITYIES.copy()
        city = all_city.pop()
        if not all_names:
            all_names = set(NAMES)
        
        name = ' '.join([city, all_names.pop() + str(count)])
        if not all_districts:
            all_districts = DISTRICTS.copy()
        district = all_districts.pop()
        yield {'short_name': short_name, 'city': city, 'name': name, 'district': district}
        count -= 1


def create_user_data(count=10):
    """
    Generet data for user. Count is number of users
    Return dict with: username, first_name, last_name, password.
    """
    all_names = set(NAMES)
    while count > 0:
        if not all_names:
            all_names = set(NAMES)
        username = all_names.pop() + str(count)
        last_name = random.choice(NAMES)
        while last_name + str(count) == username:
            last_name = random.choice(NAMES)
        password='password123'
        yield {'username': username, 'first_name': username, 'last_name': last_name, 'password': password}
        count -= 1

