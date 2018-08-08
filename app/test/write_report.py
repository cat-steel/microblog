from flask import render_template

class Write_report():
    def __init__(self,results,start_time,file_time,end_time,num,succ_num,fail_num):
        self.results = results
        self.start_time = start_time
        self.file_time = file_time
        self.end_time = end_time
        self.num = num
        self.succ_num = succ_num
        self.fail_num = fail_num

    def run_tem(self):
        file_time = self.file_time
        results = self.results
        lenth = len(results)
        dir = 'app\\static\\report\\'
        file_name = dir+file_time+'-report.html'
        html = render_template('report_tem.html',
                               results=self.results,
                               lenth=lenth,
                               start_time=self.start_time,
                               file_time=self.file_time,
                               end_time=self.end_time,
                               num=self.num,
                               succ_num=self.succ_num,
                               fail_num=self.fail_num)
        with open(file_name,'wb+') as f:
            f.write(html.encode('utf8'))