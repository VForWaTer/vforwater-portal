from django import forms
from django.template import Template, Context
from django.utils.safestring import mark_safe
import re

from django.contrib.gis import forms
from django.contrib.gis.geos import GEOSGeometry
from django.shortcuts import render
from django.template import Template, Context, loader
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from vfw_home.models import Entries


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


class SearchableSelect(forms.Select):
    """
    Create a Searchable select box with several columns and an optional columns heading.
    Keywords are (Title is) searched too
    First value of values_list is the ID.
    """
    def __init__(self, item_attrs=[], *args, **kwargs):
        super(SearchableSelect, self).__init__(*args, **kwargs)
        self.item_attrs = item_attrs

    def render(self, name, value, attrs=None, **kwargs):

        self.elem_id = attrs['id']

        required = 'required' if attrs['required'] else ''
        heading = self.item_attrs['heading'] if 'heading' in self.item_attrs else []
        title = self.item_attrs['data-forsearch'][0] if 'data_foresearch' in self.item_attrs else ''

        select_head = """
        <input list={id_str} name={name} id="input{id_str}">
        <datalist {required} id={id_str}>
        <option value="" title={title}>{heading}
        </option>""".format(required=required, id_str=self.elem_id, title=title,
                            heading='&emsp;|&emsp;'.join(heading), name=name)

        all_options = ""
        for sc_idx, self_choices in enumerate(self.choices):  # loop table rows

            if sc_idx > 0:

                sc_list = self_choices[1][1:-1].split(', ')
                sc_list = [item.replace('None', "'-'") for item in sc_list]
                sc_list = [item.replace("'", "") for item in sc_list]

                if 'data-forsearch' in self.item_attrs:
                    option = "<option value={value} title='{title}'>{option}</option>" \
                        .format(value=sc_list[0], title=sc_list[-1], option='&emsp;|&emsp;'.join(sc_list[1:-1]))
                else:
                    option = "<option value={value} data-search=''>{option}</option>"\
                        .format(value=sc_list[0], option='&emsp;|&emsp;'.join(sc_list[1:]))

                all_options += option

        html = select_head + all_options + """</datalist>"""

        return mark_safe(html)


class TableSelect(forms.Select):
    """
    Create a select box with several columns and an optional columns heading. First value of values_list is the ID.
    """
    def __init__(self, item_attrs=[], *args, **kwargs):
        super(TableSelect, self).__init__(*args, **kwargs)
        self.item_attrs = item_attrs

    def render(self, name, value, attrs=None, **kwargs):

        self.elem_id = attrs['id']

        required = 'required' if attrs['required'] else ''
        heading = self.item_attrs['heading'] if 'heading' in self.item_attrs else []
        title = self.item_attrs['data-forsearch'][0] if 'data_foresearch' in self.item_attrs else ''

        select_head = """<select name="{name}" {required} id=id_{id_str}><option value="" title={title}>{heading}
        </option>""".format(required=required, id_str=self.elem_id, title=title, name=name,
                            heading='&emsp;|&emsp;'.join(heading))

        all_options = ""
        for sc_idx, self_choices in enumerate(self.choices):  # loop table rows

            if sc_idx > 0:

                sc_list = self_choices[1][1:-1].split(', ')
                sc_list = [item.replace('None', "'-'") for item in sc_list]
                sc_list = [item.replace("'", "") for item in sc_list]

                if 'data-forsearch' in self.item_attrs:
                    option = "<option value={value} title='{title}'>{option}</option>" \
                        .format(value=sc_list[0], title=sc_list[-1], option='&emsp;|&emsp;'.join(sc_list[1:-1]))
                elif 'title-col' in self.item_attrs:
                    option = "<option value={value} title='{title}'>{option}</option>" \
                        .format(value=sc_list[0], title=','.join(sc_list[self.item_attrs['title-col']:]),
                                option='&emsp;|&emsp;'.join(sc_list[1:self.item_attrs['title-col']]))
                else:
                    option = "<option value={0} data-search=''>{1}</option>"\
                        .format(sc_list[0], '&emsp;|&emsp;'.join(sc_list[1:]))

                all_options += option

        html = select_head + all_options + """</select>"""

        return mark_safe(html)


class TableSelect_plus(TableSelect):

    def __init__(self, *args, **kwargs):
        super(TableSelect_plus, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):
        tableselect = super(TableSelect_plus, self).render(name, value, attrs)

        plus = """
        <button type="button" class="collapsible" id="add"{name} onclick="vfw.util.collapsibleFun('quickfiltermore')">
          {% trans "new" %} """ + name + """"</button>
            <div class="content">
              <p>
                {% for obj in more %}
                  <div>{{ obj.name }}: {{ obj }} </div></br>
                {% endfor %}
              </p>
            </div>"""

        html = tableselect

        return html


class CustomOSMWidget(forms.OpenLayersWidget):
    """
    An OpenLayers/OpenStreetMap-based widget.
    """
    default_lon = 8.4327681  # Coordinates of KIT SCC Campus North, Karlsruhe, Germany
    default_lat = 49.0959129
    default_zoom = 7
    default_srid = 4326

    def __init__(self, attrs=None):
        super().__init__()
        for key in ('default_lon', 'default_lat', 'default_zoom'):
            self.attrs[key] = getattr(self, key)
        if attrs:
            self.attrs.update(attrs)
    def render(self, name, value, attrs=None, renderer=None):

        s = super(CustomOSMWidget, self).render(name, value, attrs)
        self.elem_id = re.findall(r'id_([A-Za-z0-9_\./\\-]*)"', s)[0]

        html = loader.get_template('vfw_home/map_widget.html').render(context={'name': name,
                                                                               'default_lon': self.default_lon,
                                                                               'default_lat': self.default_lat,
                                                                               'default_zoom': self.default_zoom,
                                                                               'default_srid': self.default_srid,
                                                                               'map_width': self.attrs['map_width'],
                                                                               'map_height': self.attrs['map_height'],
                                                                               })

        return html


class AutocompleteCharWidget(forms.ChoiceField, forms.TextInput):

    def __init__(self, *args, **kwargs):
        super(AutocompleteCharWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):

        s = super(AutocompleteCharWidget, self).render(name, value, attrs)
        self.elem_id = re.findall(r'id_([A-Za-z0-9_\./\\-]*)"', s)[0]

        html = loader.get_template('vfw_home/autocomplete_widget.html')\
            .render(context={'name': name,
                             'choices': self.choices,
                             })
        return html
