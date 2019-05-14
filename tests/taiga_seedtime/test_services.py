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


import pytest

from taiga_seedtime import models, services


@pytest.mark.django_db
def test_bulk_update_or_create_estimate(games_world):
    estimates_queryset = models.Estimate.objects.order_by("created_date")

    services.bulk_update_or_create_estimate(games_world["game_1"])
    estimates = estimates_queryset.all()
    assert estimates_queryset.count() == 2
    assert [estimate.game_name for estimate in estimates] == ["Game 0", "Game 0"]
    assert [estimate.estimate_value for estimate in estimates] == ["S", "M"]

    services.bulk_update_or_create_estimate(games_world["game_2"])
    estimates = estimates_queryset.all()
    assert estimates_queryset.count() == 3
    assert [estimate.game_name for estimate in estimates] == ["Game 1", "Game 0", "Game 1"]
    assert [estimate.estimate_value for estimate in estimates] == ["3", "M", "8"]
    assert [estimate.userstory_id for estimate in estimates] == [games_world["us_1"].id,
                                                                 games_world["us_2"].id,
                                                                 games_world["us_3"].id]
