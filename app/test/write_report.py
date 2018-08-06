from flask import render_template

class Write_report():
    def __init__(self,results,start_time,end_time,num,succ_num,fail_num):
        self.results = results
        self.start_time = start_time
        self.end_time = end_time
        self.num = num
        self.succ_num = succ_num
        self.fail_num = fail_num

    def run_tem(self):
        html = render_template('report_tem.html',
                               results=self.results,
                               start_time=self.start_time,
                               end_time=self.end_time,
                               num=self.num,
                               succ_num=self.succ_num,
                               fail_num=self.fail_num)
        with open('app\\report\\report_case.html','wb+') as f:
            f.write(html.encode('utf8'))