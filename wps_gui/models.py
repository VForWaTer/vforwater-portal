# =================================================================
#
# Authors: Marcus Strobl <marcus.strobl@gmx.de>
#
# Copyright (c) 2024 Marcus Strobl
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class GeoAPIResults(models.Model):
    """
    Store data of creation in case datasets get an update.
    Last access time to be able to remove datasets not used for ages
    """
    PROCESS_STATES = [('CREATED', 'Process just created'),
                      ('ACCEPTED', 'Process just accepted'),
                      ('STARTED', 'Process just started'),
                      ('PENDING', 'Process is still running'),
                      ('FINISHED', 'Process ended successfully'),
                      ('ERROR', 'Process had an error'),
                      ]
    access = models.DateTimeField(blank=True, null=True)  # date of last access, relevant for cleaning
    creation = models.DateTimeField(default=timezone.now)  # creation date
    inputs = models.JSONField(max_length=4096)
    name = models.CharField(max_length=255)  # name of the process
    open = models.BooleanField()  # free to use for everyone?
    outputs = models.JSONField(blank=True, max_length=2048)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=8, choices=PROCESS_STATES, default='CREATED')

    def __str__(self):
        return f'{self.creation} - {self.name} - {self.status}'

    class Meta:
        managed = True
        db_table = 'wps_gui_geoapiresults'


class WebProcessingService(models.Model):
    """
    ORM for Web Processing Services settings.
    """
    name = models.CharField(max_length=30, unique=True)
    endpoint = models.CharField(max_length=1024)
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Web Processing Service'
        verbose_name_plural = 'Web Processing Services'
        managed = True

    def __str__(self):
        return self.name


class WpsResults(models.Model):
    """
    Store data of creation in case datasets get an update.
    Last access time to be able to remove datasets not used for ages
    """
    creation = models.DateTimeField(blank=True, null=True)
    access = models.DateTimeField(blank=True, null=True)
    open = models.BooleanField()
    outputs = models.CharField(max_length=1024)  # TODO: Use jsonField instead of CharField
    wps = models.CharField(max_length=255)
    inputs = models.CharField(max_length=2048)  # TODO: Use jsonField instead of CharField

    def __str__(self):
        return '%s %s' % (self.wps, self.inputs)

    class Meta:
        managed = True
        db_table = 'wps_gui_wpsresults'


class WpsDescription(models.Model):
    """
    Store information about wps process to reduce time to open workspace
    """
    service = models.CharField(max_length=30, default='')
    title = models.CharField(max_length=120, unique=True, default='')
    identifier = models.CharField(max_length=120, unique=True, default='')
    abstract = models.CharField(max_length=8192, default='')
    inputs = models.CharField(max_length=2048, default='')  # short description
    outputs = models.CharField(max_length=2048, default='')  # short description

    # extended schema for tools
    verbose = models.BooleanField()
    statusSupported = models.BooleanField(blank=True, default=False)
    storeSupported = models.BooleanField(blank=True, default=False)
    metadata = models.CharField(max_length=2048)
    dataInputs = models.CharField(max_length=4096)  # complete description
    processOutputs = models.CharField(max_length=2048)  # complete description

    lastUpdateDateCheck = models.DateTimeField(default=timezone.now, blank=True)
    version = models.CharField(max_length=8, default='', blank=True, null=True)

    def __str__(self):
        return 'service: %s, title: %s' % (self.service, self.title)

    class Meta:
        managed = True
