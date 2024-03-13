from account import roles

sample_form_back_track_status_choices = (
        ('pending', 'pending'),#initial
        ('processing', 'processing'), #smu-assign-supervisor (smu:pending-not_assign,display:processing)
        ('not_assigned', 'not_assigned'),#supervisor-assign-analyst (supervisor:not_assign-processing,display:processing)
        ('not_verified', 'not_verified'),#analyst-to-supervisor(supervisor:processing-not_verified,display:not_verified)
        ('not_approved','not_approved'),
        ('verified', 'verified'),
        ('completed', 'completed'),#supervisor-assign-verifier (supervisor:not_verified-verified,display:processing) action:recheck,reject
        ('recheck', 'recheck'),
        ('rejected', 'rejected'),
        ('Test Completed','Test Completed'),
        ('parameter_recheck', 'Parameter Recheck'),
        ('back', 'back'),
        ('submit_back', 'Submit Back'),
    )

role_track_mapping = {
    f'{roles.SMU}-{roles.VERIFIER}':[roles.VERIFIER,'not_verified',True], 
    f'{roles.SMU}-{roles.SUPERVISOR}':[roles.SUPERVISOR,'processing',True],

    f'{roles.VERIFIER}-{roles.ADMIN}':[roles.ADMIN,'not_approved',True],

    f'{roles.SUPERVISOR}-{roles.VERIFIER}':[roles.VERIFIER,'not_verified',True],
}

back_to_status = {
    roles.SMU:['processing','smu_back'],
    roles.SUPERVISOR:['processing','supervisor_back'],
    roles.VERIFIER:['not_verified','verifier_back']
}