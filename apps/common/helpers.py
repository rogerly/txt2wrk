import uuid
import re

from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import Field, RegexField, Select, CharField
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

def createUniqueDjangoUsername():
    '''
        Creates a GUID based username that is compatible with 
        Django limitations
    '''
    return (str(uuid.uuid4()).translate(None, '-'))[:30]

phone_digits_re = re.compile(r'^[+]?(?:1-?)?(\d{3})[-\.]?(\d{3})[-\.]?(\d{4})$')

class USPhoneNumberField(CharField):
    default_error_messages = {
        'invalid': _('Phone numbers must be in XXX-XXX-XXXX format.'),
    }

    def clean(self, value):
        super(USPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        value = re.sub('(\(|\)|\s+)', '', smart_unicode(value))
        m = phone_digits_re.search(value)
        if m:
            return u'%s-%s-%s' % (m.group(1), m.group(2), m.group(3))
        raise ValidationError(self.error_messages['invalid'])

pin_re = re.compile(r'^(\d{4})$')

class PhonePINField(CharField):
    default_error_messages = {
        'invalid': _('Password must be four digits long.'),
    }
    
    def clean(self, value):
        super(PhonePINField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        m = pin_re.search(value)
        if m:
            return u'%s' % (m,)
        raise ValidationError(self.error_messages['invalid'])