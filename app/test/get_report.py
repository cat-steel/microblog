import os

def get_report():
    filepath = 'D:\\python\\work\\microblog\\microblog\\app\\templates\\report'
    reports = os.listdir(filepath)
    return reports
