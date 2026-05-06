import json
import logging
from django.http import (HttpResponse, JsonResponse,
                         HttpResponseBadRequest,     # 400
                         HttpResponseForbidden,      # 403
                         HttpResponseNotFound,       # 404
                         HttpResponseNotAllowed,     # 405
                         HttpResponseNotModified,    # 304
                         HttpResponseRedirect)       # 302
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model as DBModel
from django.views.generic import View
from django.urls import reverse
from allauth.socialaccount.models import SocialApp, SocialAccount
from .models import Text, Researcher, Team, Project
from .forms import ResearcherForm, TeamForm, ProjectForm


logger = logging.getLogger("directory")


def index(request):  # for debugging, to remove
    return HttpResponse("Hello, world. You're at the directory index.")


def profile(request):
    orcid_profile = SocialAccount.objects.get(user=request.user)
    #return JsonResponse({"orcid": orcid_profile.uid})
    return JsonResponse({
        "orcid": orcid_profile.uid,
        "profile": orcid_profile.extra_data
    })
    # todo: check if extra_data is updated when logging in after updating ORCID profile


def upload_photo(request, id):
    researcher = Researcher.objects.get(id=id)
    researcher.photo = request.FILES['file']
    researcher.save()
    return JsonResponse({"id": id})


def upload_logo(request, id):
    project = Project.objects.get(id=id)
    project.logo = request.FILES['file']
    project.save()
    return JsonResponse({"id": id})


class Serializer(object):

    @classmethod
    def serialize(cls, objects, request):
        if isinstance(objects, DBModel):
            data = cls._to_dict(objects, request)
        else:
            data = [cls._to_dict(obj, request) for obj in objects]
        encoder = DjangoJSONEncoder(ensure_ascii=False, indent=4)
        return encoder.encode(data)


class PeopleSerializer(Serializer):

    @staticmethod
    def _to_dict(obj, request):
        label = obj.id
        data = {
            "label": obj.id,
            "resource_uri": request.build_absolute_uri(reverse("researcher-profile-api", args=[obj.id])),
            "orcid": obj.orcid,
            "first_name": obj.first_name,
            "last_name": obj.last_name,
            "middle_initials": obj.middle_initials,
            "display_name": obj.full_name(),
            "title": obj.title,
            "team": {"uri": request.build_absolute_uri(reverse("team-profile-api", args=[obj.team.id])),
                        "label": obj.team.id,
                        "name_en": obj.team.name_en,
                        "name_fr": obj.team.name_fr,
                        "institution": obj.team.lab.name,
                        "institution_uri": obj.team.lab.url,
                        "city": obj.team.lab.city
                        },
            "is_team_leader": obj.is_team_leader,
            "position": getattr(obj.position, "name", ""),
            "interests_en": obj.interests_en,
            "interests_fr": obj.interests_fr,
            "telephone": obj.telephone,
            #keywords = models.ManyToManyField(Keyword, related_name="researchers")
            "projects": [{"uri": request.build_absolute_uri(reverse("project-profile-api", args=[project_id])),
                            "label": project_id}
                            for project_id in obj.projects.values_list("id", flat=True)]
        }
        try:
            data["photo"] = obj.photo.url
        except ValueError:
            pass
        return data


class TeamSerializer(Serializer):

    @staticmethod
    def _to_dict(obj, request):
        data = {
            "label": obj.id,
            "resource_uri": request.build_absolute_uri(reverse("team-profile-api", args=[obj.id])),
            "name_en": obj.name_en,
            "name_fr": obj.name_fr,
            "description_en": obj.description_en,
            "description_fr": obj.description_fr,
            "institution": obj.lab.name,
            "institution_uri": obj.lab.url,
            "city": obj.lab.city,
            "country": obj.lab.country,
            "members": [{"uri": request.build_absolute_uri(reverse("researcher-profile-api", args=[member_id])),
                         "label": member_id}
                        for member_id in obj.members.values_list("id", flat=True)],
            "projects": [{"uri": request.build_absolute_uri(reverse("project-profile-api", args=[project_id])),
                          "label": project_id}
                         for project_id in obj.members.values_list("projects__id", flat=True).distinct()]
        }
        try:
            data["logo"] = obj.logo.url
        except ValueError:
            pass
        return data


