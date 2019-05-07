# Copyright (C) 2014-2019 Taiga Agile LLC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from taiga.base.db.models.fields import JSONField
from taiga.projects.occ import OCCModelMixin
from taiga.projects.models import Project


class Game(OCCModelMixin, models.Model):
    uuid = models.CharField(max_length=32, editable=False, null=True,
                            blank=True, default=None, db_index=True)
    name = models.CharField(max_length=250, null=False, blank=False,
                            verbose_name=_("name"))
    project = models.ForeignKey(Project, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name=_("create at"))
    end_at = models.DateTimeField(null=True, blank=True)
    userstories = JSONField()
    scales = JSONField()
    roles = JSONField(null=True, blank=True)
    discard = JSONField(null=True, blank=True)
    notnow = JSONField(null=True, blank=True)
    _importing = None
    _event_tag = "games"

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4().hex
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"
        ordering = ["project", "name", "uuid"]
        unique_together = ("project", "uuid")

    def __str__(self):
        return self.name
