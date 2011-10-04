# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ApplicantProfile'
        db.create_table('applicant_applicantprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='applicantprofile', unique=True, to=orm['auth.User'])),
            ('availability', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
            ('experience', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
            ('education', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
            ('employment_type', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
            ('overtime', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('confirmed_phone', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('resume', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('distance', self.gf('django.db.models.fields.IntegerField')(default=5)),
        ))
        db.send_create_signal('applicant', ['ApplicantProfile'])

        # Adding M2M table for field workday on 'ApplicantProfile'
        db.create_table('applicant_applicantprofile_workday', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('applicantprofile', models.ForeignKey(orm['applicant.applicantprofile'], null=False)),
            ('workday', models.ForeignKey(orm['job.workday'], null=False))
        ))
        db.create_unique('applicant_applicantprofile_workday', ['applicantprofile_id', 'workday_id'])

        # Adding M2M table for field industry on 'ApplicantProfile'
        db.create_table('applicant_applicantprofile_industry', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('applicantprofile', models.ForeignKey(orm['applicant.applicantprofile'], null=False)),
            ('industry', models.ForeignKey(orm['job.industry'], null=False))
        ))
        db.create_unique('applicant_applicantprofile_industry', ['applicantprofile_id', 'industry_id'])

        # Adding model 'ApplicantJob'
        db.create_table('applicant_applicantjob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_submitted', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 10, 3, 16, 17, 26, 160704))),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(related_name='applicant_job', to=orm['job.Job'])),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['applicant.ApplicantProfile'])),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('send_email', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('applicant', ['ApplicantJob'])


    def backwards(self, orm):
        
        # Deleting model 'ApplicantProfile'
        db.delete_table('applicant_applicantprofile')

        # Removing M2M table for field workday on 'ApplicantProfile'
        db.delete_table('applicant_applicantprofile_workday')

        # Removing M2M table for field industry on 'ApplicantProfile'
        db.delete_table('applicant_applicantprofile_industry')

        # Deleting model 'ApplicantJob'
        db.delete_table('applicant_applicantjob')


    models = {
        'applicant.applicantjob': {
            'Meta': {'object_name': 'ApplicantJob'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['applicant.ApplicantProfile']"}),
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 10, 3, 16, 17, 26, 160704)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applicant_job'", 'to': "orm['job.Job']"}),
            'send_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'applicant.applicantprofile': {
            'Meta': {'object_name': 'ApplicantProfile'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'availability': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'confirmed_phone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'distance': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'education': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'employment_type': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'experience': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['job.Industry']", 'symmetrical': 'False'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'overtime': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'applicantprofile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'workday': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['job.Workday']", 'symmetrical': 'False'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
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
            'availability': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'education': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobs'", 'to': "orm['employer.EmployerProfile']"}),
            'employment_type': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'experience': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['job.Industry']", 'symmetrical': 'False'}),
            'job_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '8', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'overtime': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'workday': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['job.Workday']", 'symmetrical': 'False'})
        },
        'job.workday': {
            'Meta': {'object_name': 'Workday'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['applicant']
