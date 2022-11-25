import re

import pandas as pd
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.gis import forms
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy

from .widgets import DateTimeRangeSlider, DateRangeSlider, RangeSlider, Slider, AutocompleteCharWidget


class SliderField(forms.DateTimeField):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', '')
        self.minimum = kwargs.pop('minimum', 0)
        self.maximum = kwargs.pop('maximum', 100)
        self.step = kwargs.pop('step', 1)
        self.onchange = kwargs.pop('onchange', '')
        kwargs['widget'] = Slider(self.minimum, self.maximum, self.step, self.name, self.onchange)
        if 'label' not in kwargs.keys():
            kwargs['label'] = False
        super(SliderField, self).__init__(*args, **kwargs)


class RangeSliderField(forms.CharField):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', '')
        self.minimum = kwargs.pop('minimum', 0)
        self.maximum = kwargs.pop('maximum', 100)
        self.step = kwargs.pop('step', 1)
        self.onchange = kwargs.pop('onchange', '')
        kwargs['widget'] = RangeSlider(self.minimum, self.maximum, self.step, self.name, self.onchange)
        if 'label' not in kwargs.keys():
            kwargs['label'] = False
        super(RangeSliderField, self).__init__(*args, **kwargs)


class DateRangeSliderField(forms.DateField):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', '')
        self.minimum = kwargs.pop('minimum', 0)
        self.maximum = kwargs.pop('maximum', 100)
        self.step = kwargs.pop('step', 1)
        self.onchange = kwargs.pop('onchange', '')
        kwargs['widget'] = DateRangeSlider(self.minimum, self.maximum, self.step, self.name, self.onchange)
        if 'label' not in kwargs.keys():
            kwargs['label'] = False
        super(DateRangeSliderField, self).__init__(*args, **kwargs)


class DateTimeRangeSliderField(forms.DateTimeField):
    """
    Create a date range slider in html. Your project needs jquery, jquery-ui and jquery-ui.css
    """
    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        self.name = kwargs.pop('name', '')
        self.minimum = kwargs.pop('minimum', 0)
        self.maximum = kwargs.pop('maximum', 100)
        self.step = kwargs.pop('step', 1)
        self.onchange = kwargs.pop('onchange', '')
        kwargs['widget'] = DateTimeRangeSlider(self.minimum, self.maximum, self.step, self.name, self.onchange)
        if 'label' not in kwargs.keys():
            kwargs['label'] = False
        super(DateTimeRangeSliderField, self).__init__(*args, **kwargs)


class CustomOSMField(forms.Field):

    default_error_messages = {
        'invalid': ugettext_lazy('Enter Latitude and Longitude'),
    }
    re_point = re.compile(r'^\s*(-?\d{1,3}(?:\.\d+)?),\s*(-?\d{1,3}(?:\.\d+)?)\s*,\s*(?:(\d{4,5})?)$')
    lat_pattern = re.compile(r'^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$')
    lon_pattern = re.compile(r'^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$')

    def __int__(self, separator=",", *args, **kwargs):

        self.attrs = kwargs.pop('attrs', '')
        # kwargs['widget'] = CustomMap(self.attrs)
        kwargs['widget'] = CustomOSMField(self.attrs)
        kwargs['max_length'] = 105
        self.separator = separator
        super(CustomOSMField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        value = super(CustomOSMField, self).to_python(value)
        if value in self.empty_values:
            return None
        try:
            m = self.re_point.match(force_text(value))
            lat = self.lat_pattern.match(m.group(1))
            lon = self.lon_pattern.match(m.group(2))
            srid = m.group(3)
            if not m or not lat or not lon or not srid:
                raise ValueError()
            value = Point(float(m.group(1)), float(m.group(2)), srid=int(m.group(3)))
            return value
        except (ValueError, TypeError):
            raise ValidationError(self.error_messages['invalid'], code='invalid')

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)


class AutocompleteCharField(forms.Field):

    default_error_messages = {
        'invalid': ugettext_lazy('Enter Latitude and Longitude'),
    }

    def __int__(self, *args, **kwargs):

        self.attrs = kwargs.pop('attrs', '')
        kwargs['widget'] = AutocompleteCharField(self.attrs)
        kwargs['max_length'] = 105
        super(AutocompleteCharField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        # TODO: there are still bugs in the template. Shouldn't show anything in URL
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        value = super(AutocompleteCharField, self).to_python(value)
        if value in self.empty_values:
            return None
        try:

            if not True:
                raise ValueError()
            # value = Point(float(m.group(1)), float(m.group(2)), srid=int(m.group(3)))
            return value
        except (ValueError, TypeError):
            raise ValidationError(self.error_messages['invalid'], code='invalid')

    def validate(self, value):
        """Check if value consists only of valid emails."""
        super().validate(value)
