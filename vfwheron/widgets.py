from django import forms
from django.template import Template, Context
from django.utils.safestring import mark_safe
import re


class Slider(forms.HiddenInput):
    def __init__(self, minimum, maximum, step, elem_name, onchange, *args, **kwargs):
        widget = super(Slider, self).__init__(*args, **kwargs)
        self.minimum = str(minimum)
        self.maximum = str(maximum)
        self.step = str(step)
        self.elem_name = str(elem_name)
        self.onchange = str(onchange)

    def render(self, name, value, attrs=None, renderer=None):
        s = super(Slider, self).render(name, value, attrs)
        self.elem_id = re.findall(r'id_([A-Za-z0-9_\./\\-]*)"', s)[0]
        template = Template("""<div class="slidecontainer">
        <input type="range" min={{ minimum }} max={{ maximum }} value={{ minimum }} class="slider"
        id='valueslider_{{ id }}'><p>{{ id }}: <span id='slidOut_{{ id }}'></span></p></div>""")
        html = template.render(Context({'id': self.elem_id, 'minimum': self.minimum, 'maximum': self.maximum}))
        return mark_safe(s + html)


class RangeSlider(forms.TextInput):
    def __init__(self, minimum, maximum, step, elem_name, onchange, *args, **kwargs):
        widget = super(RangeSlider, self).__init__(*args, **kwargs)
        self.minimum = str(minimum)
        self.maximum = str(maximum)
        self.step = str(step)
        self.elem_name = str(elem_name)
        self.onchange = str(onchange)

    def render(self, name, value, attrs=None, renderer=None):
        s = super(RangeSlider, self).render(name, value, attrs)
        self.elem_id = re.findall(r'id_([A-Za-z0-9_\./\\-]*)"', s)[0]
        html = """<div onmouseup='""" + self.onchange + """' onmouseleave='""" + self.onchange + """' id="slider-range-""" + self.elem_id + """"></div>
        <script>
        """ + self.onchange + """
        $('#id_""" + self.elem_id + """').attr("readonly", true)
        $( "#slider-range-""" + self.elem_id + """" ).slider({
        range: true,
        min: """ + self.minimum + """,
        max: """ + self.maximum + """,
        step: """ + self.step + """,
        values: [ """ + self.minimum + """,""" + self.maximum + """ ],
        slide: function( event, ui ) {
          $( "#id_""" + self.elem_id + """" ).val(" """ + self.elem_name + """ "+ ui.values[ 0 ] + " - " + ui.values[ 1 ] );
        }
        });
        $( "#id_""" + self.elem_id + """" ).val(" """ + self.elem_name + """ "+ $( "#slider-range-""" + self.elem_id + """" ).slider( "values", 0 ) +
        " - " + $( "#slider-range-""" + self.elem_id + """" ).slider( "values", 1 ) );
        </script>
        """
        return mark_safe(s + html)


class DateRangeSlider(forms.DateInput):
    # TODO: Make sure min/max of Slider is min/max of data (no missing hours/..)
    def __init__(self, minimum, maximum, step, elem_name, onchange, *args, **kwargs):
        widget = super(DateRangeSlider, self).__init__(*args, **kwargs)
        self.minimum = str(minimum)
        self.maximum = str(maximum)
        self.step = str(step)
        self.elem_name = str(elem_name)
        self.onchange = str(onchange)

    def render(self, name, value, attrs=None, renderer=None):
        s = super(DateRangeSlider, self).render(name, value, attrs)
        self.elem_id = re.findall(r'id_([A-Za-z0-9_\./\\-]*)"', s)[0]
        # TODO: implement behaviour when mouse leaves slider without buttonup event
        # <div onmouseup='""" + self.onchange + """' onmouseleave='""" + self.onchange + """'
        html = """
        <div onmouseup='""" + self.onchange + """'
        id="slider-date-range-""" + self.elem_id + """"></div>
        <script>
        $('#id_""" + self.elem_id + """').attr("readonly", true)
        $( "#slider-date-range-""" + self.elem_id + """" ).slider({
        range: true,
        min: new Date('""" + self.minimum + """').getTime(),
        max: new Date('""" + self.maximum + """').getTime(),
        step: """ + self.step + """,
        values: [ new Date('""" + self.minimum + """'),new Date('""" + self.maximum + """') ],
        slide: function( event, ui ) {
          let minDate = new Date(ui.values[0]);
          let maxDate = new Date(ui.values[1]);
          $( "#id_""" + self.elem_id + """" )
          .val(" """ + self.elem_name + """ "+ minDate.toLocaleDateString() + " - " + maxDate.toLocaleDateString() );
          $( "#id_""" + self.elem_id + """" )
          .data("values", [minDate.toISOString().split('T')[0], maxDate.toISOString().split('T')[0]]);
          // if (event.keyCode >= 37 && event.keyCode <= 40) {
          // console.log(event.keyCode)
          if (event.keyCode == 13) {
          """ + self.onchange + """
          }
        }
        });
        // initial values of box:
        let minStart = new Date($( "#slider-date-range-""" + self.elem_id + """" ).slider("values", 0))
        .toLocaleDateString()
        let maxStart = new Date($( "#slider-date-range-""" + self.elem_id + """" ).slider("values", 1))
        .toLocaleDateString()
        $( "#id_""" + self.elem_id + """" ).val(" """ + self.elem_name + """ " + minStart + " - " + maxStart);
        </script>
        """
        return mark_safe(s + html)


class DateTimeRangeSlider(forms.DateTimeInput):
    def __init__(self, minimum, maximum, step, elem_name, onchange, *args, **kwargs):
        widget = super(DateTimeRangeSlider, self).__init__(*args, **kwargs)
        self.minimum = str(minimum)
        self.maximum = str(maximum)
        self.step = str(step)
        self.elem_name = str(elem_name)
        self.onchange = str(onchange)

    def render(self, name, value, attrs=None, renderer=None):
        s = super(DateTimeRangeSlider, self).render(name, value, attrs)
        self.elem_id = re.findall(r'id_([A-Za-z0-9_\./\\-]*)"', s)[0]
        html = """<div onmouseup='""" + self.onchange + """' onmouseleave='""" + self.onchange + """' id="slider-d-t-range-""" + self.elem_id + """"></div>
        <script>
        """ + self.onchange + """
        $('#id_""" + self.elem_id + """').attr("readonly", true)
        $( "#slider-d-t-range-""" + self.elem_id + """" ).slider({
        range: true,
        min: new Date('""" + self.minimum + """').getTime(),
        max: new Date('""" + self.maximum + """').getTime(),
        step: """ + self.step + """,
        values: [new Date('""" + self.minimum + """'), new Date('""" + self.maximum + """')],
        slide: function( event, ui ) {
          let minDate = new Date(ui.values[0]).toLocaleString();
          let maxDate = new Date(ui.values[1]).toLocaleString();
          $( "#id_""" + self.elem_id + """" ).val(" """ + self.elem_name + """ "+ minDate + " - " + maxDate );
        }
        });
        // initial values of box:
        let minStart = new Date($( "#slider-d-t-range-""" + self.elem_id + """" ).slider("values", 0)).toLocaleString()
        let maxStart = new Date($( "#slider-d-t-range-""" + self.elem_id + """" ).slider("values", 1)).toLocaleString()
        $( "#id_""" + self.elem_id + """" ).val(" """ + self.elem_name + """ " + minStart + " - " + maxStart);
        </script>
        """
        return mark_safe(s + html)
