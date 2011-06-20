# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Job.experience'
        db.alter_column('job_job', 'experience_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Experience']))

        # Changing field 'Job.availability'
        db.alter_column('job_job', 'availability_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Availability']))

        # Changing field 'Job.location'
        db.alter_column('job_job', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Location']))

        # Changing field 'Job.education'
        db.alter_column('job_job', 'education_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Education']))


    def backwards(self, orm):
        
        # Changing field 'Job.experience'
        db.alter_column('job_job', 'experience_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Experience'], null=True))

        # Changing field 'Job.availability'
        db.alter_column('job_job', 'availability_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Availability'], null=True))

        # Changing field 'Job.location'
        db.alter_column('job_job', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Location'], null=True))

        # Changing field 'Job.education'
        db.alter_column('job_job', 'education_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Education'], null=True))


    models = {
        'job.availability': {
            'Meta': {'object_name': 'Availability'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'job.education': {
            'Meta': {'object_name': 'Education'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'job.experience': {
            'Meta': {'object_name': 'Experience'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'job.industry': {
            'Meta': {'object_name': 'Industry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'job.job': {
            'Meta': {'object_name': 'Job'},
            'availability': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['job.Availability']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'education': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['job.Education']"}),
            'experience': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['job.Experience']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['job.Industry']", 'symmetrical': 'False'}),
            'job_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '8', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['job.Location']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'workday': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['job.Workday']", 'symmetrical': 'False'})
        },
        'job.location': {
            'Meta': {'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'job.workday': {
            'Meta': {'object_name': 'Workday'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['job']
