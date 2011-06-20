from django.db import models

from applicant.models import ApplicantProfile
from job.models import Job

NEW_REC = 1
SAVED_REC = 2
APPLIED_REC = 3
DELETED_REC = 4
INVALID_REC = 5

RECOMMENDATION_STATE_TEXT = {
                             NEW_REC: 'New recommendation',
                             SAVED_REC: 'Saved recommendation',
                             APPLIED_REC: 'Applied recommendation',
                             DELETED_REC: 'Deleted recommendation',
                             INVALID_REC: 'Invalid (closed?) recommendation'
                             }

class JobRecommendation(models.Model):
    
    job = models.ForeignKey(Job,
                            related_name='recommendations')
    
    applicant = models.ForeignKey(ApplicantProfile,
                                  related_name='recommendations')
    
    state = models.IntegerField('Recommendation state',
                                default = NEW_REC,
                                choices = (
                                           (NEW_REC, RECOMMENDATION_STATE_TEXT[NEW_REC]),
                                           (SAVED_REC, RECOMMENDATION_STATE_TEXT[SAVED_REC]),
                                           (APPLIED_REC, RECOMMENDATION_STATE_TEXT[APPLIED_REC]),
                                           (DELETED_REC, RECOMMENDATION_STATE_TEXT[DELETED_REC]),
                                           (INVALID_REC, RECOMMENDATION_STATE_TEXT[INVALID_REC]),
                                           )
                                )
    
    recommendation_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s - %s' % (self.job.title, self.applicant.mobile_number,)
