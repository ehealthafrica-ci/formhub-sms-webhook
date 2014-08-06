# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Messages.hook_ip'
        db.alter_column(u'core_messages', 'hook_ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39))

    def backwards(self, orm):

        # Changing field 'Messages.hook_ip'
        db.alter_column(u'core_messages', 'hook_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15))

    models = {
        u'core.messages': {
            'Meta': {'object_name': 'Messages'},
            'hook_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
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