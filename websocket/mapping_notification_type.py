from . import frontend_setting
mapping = {
    "new_sample_form":{
        "model_name":"SampleForm",
        "from_user":['admin','user'],
        "to_users":['admin','user'],
        "admin_message":"A new sample <strong>{sample_name} ({namuna_code})</strong> has been requested for testing by <strong>{first_name} {last_name}</strong>",
        "path":frontend_setting.smu_sample_request_details, #sagar put full path here
        "user_path":frontend_setting.smu_sample_request_details,  #sagar put full path here
        "user_message":"Your sample ({refrence_number}) has been submitted successfully",
    },
    "assigned_supervisor":{
        "model_name":"SuperVisorSampleForm",
        "from_user":['admin','smu'],
        "to_users":['supervisor'],
        "path":frontend_setting.supervisor_sample_request_details,
        "admin_message":"A new sample <strong>{sample_name} ({namuna_code})</strong> has been assigned by <strong>{smu_first_name} {smu_last_name}</strong> for supervision.",
        "user_message":"None",
    },
    "assigned_analyst":{
        "model_name":"SampleFormHasParameter",
        "from_user":['supervisor'],
        "to_users":['analyst'],
        "path":frontend_setting.analyst_sample_request_details,
        "admin_message":"A new sample <strong>{sample_name} ({namuna_code})</strong>s has been assigned by <strong>{supervisor_first_name} {supervisor_last_name}</strong> for testing.",
        "user_message":"None",
    },
    "sent_to_supervisor":{
        "model_name":"SampleFormHasParameter",
        "from_user":['supervisor'],
        "to_users":['analyst'],
        "path":frontend_setting.supervisor_sample_assigned_details,
        "admin_message":"A test report of <strong>{sample_name} ({namuna_code})</strong> has been submitted by <strong>{analyst_first_name} {analyst_last_name}</strong>",
        "user_message":"None",
    },
    "assigned_verifier":{
        "model_name":"SampleFormVerifier",
        "from_user":['supervisor'],
        "to_users":['verifier'],
        "path":frontend_setting.verifier_sample_request_details,
        "admin_message":"A sample report of <strong>{sample_name} ({namuna_code})</strong> has been submitted by <strong>{supervisor_first_name} {supervisor_last_name}</strong> for verification.",
        "user_message":"None",
    },
    "assigned_admin":{
        "model_name":"SampleFormVerifier",
        "from_user":['verifier'],
        "to_users":['user','smu','admin','supervisor','analyst'],
        "path":frontend_setting.admin_sample_request_details,
        "admin_message":"A sample report of <strong> {sample_name} ({namuna_code}) </strong> has been submitted by {verified_by_first_name} {verified_by_last_name} for approval.",
        "user_message":"this sample form verified",
    },
    "approved_sample_form":{
        "model_name":"SampleFormVerifier",
        "from_user":['verifier'],
        "to_users":['user','smu','admin','supervisor','analyst'],#user, smu,supervisor,superadmin,verifier
        "path":frontend_setting.sample_request,
        "admin_message":"A sample report of {sample_name} ({namuna_code}) has been approved by admin",
        "user_path":frontend_setting.smu_sample_request_details,  #sagar put full path here
        "user_message":"A sample report of {sample_name} ({namuna_code}) has been approved by admin",
    }
}
