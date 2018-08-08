import os

def get_report():
    filepath = ('app/static/report')
    reports = os.listdir(filepath)
    return reports