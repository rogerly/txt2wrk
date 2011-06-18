from django.dispatch import Signal

# A new job has been created
job_created = Signal(providing_args=["job", "request"])
