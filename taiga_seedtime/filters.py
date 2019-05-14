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

from taiga.base.filters import FilterBackend

from . import models


class GameFilterBackend(FilterBackend):
    def filter_queryset(self, request, queryset, view):
        if "uuid" not in request.QUERY_PARAMS:
            return []

        try:
            game = models.Game.objects.get(uuid=request.QUERY_PARAMS["uuid"])
        except models.Game.DoesNotExist:
            return []

        if request.GET.get('discard') != 'true':
            queryset = queryset.exclude(id__in=game.discard)

        return queryset.filter(project=game.project).exclude(id__in=[us['id'] for us in
                                                                     game.userstories])
