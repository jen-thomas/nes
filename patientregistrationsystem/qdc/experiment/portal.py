import coreapi
import os

from datetime import date, timedelta

from django.conf import settings
from django.utils import translation

from .models import Experiment, Group, Subject, TeamPerson, User


class RestApiClient(object):
    client = None
    schema = None
    active = False

    def __init__(self):
        auth = coreapi.auth.BasicAuthentication(username=settings.PORTAL_API['USER'],
                                                password=settings.PORTAL_API['PASSWORD'])
        self.client = coreapi.Client(auth=auth)

        try:
            self.schema = self.client.get(settings.PORTAL_API['URL'] + ':' +
                                          settings.PORTAL_API['PORT'] + '/api/schema/')
            self.active = True
        except:
            self.active = False


def get_portal_status():
    return RestApiClient().active


# def send_user_to_portal(user):
#
#     rest = RestApiClient()
#
#     if not rest.active:
#         return None
#
#     try:
#         portal_user = rest.client.action(
#             rest.schema, ['researchers', 'read'], params={"nes_id": str(user.id)})
#
#     except:
#         portal_user = None
#
#     # general params
#     params = {"nes_id": str(user.id),
#               "first_name": user.first_name,
#               "surname": user.last_name,
#               "email": user.email}
#
#     # create or update
#     if portal_user:
#         # params["id"] = portal_user['id']
#
#         portal_user = rest.client.action(
#             rest.schema, ['researchers', 'update'], params=params)
#     else:
#         portal_user = rest.client.action(
#             rest.schema, ['researchers', 'create'], params=params)
#
#     return portal_user


def send_experiment_to_portal(experiment: Experiment):

    rest = RestApiClient()

    if not rest.active:
        return None

    # general params
    params = {"nes_id": str(experiment.id),
              "title": experiment.title,
              "description": experiment.description,
              "data_acquisition_done": str(experiment.data_acquisition_is_concluded),
              }

    action_keys = ['experiments', 'create']

    if experiment.ethics_committee_project_file:
        with open(settings.MEDIA_ROOT + '/' + str(experiment.ethics_committee_project_file), 'rb') as f:
            # params["ethics_committee_project_file"] = \
            #     coreapi.utils.File(os.path.basename(experiment.ethics_committee_project_file.name), f)

            portal_experiment = rest.client.action(rest.schema, action_keys,
                                                   params=params, encoding="multipart/form-data")
    else:
        portal_experiment = rest.client.action(rest.schema, action_keys,
                                               params=params, encoding="multipart/form-data")

    return portal_experiment


def send_experiment_end_message_to_portal(experiment: Experiment):

    rest = RestApiClient()

    if not rest.active:
        return None

    # general params
    params = {"experiment_nes_id": str(experiment.id),
              "status": "to_be_analysed"
              }

    action_keys = ['experiments', 'partial_update']

    portal_experiment = rest.client.action(rest.schema, action_keys, params=params)

    return portal_experiment


def send_group_to_portal(group: Group):

    rest = RestApiClient()

    if not rest.active:
        return None

    # general params
    params = {"experiment_nes_id": str(group.experiment.id),
              "title": group.title,
              "description": group.description,
              "inclusion_criteria": []
              }

    for criteria in group.classification_of_diseases.all():
        params['inclusion_criteria'].append({'code': criteria.code})

    action_keys = ['experiments', 'groups', 'create']

    portal_group = rest.client.action(rest.schema, action_keys, params=params)

    return portal_group


def send_experimental_protocol_to_portal(portal_group_id, textual_description, image):

    rest = RestApiClient()

    if not rest.active:
        return None

    params = {"id": portal_group_id}

    if textual_description:
        params["textual_description"] = textual_description

    action_keys = ['groups', 'experimental_protocol', 'create']

    if image:
        with open(settings.BASE_DIR + image, 'rb') as f:
            params["image"] = coreapi.utils.File(os.path.basename(image), f)
            portal_experimental_protocol = rest.client.action(rest.schema, action_keys,
                                                              params=params, encoding="multipart/form-data")
    else:
        portal_experimental_protocol = rest.client.action(rest.schema, action_keys, params=params)

    return portal_experimental_protocol


def send_participant_to_portal(portal_group_id, subject: Subject):

    rest = RestApiClient()

    if not rest.active:
        return None

    current_language = translation.get_language()
    translation.activate('en')
    gender_name = subject.patient.gender.name.lower()
    translation.activate(current_language)

    params = {"id": portal_group_id,
              "code": subject.patient.code,
              "gender": gender_name,
              "age": format((date.today() - subject.patient.date_birth) / timedelta(days=365.2425), '.4')}

    action_keys = ['groups', 'participant', 'create']

    portal_participant = rest.client.action(rest.schema, action_keys, params=params)

    return portal_participant


def send_research_project_to_portal(experiment: Experiment):

    rest = RestApiClient()

    if not rest.active:
        return None

    # general params
    params = {"experiment_nes_id": str(experiment.id),
              "title": experiment.research_project.title,
              "description": experiment.research_project.description,
              "start_date": experiment.research_project.start_date.strftime("%Y-%m-%d"),
              "keywords": []
              }

    for keyword in experiment.research_project.keywords.all():
        params['keywords'].append({'name': keyword.name})

    if experiment.research_project.end_date:
        params["end_date"] = experiment.research_project.end_date.strftime("%Y-%m-%d")

    action_keys = ['experiments', 'studies', 'create']

    portal_research_project = rest.client.action(rest.schema, action_keys , params=params)

    return portal_research_project


def send_collaborator_to_portal(research_project_id, team_person: TeamPerson):

    rest = RestApiClient()

    if not rest.active:
        return None

    params = {"id": research_project_id,
              "name": team_person.person.first_name + ' ' + team_person.person.last_name,
              "team": team_person.team.name,
              "coordinator": team_person.is_coordinator}

    action_keys = ['studies', 'collaborators', 'create']

    portal_participant = rest.client.action(rest.schema, action_keys, params=params)

    return portal_participant


def send_researcher_to_portal(research_project_id, researcher: User):

    rest = RestApiClient()

    if not rest.active:
        return None

    params = {"id": research_project_id,
              "name": researcher.first_name + ' ' + researcher.last_name,
              "email": researcher.email}

    action_keys = ['studies', 'researcher', 'create']

    portal_participant = rest.client.action(rest.schema, action_keys, params=params)

    return portal_participant


def get_experiment_status_portal(experiment_id):

    rest = RestApiClient()

    status = None

    if rest.active:

        try:
            portal_experiment = rest.client.action(
                rest.schema, ['experiments', 'read'], params={"experiment_nes_id": str(experiment_id)})
        except:
            portal_experiment = None

        if portal_experiment and 'status' in portal_experiment:
            status = portal_experiment['status']

    return status