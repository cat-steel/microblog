from app.models import Case, Project ,Module
from app import db
class Do_sql():
    def editor_case(self,id_num,org_name,module_name,name,server,ways,request_method,data_i,data,check,is_base):
        org_id = db.session.query(Project.id).filter_by(project_name=org_name).first()[0]
        module_id = db.session.query(Module.id).filter_by(module_name=module_name).first()[0]
        Case.query.filter_by(id=id_num).update({Case.name: name,
                                                Case.IP: server,
                                                Case.ways: ways,
                                                Case.request_method: request_method,
                                                Case.data_i: data_i,
                                                Case.data: data,
                                                Case.check: check,
                                                Case.is_base: is_base,
                                                Case.org_id: org_id,
                                                Case.module_id: module_id,
                                                Case.is_succ: 0})
        db.session.commit()

    def value(self,id_num,arg):
        values = db.session.query(arg).filter_by(id=id_num).first()[0]
        return values

    def get_case(self,id_num):
        case_name = self.value(id_num,Case.name)
        server = self.value(id_num,Case.IP)
        way = self.value(id_num,Case.ways)
        request_method = self.value(id_num,Case.request_method)
        data_type = self.value(id_num,Case.data_i)
        data_i = self.value(id_num,Case.data)
        check = self.value(id_num,Case.check)
        is_base = self.value(id_num,Case.is_base)
        org_id = self.value(id_num,Case.org_id)
        org_name = self.value(org_id,Project.project_name)
        module_id = self.value(id_num,Case.module_id)
        module_name = self.value(module_id,Module.module_name)
        is_succ = self.value(id_num,Case.is_succ)
        sql_case = {
            'case_name':case_name,
            'server':server,
            'way':way,
            'request_method':request_method,
            'data_type':data_type,
            'data_i':data_i,
            'check':check,
            'is_base':is_base,
            'org_name':org_name,
            'module_name':module_name,
            'is_succ':is_succ
        }
        return sql_case