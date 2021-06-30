from django import forms
from .widgets import DateRangeSlider, RangeSlider, Slider


class RangeSliderField(forms.CharField):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', '')
        self.minimum = kwargs.pop('minimum', 0)
        self.maximum = kwargs.pop('maximum', 100)
        self.step = kwargs.pop('step', 1)
        kwargs['widget'] = RangeSlider(self.minimum, self.maximum, self.step, self.name)
        if 'label' not in kwargs.keys():
            kwargs['label'] = False
        super(RangeSliderField, self).__init__(*args, **kwargs)


class DateRangeSliderField(forms.DateTimeField):
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
        print('___self min: ', self.minimum)
        # print('__self min: ', self.minimum.strftime("%Y"))
        self.maximum = kwargs.pop('maximum', 100)
        self.step = kwargs.pop('step', 1)
        kwargs['widget'] = DateRangeSlider(self.minimum, self.maximum, self.step, self.name)
        if 'label' not in kwargs.keys():
            kwargs['label'] = False
        super(DateRangeSliderField, self).__init__(*args, **kwargs)


class SliderField(forms.DateTimeField):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name', '')
        self.minimum = kwargs.pop('minimum', 0)
        self.maximum = kwargs.pop('maximum', 100)
        self.step = kwargs.pop('step', 1)
        kwargs['widget'] = Slider(self.minimum, self.maximum, self.step, self.name)
        if 'label' not in kwargs.keys():
            kwargs['label'] = False
        super(SliderField, self).__init__(*args, **kwargs)
