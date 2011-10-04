# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PotentialUsers'
        db.create_table('prelaunch_potentialusers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('prelaunch', ['PotentialUsers'])


    def backwards(self, orm):
        
        # Deleting model 'PotentialUsers'
        db.delete_table('prelaunch_potentialusers')


    models = {
        'prelaunch.potentialusers': {
            'Meta': {'object_name': 'PotentialUsers'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['prelaunch']
