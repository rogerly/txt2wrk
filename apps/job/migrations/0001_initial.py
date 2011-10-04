# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Workday'
        db.create_table('job_workday', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('job', ['Workday'])

        # Adding model 'Industry'
        db.create_table('job_industry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('job', ['Industry'])

        # Adding model 'Job'
        db.create_table('job_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('availability', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
            ('experience', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
            ('education', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
            ('employment_type', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
            ('overtime', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('job_code', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=8, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('employer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jobs', to=orm['employer.EmployerProfile'])),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('job', ['Job'])

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

        # Adding model 'JobLocation'
        db.create_table('job_joblocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('business_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('business_address1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('business_address2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('job', self.gf('django.db.models.fields.related.OneToOneField')(related_name='location', unique=True, to=orm['job.Job'])),
        ))
        db.send_create_signal('job', ['JobLocation'])


    def backwards(self, orm):
        
        # Deleting model 'Workday'
        db.delete_table('job_workday')

        # Deleting model 'Industry'
        db.delete_table('job_industry')

        # Deleting model 'Job'
        db.delete_table('job_job')

        # Removing M2M table for field workday on 'Job'
        db.delete_table('job_job_workday')

        # Removing M2M table for field industry on 'Job'
        db.delete_table('job_job_industry')

        # Deleting model 'JobLocation'
        db.delete_table('job_joblocation')


    models = {
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
        'job.joblocation': {
            'Meta': {'object_name': 'JobLocation'},
            'business_address1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'location'", 'unique': 'True', 'to': "orm['job.Job']"}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'job.workday': {
            'Meta': {'object_name': 'Workday'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['job']
