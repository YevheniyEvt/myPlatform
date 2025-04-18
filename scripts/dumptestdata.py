from django.core.management import call_command
from myPlatform.settings import BASE_DIR


def dump_data():
    with open('fixtures/test_data.json', 'w', encoding='utf-8') as f:
        call_command('dumpdata', indent=2, stdout=f)
