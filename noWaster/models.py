# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models
from datetime import date

class User(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)

    id = models.CharField(max_length = 20, db_column='ID', db_index = True, primary_key=True)  # Field name made lowercase.

    stage = models.PositiveSmallIntegerField(default = 0)

    origin_loc_lat = models.FloatField(null = True)
    origin_loc_lng = models.FloatField(null = True)
    origin_loc_address = models.CharField(max_length = 200, blank = True)

    dest_loc_lat = models.FloatField(null = True)
    dest_loc_lng = models.FloatField(null = True)
    dest_loc_address = models.CharField(max_length = 200, blank = True)

    temporary_loc_lat = models.FloatField(null = True)
    temporary_loc_lng = models.FloatField(null = True)
    temporary_loc_address = models.CharField(max_length = 200, blank = True)

    profile_pic = models.URLField(blank = True)

    last_interaction_time = models.TimeField(auto_now = True)
    last_update_time = models.DateField(default = date.today)

    currently_responding_to = models.BooleanField(default = False)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'user'
        
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Loc(models.Model):
    name = models.CharField(max_length=50, blank=True, default = "")
    address = models.CharField(max_length=100, blank=True, default = "")
    id = models.AutoField(db_column='ID', primary_key=True) 

    class Meta:
        verbose_name = 'location'
        verbose_name_plural = 'locations'
        db_table = 'loc'

    def __str__(self):
        return "%s" % (self.name)

class Emoji(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    text = models.CharField(max_length = 20, blank = False)

    class Meta:
        verbose_name = 'emoji'
        verbose_name_plural = 'emojis'
        db_table = 'emoji'

    def __str__(self):
        return "%s" % (self.id)

class WeatherDictionary(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    description = models.CharField(max_length = 50, blank = False)
    emoji1 = models.ForeignKey(Emoji, null=True, related_name="emoji1")
    emoji2 = models.ForeignKey(Emoji, null=True, related_name="emoji2")

    class Meta:
        verbose_name = 'weather'
        db_table = 'weather'

    def __str__(self):
        return "%s" % (self.description)




