import json
import os

from django.core.management import call_command



def run():
    with open('about/about_data.json', 'w', encoding='utf-8') as f:
        call_command('dumpdata', 'about', indent=2, stdout=f)