# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Call'
        db.create_table('call_call', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='calls', null=True, to=orm['applicant.ApplicantProfile'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('outbound', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('call_sid', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('call_type', self.gf('django.db.models.fields.IntegerField')(default=101)),
        ))
        db.send_create_signal('call', ['Call'])

        # Adding model 'CallFragment'
        db.create_table('call_callfragment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('call', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fragments', null=True, to=orm['call.Call'])),
            ('outbound', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('fragment_type', self.gf('django.db.models.fields.IntegerField')(default=1001)),
        ))
        db.send_create_signal('call', ['CallFragment'])


    def backwards(self, orm):
        
        # Deleting model 'Call'
        db.delete_table('call_call')

        # Deleting model 'CallFragment'
        db.delete_table('call_callfragment')


    models = {
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
        'call.call': {
            'Meta': {'object_name': 'Call'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'calls'", 'null': 'True', 'to': "orm['applicant.ApplicantProfile']"}),
            'call_sid': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'call_type': ('django.db.models.fields.IntegerField', [], {'default': '101'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outbound': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'call.callfragment': {
            'Meta': {'object_name': 'CallFragment'},
            'call': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fragments'", 'null': 'True', 'to': "orm['call.Call']"}),
            'fragment_type': ('django.db.models.fields.IntegerField', [], {'default': '1001'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outbound': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'job.industry': {
            'Meta': {'object_name': 'Industry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'job.workday': {
            'Meta': {'object_name': 'Workday'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['call']
