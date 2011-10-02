from django.core.management.base import BaseCommand
from applicant.models import ApplicantProfile
from job_recommendation.models import JobRecommendation
from job.models import Job
from sms.models import SMS

class Command(BaseCommand):
    help = 'Sends new job notifications to job seekers'

    def handle(self, *args, **kwargs):
        try:
            applicants = ApplicantProfile.objects.all().filter(confirmed_phone=True)
            print applicants
            for applicant in applicants:
                print applicant
                potential_jobs = self.get_potential_jobs(applicant)
                self.send_notifications(potential_jobs, applicant)
        except Exception, e:
            print e

    def get_potential_jobs(self, applicant):
        jobs = Job.objects.all().filter(experience__lte=applicant.experience).filter(education__lte=applicant.education)
        return jobs

    def send_notifications(self, jobs, applicant):
        for job in jobs:
            print applicant.get_experience_display(), ' >= ', job.get_experience_display()
            print applicant.get_education_display(), ' >= ', job.get_education_display()

            try:
                jr = JobRecommendation.objects.get(job=job, applicant=applicant)
                print 'found existing recommendation'
            except JobRecommendation.DoesNotExist:
                jr = JobRecommendation(job=job, applicant=applicant)
                print jr
#                jr.save()
