#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
"""
    Time    : 2018/4/22 14:57
    Author  : LeeLong
    File    : ueditor.py
    Software: PyCharm
    Description:
"""
import xadmin
from django.db.models import TextField

from xadmin.views import BaseAdminPlugin, ModelFormAdminView, CreateAdminView, UpdateAdminView
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from django.conf import settings


class XadminUEditorWidget(UEditorWidget):
    def __int__(self, **kwargs):
        self.ueditor_option = kwargs
        self.Media.js = None
        super(XadminUEditorWidget, self).__init__(kwargs)


class UEditorPlugin(BaseAdminPlugin):
    def get_field_style(self, attrs, db_field, style, **kwargs):
        if style == 'ueditor':
            if isinstance(db_field, UEditorField):
                widget = db_field.formfield().widget
                param = {}
                param.update(widget.ueditor_settings)
                param.update(widget.attrs)
                return {'widget': XadminUEditorWidget(**param)}
        return attrs

    def block_extrahead(self, content, nodes):
        js = '<script type="text/javascript" src="%s" ></script>' % (settings.STATIC_URL + "ueditor/ueditor.config.js")
        js += '<script type="text/javascript" src="%s" ></script>' % (settings.STATIC_URL + "ueditor/ueditor.all.min.js")
        nodes.append(js)


xadmin.site.register_plugin(UEditorPlugin, UpdateAdminView)
xadmin.site.register_plugin(UEditorPlugin, CreateAdminView)