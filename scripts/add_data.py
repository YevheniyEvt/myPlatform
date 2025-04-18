
from scripts.communication_script.add_comunication_data import communication_run
from scripts.employee_script.add_data_employee import employee_run
from scripts.dumptestdata import dump_data


def run():
    employee_run()
    communication_run()
    dump_data()