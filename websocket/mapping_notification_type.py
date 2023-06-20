from . import frontend_setting
mapping = {
    "new_sample_form":{
        "model_name":"SampleForm",
        "from_user":['admin','user'],
        "to_users":['admin','user'],
        "admin_message":"A new Sample Form Arrived",
        "path":frontend_setting.sample_request,
        "user_message":"A new Sample form on the way",
    },
    "assigned_supervisor":{
        "model_name":"SampleForm",
        "from_user":['admin','smu'],
        "to_users":['supervisor'],
        "path":frontend_setting.sample_request,
        "admin_message":"A Sample Form Assigned to You",
        "user_message":"",
    },
    "assigned_analyst":{
        "model_name":"SampleFormHasParameter",
        "from_user":['supervisor'],
        "to_users":['analyst'],
        "path":frontend_setting.sample_request,
        "admin_message":"A Sample Form Assigned to You",
        "user_message":"",
    },
    "assigned_verifier":{
        "model_name":"SampleFormVerifier",
        "from_user":['supervisor'],
        "to_users":['verifier'],
        "path":frontend_setting.sample_request,
        "admin_message":"A Sample Form Assigned to You",
        "user_message":"",
    },
    "verified":{
        "model_name":"SampleFormVerifier",
        "from_user":['verifier'],
        "to_users":['user','smu','admin','supervisor','analyst'],
        "path":frontend_setting.sample_request,
        "admin_message":"this sample form verified",
        "user_message":"this sample form verified",
    }
}

