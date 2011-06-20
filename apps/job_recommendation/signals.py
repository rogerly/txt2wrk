from django.dispatch import Signal

# A new job has been created
new_recommendation = Signal(providing_args=["job", "applicant"])
