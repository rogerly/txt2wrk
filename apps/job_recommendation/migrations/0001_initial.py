# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'JobRecommendation'
        db.create_table('job_recommendation_jobrecommendation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recommendations', to=orm['job.Job'])),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recomendations', to=orm['applicant.ApplicantProfile'])),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('recommendation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('job_recommendation', ['JobRecommendation'])


    def backwards(self, orm):
        
        # Deleting model 'JobRecommendation'
        db.delete_table('job_recommendation_jobrecommendation')


    models = {
        'applicant.applicantprofile': {
            'Meta': {'object_name': 'ApplicantProfile'},
            'confirmed_phone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'applicant_profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'job.job': {
            'Meta': {'object_name': 'Job'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '8', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'job_recommendation.jobrecommendation': {
            'Meta': {'object_name': 'JobRecommendation'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recomendations'", 'to': "orm['applicant.ApplicantProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recommendations'", 'to': "orm['job.Job']"}),
            'recommendation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['job_recommendation']
