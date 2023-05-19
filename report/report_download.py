import json

def ReportAdminList(report_type,report_lang):
    data = {
        'report_type':report_type,
        'report_lang':report_lang
    }
    data = json.dumps(data)
    return data

def ReportUserList(report_type,report_lang):
    data = {
        'report_type':report_type,
        'report_lang':report_lang
    }
    data = json.dumps(data)
    return data

def ReportUserSampleForm(report_type,report_lang):
    data = {
        'report_type':report_type,
        'report_lang':report_lang
    }
    data = json.dumps(data)
    return data

def ReportSampleForm(report_type,report_lang):
    data = {
        'report_type':report_type,
        'report_lang':report_lang
    }
    data = json.dumps(data)
    return data

def ReportCommodity(report_type,report_lang):
    data = {
        'report_type':report_type,
        'report_lang':report_lang
    }
    data = json.dumps(data)
    return data

def ReportParameter(report_type,report_lang):
    data = {
        'report_type':report_type,
        'report_lang':report_lang
    }
    data = json.dumps(data)
    return data
