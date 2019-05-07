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

from django.utils.translation import ugettext as _

from taiga.base.api import validators
from taiga.base.exceptions import ValidationError

from . import models


class GameValidator(validators.ModelValidator):
    class Meta:
        model = models.Game

    def validate_roles(self, attrs, source):
        project = attrs.get("project", None if self.object is None else self.object.project)
        if project is None:
            return attrs

        roles = attrs[source]
        if not isinstance(roles, list):
            raise ValidationError(_("Invalid roles format"))

        for role_id in roles:
            if not isinstance(role_id, int):
                raise ValidationError(_("Invalid role id format"))

            if project.roles.filter(id=role_id).count() == 0:
                raise ValidationError(_("Invalid role for the project"))

        return attrs

    def validate_scales(self, attrs, source):
        scales = attrs[source]
        if not isinstance(scales, list):
            raise ValidationError(_("Invalid scales format"))

        for scale in scales:
            if "id" not in scale or "name" not in scale:
                raise ValidationError(_("Invalid scale format"))

        return attrs

    def validate_userstories(self, attrs, source):
        project = attrs.get("project", None if self.object is None else self.object.project)
        if project is None:
            return attrs

        userstories = attrs[source]
        if not isinstance(userstories, list):
            raise ValidationError(_("Invalid user stories format"))

        scales = attrs["scales"] if self.object is None else self.object.scales
        scales = list(map(lambda x: x['id'], scales))

        for us in userstories:
            if "id" not in us:
                raise ValidationError(_("Invalid user story format"))

            if project.user_stories.filter(id=us['id']).count() == 0:
                raise ValidationError(_("Invalid user story for the project"))

            if 'scale_id' in us and us['scale_id'] is not None and us['scale_id'] not in scales:
                raise ValidationError(_("Invalid scale id for user story"))

        return attrs
