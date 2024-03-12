sample_form_status_choices = (
        ('pending', 'pending'),#initial
        ('processing', 'processing'), #smu-assign-supervisor (smu:pending-not_assign,display:processing)
        ('not_assigned', 'not_assigned'),#supervisor-assign-analyst (supervisor:not_assign-processing,display:processing)
        ('not_verified', 'not_verified'),#analyst-to-supervisor(supervisor:processing-not_verified,display:not_verified)
        ('not_approved','not_approved'),
        ('verified', 'verified'),
        ('completed', 'completed'),#supervisor-assign-verifier (supervisor:not_verified-verified,display:processing) action:recheck,reject
        ('recheck', 'recheck'),
        ('rejected', 'rejected'),
    )

sample_form_form_available = (
        ('superadmin', 'superadmin'),
        ('smu','smu'),
        ('supervisor', 'supervisor'),
        ('analyst', 'analyst'),
        ('user', 'user'),
        ('verifier','verifier'),
        ('admin', 'ADMIN'),
    )

supervisor_sampleform_status = (       
        ('pending', 'pending'), 
        ('not_assigned', 'not_assigned'), 
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('recheck', 'recheck'),
        ('rejected', 'rejected'),
        ('not_verified','not_verified'),
        ('not_approved','not_approved'),
        ('Test Completed','Test Completed'),
        ('verified','verified'),
    )

sample_formhas_parameter_status = (       
        ('pending', 'pending'), 
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('recheck', 'recheck'),
        ('rejected', 'rejected'),
        ('not_verified','not_verified'),
        ('tested','tested'),
        ('verified','verified'),
    )