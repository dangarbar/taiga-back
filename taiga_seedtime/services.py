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

from django.db import transaction

from . import models


@transaction.atomic
def bulk_update_or_create_estimate(game):
    scale_names = {}
    for scale in game.scales:
        scale_names[scale["id"]] = scale["name"]

    for us in game.userstories:
        if us['id'] in game.discard:
            continue

        if 'scale_id' not in us or not us['scale_id'] in scale_names:
            continue

        models.Estimate.objects.update_or_create(
            project=game.project,
            userstory_id=us['id'],
            defaults={
                "game": game,
                "game_name": game.name,
                "estimate_value": scale_names[us['scale_id']],
            }
        )
