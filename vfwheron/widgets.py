from django import forms
from django.shortcuts import render
from django.template import Template, Context
from django.utils.safestring import mark_safe
import re


class RangeSlider(forms.TextInput):
    def __init__(self, minimum, maximum, step, elem_name, *args, **kwargs):
        widget = super(RangeSlider, self).__init__(*args, **kwargs)
        self.minimum = str(minimum)
        self.maximum = str(maximum)
        self.step = str(step)
        self.elem_name = str(elem_name)

    def render(self, name, value, attrs=None, renderer=None):
        s = super(RangeSlider, self).render(name, value, attrs)
        self.elem_id = re.findall(r'id_([A-Za-z0-9_\./\\-]*)"', s)[0]
        html = """<div id="slider-range-""" + self.elem_id + """"></div>
        <script>
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


class Slider(forms.HiddenInput):
    def __init__(self, minimum, maximum, step, elem_name, *args, **kwargs):
        widget = super(Slider, self).__init__(*args, **kwargs)
        self.minimum = str(minimum)
        self.maximum = str(maximum)
        self.step = str(step)
        self.elem_name = str(elem_name)

    def render(self, name, value, attrs=None, renderer=None):
        s = super(Slider, self).render(name, value, attrs)
        self.elem_id = re.findall(r'id_([A-Za-z0-9_\./\\-]*)"', s)[0]
        print('self.elem_id: ', self.elem_id)
        template = Template("""<div class="slidecontainer">
        <input type="range" min={{ minimum }} max={{ maximum }} value={{ minimum }} class="slider"
        id='valueslider_{{ id }}'><p>{{ id }}: <span id='slidOut_{{ id }}'></span></p></div>""")
        print('template: ', template)
        html = template.render(Context({'id': self.elem_id, 'minimum': self.minimum, 'maximum': self.maximum}))
        return mark_safe(s + html)

    # class Media:
    #     js = ('slider.js',)
    @property
    def media(self):
        print('in media....')
        print('in media....', self.elem_id)

        # return "console.log('da')"
        # "var slider = document.getElementById('valueslider_""" + self.elem_id + """');
        # var output = document.getElementById('slidOut_""" + self.elem_id + """');
        #        console.log('output: ', output);
        #        output.innerHTML = slider.value; // Display the default slider value
        #        // Update the current slider value (each time you drag the slider handle)
        #        slider.oninput = function () {
        #        output.innerHTML = this.value;
        #        }"""
        return forms.Media(css={'all': ('base.css',)},
                           js='slider.js',)
    #     return forms.Media(css={'all': ('pretty.css',)},
        #                    js=('animations.js', 'actions.js'))


