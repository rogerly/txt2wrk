from django.db import models

from applicant.models import ApplicantProfile
from job.models import Job

class JobRecommendation(models.Model):
    
    NEW_REC = 1
    KEPT_NEW_REC = 2
    SAVED_REC = 3
    APPLIED_REC = 4
    DELETED_REC = 5
    INVALID_REC = 6
    
    RECOMMENDATION_STATE_TEXT = {
                                 NEW_REC: 'New recommendation',
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
                                default = NEW_REC,
                                choices = (
                                           (NEW_REC, RECOMMENDATION_STATE_TEXT[NEW_REC]),
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
