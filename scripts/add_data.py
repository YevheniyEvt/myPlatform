"""Script to add data to database and dumpdata to json for test"""


from scripts.employee_script.add_data_employee import employee_run
from scripts.communication_script.add_comunication_data import communication_run
from scripts.notebook_script.add_notebook_data import notebook_run
from scripts.tasks_scripts.add_tasks_data import tasks_run

from scripts.dumptestdata import dump_data


def run():
    employee_run()
    communication_run()
    notebook_run()
    tasks_run()

    print('Create JSON...', end=' ')
    dump_data()
    print('Ok')