class ProjectSerializer(Serializer):

    @staticmethod
    def _to_dict(obj, request):
        data = {
            "label": obj.id,
            "name": obj.name,
            "resource_uri": request.build_absolute_uri(reverse("project-profile-api", args=[obj.id])),
            "short_description_en": obj.short_description_en,
            "short_description_fr": obj.short_description_fr,
            "long_description_en": obj.long_description_en,
            "long_description_fr": obj.long_description_fr,
            "contributors": [{"uri": request.build_absolute_uri(reverse("researcher-profile-api", args=[member.id])),
                              "label": member.id,
                              "orcid": member.orcid}
                             for member in obj.members.all()],
            "contributing_teams": [{"uri": request.build_absolute_uri(reverse("team-profile-api", args=[team_id])),
                                    "label": team_id}
                                   for team_id in obj.members.values_list("team__id", flat=True).distinct()],
            # fields related to software projects only
            "licence": obj.licence,
            "documentation": obj.documentation,
            "download": obj.download,
            "source_code": obj.source_code,
        }
        try:
            data["logo"] = obj.logo.url
        except ValueError:
            pass
        return data



class Resource(View):

    def _get_result(self, pk):
        try:
            result = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            result = None
        return result

    def get(self, request, *args, **kwargs):
        """View a result"""
        result = self._get_result(kwargs["id"])
        logger.info("Viewing {} {}".format(self.model.__name__, kwargs["id"]))
        if result is None:
            return HttpResponseNotFound("No such resource")
        content = self.serializer.serialize(result, request)
        return HttpResponse(content, content_type="application/json; charset=utf-8", status=200)


class ListResource(View):
    ordering = None

    def get(self, request, *args, **kwargs):
        """List of resources"""
        objects = self.model.objects.all()
        if self.ordering:
            objects = objects.order_by(self.ordering)
        logger.info("Viewing list of {}".format(self.model.__name__))
        content = self.serializer.serialize(objects, request)
        return HttpResponse(content, content_type="application/json; charset=utf-8", status=200)


class PeopleResource(Resource):
    serializer = PeopleSerializer
    model = Researcher

    def put(self, request, *args, **kwargs):
        # todo: check permissions
        data = json.loads(request.body.decode('utf-8'))
        researcher = self.model.objects.get(id=data["label"])
        for field in ("interests_en", "interests_fr"):
            setattr(researcher, field, data[field])
        researcher.save()
        content = self.serializer.serialize(researcher, request)
        return HttpResponse(content, content_type="application/json; charset=utf-8", status=201)
        #return HttpResponseBadRequest(errors.as_json(),
        #                                content_type="application/json; charset=utf-8")


class TeamResource(Resource):
    serializer = TeamSerializer
    model = Team


class TeamListResource(ListResource):
    serializer = TeamSerializer
    model = Team


class PeopleListResource(ListResource):
    serializer = PeopleSerializer
    model = Researcher
    ordering = "last_name"


class ProjectResource(Resource):
    serializer = ProjectSerializer
    model = Project

    def put(self, request, *args, **kwargs):
        # todo: check permissions
        data = json.loads(request.body.decode('utf-8'))
        project = self.model.objects.get(id=data["label"])
        for field in ("short_description_en",
                      "short_description_fr",
                      "long_description_en",
                      "long_description_fr",
                      "licence",
                      "documentation",
                      "download",
                      "source_code"):
            setattr(project, field, data[field])
        project.save()
        # todo: handle contributors
        logger.info(data['contributors'])
        for contributor_data in data["contributors"]:
            if "label" in contributor_data:
                contributor = Researcher.objects.filter(id=contributor_data["label"])
            elif "orcid" in contributor_data:
                contributor = Researcher.objects.filter(orcid=contributor_data["orcid"])
            else:
                contributor = None
                logging.warn("No contributor identifier")
            if contributor and contributor[0] not in project.members.all():
                project.members.add(contributor[0])
        content = self.serializer.serialize(project, request)
        return HttpResponse(content, content_type="application/json; charset=utf-8", status=201)


class ProjectListResource(ListResource):
    serializer = ProjectSerializer
    model = Project

    def post(self, request, *args, **kwargs):
        form = ProjectForm(json.loads(request.body.decode('utf-8')))
        if form.is_valid():
            project = form.save()
            content = self.serializer.serialize(project)
            return HttpResponse(content, content_type="application/json; charset=utf-8", status=201)
        else:
            return HttpResponseBadRequest(form.errors.as_json(),
                                          content_type="application/json; charset=utf-8")
