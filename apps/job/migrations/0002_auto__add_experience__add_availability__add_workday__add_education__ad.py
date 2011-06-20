# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Experience'
        db.create_table('job_experience', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('job', ['Experience'])

        # Adding model 'Availability'
        db.create_table('job_availability', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('job', ['Availability'])

        # Adding model 'Workday'
        db.create_table('job_workday', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('job', ['Workday'])

        # Adding model 'Education'
        db.create_table('job_education', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('job', ['Education'])

        # Adding model 'Industry'
        db.create_table('job_industry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('job', ['Industry'])

        # Adding model 'Location'
        db.create_table('job_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('job', ['Location'])

        # Adding field 'Job.availability'
        db.add_column('job_job', 'availability', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Availability'], null=True), keep_default=False)

        # Adding field 'Job.location'
        db.add_column('job_job', 'location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Location'], null=True), keep_default=False)

        # Adding field 'Job.education'
        db.add_column('job_job', 'education', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Education'], null=True), keep_default=False)

        # Adding field 'Job.experience'
        db.add_column('job_job', 'experience', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Experience'], null=True), keep_default=False)

        # Adding M2M table for field workday on 'Job'
        db.create_table('job_job_workday', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('job', models.ForeignKey(orm['job.job'], null=False)),
            ('workday', models.ForeignKey(orm['job.workday'], null=False))
        ))
        db.create_unique('job_job_workday', ['job_id', 'workday_id'])

        # Adding M2M table for field industry on 'Job'
        db.create_table('job_job_industry', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('job', models.ForeignKey(orm['job.job'], null=False)),
            ('industry', models.ForeignKey(orm['job.industry'], null=False))
        ))
        db.create_unique('job_job_industry', ['job_id', 'industry_id'])


    def backwards(self, orm):
        
        # Deleting model 'Experience'
        db.delete_table('job_experience')

        # Deleting model 'Availability'
        db.delete_table('job_availability')

        # Deleting model 'Workday'
        db.delete_table('job_workday')

        # Deleting model 'Education'
        db.delete_table('job_education')

        # Deleting model 'Industry'
        db.delete_table('job_industry')

        # Deleting model 'Location'
        db.delete_table('job_location')

        # Deleting field 'Job.availability'
        db.delete_column('job_job', 'availability_id')

        # Deleting field 'Job.location'
        db.delete_column('job_job', 'location_id')

        # Deleting field 'Job.education'
        db.delete_column('job_job', 'education_id')

        # Deleting field 'Job.experience'
        db.delete_column('job_job', 'experience_id')

        # Removing M2M table for field workday on 'Job'
        db.delete_table('job_job_workday')

        # Removing M2M table for field industry on 'Job'
        db.delete_table('job_job_industry')


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
            'availability': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['job.Availability']", 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'education': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['job.Education']", 'null': 'True'}),
            'experience': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['job.Experience']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['job.Industry']", 'symmetrical': 'False'}),
            'job_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '8', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['job.Location']", 'null': 'True'}),
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
