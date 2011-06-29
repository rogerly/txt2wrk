# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'ApplicantProfile.availability'
        db.add_column('applicant_applicantprofile', 'availability', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['job.Availability']), keep_default=False)

        # Adding field 'ApplicantProfile.location'
        db.add_column('applicant_applicantprofile', 'location', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['job.Location']), keep_default=False)

        # Adding field 'ApplicantProfile.education'
        db.add_column('applicant_applicantprofile', 'education', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['job.Education']), keep_default=False)

        # Adding field 'ApplicantProfile.experience'
        db.add_column('applicant_applicantprofile', 'experience', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['job.Experience']), keep_default=False)

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


    def backwards(self, orm):
        
        # Deleting field 'ApplicantProfile.availability'
        db.delete_column('applicant_applicantprofile', 'availability_id')

        # Deleting field 'ApplicantProfile.location'
        db.delete_column('applicant_applicantprofile', 'location_id')

        # Deleting field 'ApplicantProfile.education'
        db.delete_column('applicant_applicantprofile', 'education_id')

        # Deleting field 'ApplicantProfile.experience'
        db.delete_column('applicant_applicantprofile', 'experience_id')

        # Removing M2M table for field workday on 'ApplicantProfile'
        db.delete_table('applicant_applicantprofile_workday')

        # Removing M2M table for field industry on 'ApplicantProfile'
        db.delete_table('applicant_applicantprofile_industry')


    models = {
        'applicant.applicantprofile': {
            'Meta': {'object_name': 'ApplicantProfile'},
            'availability': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['job.Availability']"}),
            'confirmed_phone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'education': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['job.Education']"}),
            'experience': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['job.Experience']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['job.Industry']", 'symmetrical': 'False'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['job.Location']"}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'applicant_profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'workday': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['job.Workday']", 'symmetrical': 'False'})
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

    complete_apps = ['applicant']
