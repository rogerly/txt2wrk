# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Availability'
        db.delete_table('job_availability')

        # Deleting model 'Education'
        db.delete_table('job_education')

        # Deleting model 'Experience'
        db.delete_table('job_experience')

        # Deleting model 'Location'
        db.delete_table('job_location')

        # Deleting field 'Job.location'
        db.delete_column('job_job', 'location_id')

        # Adding field 'Job.latitude'
        db.add_column('job_job', 'latitude', self.gf('django.db.models.fields.CharField')(max_length=5, null=True), keep_default=False)

        # Adding field 'Job.longitude'
        db.add_column('job_job', 'longitude', self.gf('django.db.models.fields.CharField')(max_length=5, null=True), keep_default=False)

        # Adding field 'Job.date_created'
        db.add_column('job_job', 'date_created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today), keep_default=False)

        # Renaming column for 'Job.experience' to match new field type.
        db.rename_column('job_job', 'experience_id', 'experience')
        # Changing field 'Job.experience'
        db.alter_column('job_job', 'experience', self.gf('django.db.models.fields.IntegerField')())

        # Removing index on 'Job', fields ['experience']
        db.delete_index('job_job', ['experience_id'])

        # Renaming column for 'Job.education' to match new field type.
        db.rename_column('job_job', 'education_id', 'education')
        # Changing field 'Job.education'
        db.alter_column('job_job', 'education', self.gf('django.db.models.fields.IntegerField')())

        # Removing index on 'Job', fields ['education']
        db.delete_index('job_job', ['education_id'])

        # Renaming column for 'Job.availability' to match new field type.
        db.rename_column('job_job', 'availability_id', 'availability')
        # Changing field 'Job.availability'
        db.alter_column('job_job', 'availability', self.gf('django.db.models.fields.IntegerField')())

        # Removing index on 'Job', fields ['availability']
        db.delete_index('job_job', ['availability_id'])


    def backwards(self, orm):
        
        # Adding index on 'Job', fields ['availability']
        db.create_index('job_job', ['availability_id'])

        # Adding index on 'Job', fields ['education']
        db.create_index('job_job', ['education_id'])

        # Adding index on 'Job', fields ['experience']
        db.create_index('job_job', ['experience_id'])

        # Adding model 'Availability'
        db.create_table('job_availability', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('job', ['Availability'])

        # Adding model 'Education'
        db.create_table('job_education', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('job', ['Education'])

        # Adding model 'Experience'
        db.create_table('job_experience', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('job', ['Experience'])

        # Adding model 'Location'
        db.create_table('job_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('job', ['Location'])

        # Adding field 'Job.location'
        db.add_column('job_job', 'location', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['job.Location']), keep_default=False)

        # Deleting field 'Job.latitude'
        db.delete_column('job_job', 'latitude')

        # Deleting field 'Job.longitude'
        db.delete_column('job_job', 'longitude')

        # Deleting field 'Job.date_created'
        db.delete_column('job_job', 'date_created')

        # Renaming column for 'Job.experience' to match new field type.
        db.rename_column('job_job', 'experience', 'experience_id')
        # Changing field 'Job.experience'
        db.alter_column('job_job', 'experience_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Experience']))

        # Renaming column for 'Job.education' to match new field type.
        db.rename_column('job_job', 'education', 'education_id')
        # Changing field 'Job.education'
        db.alter_column('job_job', 'education_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Education']))

        # Renaming column for 'Job.availability' to match new field type.
        db.rename_column('job_job', 'availability', 'availability_id')
        # Changing field 'Job.availability'
        db.alter_column('job_job', 'availability_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['job.Availability']))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
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
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'employer.employerprofile': {
            'Meta': {'object_name': 'EmployerProfile'},
            'business_address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'business_address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'business_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'business_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'business_website_url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'employerprofile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'job.industry': {
            'Meta': {'object_name': 'Industry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'job.job': {
            'Meta': {'object_name': 'Job'},
            'availability': ('django.db.models.fields.IntegerField', [], {}),
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'education': ('django.db.models.fields.IntegerField', [], {}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobs'", 'to': "orm['employer.EmployerProfile']"}),
            'experience': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['job.Industry']", 'symmetrical': 'False'}),
            'job_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '8', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'workday': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['job.Workday']", 'symmetrical': 'False'})
        },
        'job.workday': {
            'Meta': {'object_name': 'Workday'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['job']
