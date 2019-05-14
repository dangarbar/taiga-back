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

from django.apps import AppConfig
from django.conf.urls import include, url


class TaigaSeedtimeConfig(AppConfig):
    name = "taiga_seedtime"
    verbose_name = "TaigaSeedtime"

    def ready(self):
        from taiga.urls import urlpatterns
        from .routers import router
        urlpatterns.append(url(r'^api/v1/', include(router.urls)))
