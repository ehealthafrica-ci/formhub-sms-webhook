# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Messages'
        db.create_table(u'core_messages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=450)),
            ('when_to_send', self.gf('django.db.models.fields.DateTimeField')()),
            ('sent_when', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('sent_return_message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('hook_json_message', self.gf('django.db.models.fields.TextField')()),
            ('hook_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('hook_recieved', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Messages'])


    def backwards(self, orm):
        # Deleting model 'Messages'
        db.delete_table(u'core_messages')


    models = {
        u'core.messages': {
            'Meta': {'object_name': 'Messages'},
            'hook_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'hook_json_message': ('django.db.models.fields.TextField', [], {}),
            'hook_recieved': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '450'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sent_return_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sent_when': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'when_to_send': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['core']