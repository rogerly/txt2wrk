from django.db import models
from django.dispatch import receiver

from applicant.models import ApplicantProfile, ApplicantJob
from applicant.signals import job_applied
from job.models import Job
from job.signals import job_created

class JobRecommendation(models.Model):

    NEW_REC_NOT_SENT = 0
    NEW_REC_SENT = 1
    KEPT_NEW_REC = 2
    SAVED_REC = 3
    APPLIED_REC = 4
    DELETED_REC = 5
    INVALID_REC = 6
    
    RECOMMENDATION_STATE_TEXT = {
                                 NEW_REC_NOT_SENT: 'New recommendation/No text sent',
                                 NEW_REC_SENT: 'New recommendation',
                                 KEPT_NEW_REC: 'Kept as new recommendation',
                                 SAVED_REC: 'Saved recommendation',
                                 APPLIED_REC: 'Applied recommendation',
                                 DELETED_REC: 'Deleted recommendation',
                                 INVALID_REC: 'Invalid (closed?) recommendation'
                                 }

    job = models.ForeignKey(Job,
                            related_name='recommendations')
    
    applicant = models.ForeignKey(ApplicantProfile,
                                  related_name='recommendations')
    
    state = models.IntegerField('Recommendation state',
                                default = NEW_REC_NOT_SENT,
                                choices = (
                                           (NEW_REC_NOT_SENT, RECOMMENDATION_STATE_TEXT[NEW_REC_NOT_SENT]),
                                           (NEW_REC_SENT, RECOMMENDATION_STATE_TEXT[NEW_REC_SENT]),
                                           (KEPT_NEW_REC, RECOMMENDATION_STATE_TEXT[KEPT_NEW_REC]),
                                           (SAVED_REC, RECOMMENDATION_STATE_TEXT[SAVED_REC]),
                                           (APPLIED_REC, RECOMMENDATION_STATE_TEXT[APPLIED_REC]),
                                           (DELETED_REC, RECOMMENDATION_STATE_TEXT[DELETED_REC]),
                                           (INVALID_REC, RECOMMENDATION_STATE_TEXT[INVALID_REC]),
                                           )
                                )
    
    recommendation_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s - %s' % (self.job.title, self.applicant.mobile_number,)

    # Update job recommendation state upon job application
    # Once applied, user should not hear the job in the phone tree or
    # via SMS
    @staticmethod
    @receiver(job_applied, sender=ApplicantJob)
    def update_applied_state(sender, **kwargs):
        applicant = kwargs['applicant']
        job = kwargs['job']
        if applicant is not None and job is not None:
            try:
                recommendation = JobRecommendation.objects.get(job=job, applicant=applicant)
                recommendation.state = JobRecommendation.APPLIED_REC
                recommendation.save()
            except JobRecommendation.DoesNotExist:
                pass

    @staticmethod
    @receiver(job_created, sender=Job)
    def create_recommendation(sender, **kwargs):
        job = kwargs['job']
        if job.employer.demo:
            applicants = ApplicantProfile.objects.all().filter(user__email__iexact=job.employer.user.email, demo=True)
            for applicant in applicants:
                recommendation = JobRecommendation(applicant=applicant, job=job, state=JobRecommendation.NEW_REC_NOT_SENT)
                recommendation.save()

