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

from taiga.base import response
from taiga.base import filters as base_filters
from taiga.base.api import ModelCrudViewSet, GenericViewSet
from taiga.base.api.utils import get_object_or_404
from taiga.projects.occ import OCCResourceMixin
from taiga.projects.userstories.models import UserStory

from . import filters
from . import models
from . import permissions
from . import serializers
from . import validators


class GameViewSet(OCCResourceMixin, ModelCrudViewSet):
    model = models.Game
    serializer_class = serializers.GameSerializer
    validator_class = validators.GameValidator
    permission_classes = (permissions.GamePermission,)
    filter_fields = ('project', 'uuid')
    lookup_field = "selector"
    lookup_value_regex = "[\w-]+\/[0-9a-f-]+$"

    def dispatch(self, request, *args, **kwargs):
        if "selector" in kwargs:
            (kwargs['project__slug'], kwargs['uuid']) = kwargs.pop('selector').split("/")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, **self.kwargs)
        return obj


class GameUsViewSet(GenericViewSet):
    serializer_class = serializers.UserStorySerializer
    queryset = UserStory.objects.all()
    permission_classes = (permissions.GamePermission,)
    filter_backends = (
        base_filters.CanViewUsFilterBackend,
        filters.GameFilterBackend,
    )
    filter_fields = ["milestone__isnull",
                     "status__is_archived",
                     "status__is_closed"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(queryset, many=True)

        return response.Ok(serializer.data)
