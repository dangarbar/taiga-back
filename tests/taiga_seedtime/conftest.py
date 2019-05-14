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

import factory
import pytest

from django.conf import settings


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        strategy = factory.CREATE_STRATEGY

    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.LazyAttribute(lambda obj: '%s@email.com' % obj.username)
    password = factory.PostGeneration(lambda obj, *args, **kwargs: obj.set_password(obj.username))


class MilestoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "milestones.Milestone"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Milestone {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class ProjectTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = "projects.ProjectTemplate"
        django_get_or_create = ("slug",)

    name = "Template name"


class ProjectFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Project {}".format(n))
    slug = factory.Sequence(lambda n: "project-{}-slug".format(n))

    owner = factory.SubFactory("tests.factories.UserFactory")
    creation_template = factory.SubFactory("tests.factories.ProjectTemplateFactory")

    class Meta:
        model = "projects.Project"
        strategy = factory.CREATE_STRATEGY


class UserStoryStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "projects.UserStoryStatus"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "User Story status {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class UserStoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "userstories.UserStory"
        strategy = factory.CREATE_STRATEGY

    ref = factory.Sequence(lambda n: n)
    project = factory.SubFactory("tests.factories.ProjectFactory")
    subject = factory.Sequence(lambda n: "User Story {}".format(n))
    description = factory.Sequence(lambda n: "User Story {} description".format(n))
    status = factory.SubFactory("tests.factories.UserStoryStatusFactory")
    milestone = factory.SubFactory("tests.factories.MilestoneFactory")
    tags = factory.Faker("words")


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "taiga_seedtime.Game"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Game {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")
    userstories = {}
    scales = {}
    discard = []


@pytest.fixture
def games_world():
    projects = {
        "project_1": ProjectFactory(),
        "project_2": ProjectFactory()
    }

    userstories = {
        "us_1": UserStoryFactory(project=projects["project_1"]),
        "us_2": UserStoryFactory(project=projects["project_1"]),
        "us_3": UserStoryFactory(project=projects["project_1"]),
        "us_4": UserStoryFactory(project=projects["project_2"]),
        "us_5": UserStoryFactory(project=projects["project_2"]),
    }

    sizes = [{"id": 0, "name": "XS", "order": 1}, {"id": 1, "name": "S", "order": 2},
             {"id": 2, "name": "M", "order": 3}, {"id": 3, "name": "L", "order": 4},
             {"id": 4, "name": "XL", "order": 5}, {"id": 5, "name": "XXL", "order": 6}]

    points = [{"id": 0, "name": "0", "order": 1}, {"id": 1, "name": "3", "order": 2},
              {"id": 2, "name": "5", "order": 3}, {"id": 3, "name": "8", "order": 4}]

    games = {
        "game_1": GameFactory(
            project=projects["project_1"],
            scales=sizes,
            userstories=[
                {"id": userstories["us_1"].id, "scale_id": sizes[1]['id']},
                {"id": userstories["us_2"].id, "scale_id": sizes[2]['id']},
                {"id": userstories["us_3"].id, "scale_id": sizes[3]['id']},
            ],
            discard=[userstories["us_3"].id]

        ),
        "game_2": GameFactory(
            project=projects["project_1"],
            scales=points,
            userstories=[
                {"id": userstories["us_1"].id, "scale_id": sizes[1]['id']},
                {"id": userstories["us_3"].id, "scale_id": sizes[3]['id']},
                {"id": userstories["us_4"].id, "scale_id": sizes[5]['id']}
            ],
            discard=[userstories["us_4"].id]
        ),
        "game_3": GameFactory(
            project=projects["project_2"],
            scales=sizes,
            userstories=[
                {"id": userstories["us_4"].id, "scale_id": sizes[2]['id']},
                {"id": userstories["us_5"].id, "scale_id": sizes[4]['id']},
            ],
            discard=[userstories["us_5"].id]
        ),
    }

    return {**projects, **userstories, **games}
