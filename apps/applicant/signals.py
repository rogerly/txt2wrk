from django.dispatch import Signal

# A new job has been created
job_applied = Signal(providing_args=["job", "applicant", "request"])
