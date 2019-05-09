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

from taiga.base.api import serializers
from taiga.base.fields import Field
from taiga.projects.mixins.serializers import StatusExtraInfoSerializerMixin
from taiga.projects.tagging.serializers import TaggedInProjectResourceSerializer


class GameSerializer(serializers.LightSerializer):
    id = Field()
    uuid = Field()
    name = Field()
    project = Field(attr="project_id")
    created_at = Field()
    end_at = Field()
    userstories = Field()
    scales = Field()
    roles = Field()
    discard = Field()
    notnow = Field()


class UserStorySerializer(StatusExtraInfoSerializerMixin, TaggedInProjectResourceSerializer,
                          serializers.LightSerializer):
    id = Field()
    ref = Field()
    subject = Field()
    is_blocked = Field()
    project = Field(attr="project_id")
    version = Field()
