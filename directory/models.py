from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Text(models.Model):
    title_en = models.CharField(max_length=100)
    title_fr = models.CharField(max_length=100)
    slug = models.SlugField(primary_key=True)
    content_en = models.TextField()
    content_fr = models.TextField()
    
    def __str__(self):
        return self.slug

    class Meta:
        verbose_name_plural = "text"


class Laboratory(models.Model):
    id = models.SlugField(primary_key=True, max_length=200)
    name = models.CharField(max_length=200)
    url = models.URLField(blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return ", ".join((self.id, self.city))

    class Meta:
        verbose_name_plural = "laboratories"


class Team(models.Model):
    id = models.SlugField(_("label"), primary_key=True, max_length=200, help_text=_("Please do not change"))
    name_en = models.CharField(_("English name"), max_length=200)
    name_fr = models.CharField(_("French name"), max_length=200)
    description_en = models.TextField(_("Description (English)"), blank=True)
    description_fr = models.TextField(_("Description (French)"), blank=True)
    lab = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True, verbose_name=_("laboratory"))
    logo = models.ImageField(null=True, upload_to="photos", blank=True)
    
    def __str__(self):
        return ", ".join((self.name_en, str(self.lab)))

    def projects(self):
        return Project.objects.filter(members__team=self.id).distinct()

    def collaborations(self):
        return None # should return just teams, or teams and researchers?

    def leader(self):
        return [researcher.user for researcher in self.members.filter(is_team_leader=True)]


class PositionType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    
class Researcher(models.Model):
    id = models.SlugField(_("label"), primary_key=True, help_text=_("Please do not change"))
    #user = models.OneToOneField(User, on_delete=models.CASCADE, help_text=_("Please do not change"))
    orcid = models.CharField("ORCID", max_length=19, blank=True)
    last_name = models.CharField(_("Last name"), max_length=100, blank=True)
    first_name = models.CharField(_("First name"), max_length=100, blank=True)
    middle_initials = models.CharField(_("Middle initials"), max_length=10, blank=True)
    email = models.CharField(_("E-mail"), max_length=100, blank=True)
    title = models.CharField(_("Title"), max_length=20, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name="members",
                             null=True, blank=True, verbose_name=_("research group"))
    is_team_leader = models.BooleanField(_("Group leader"), default=False)
    position = models.ForeignKey(PositionType, on_delete=models.SET_NULL, null=True, blank=True)
    interests_en = models.TextField(_("Research interests (English)"), blank=True)
    interests_fr = models.TextField(_("Research interests (French)"), blank=True)
    telephone = models.CharField(_("Telephone"), max_length=20, blank=True)
    photo = models.ImageField(null=True, upload_to="photos", blank=True)

    #"You need to register a handler for the signal django.db.models.signals.post_save on the User model, and, in the handler, if created=True, create the associated user profile.
    #For more information, see Chapter 12 of the Django book."

    def __str__(self):
        return " ".join((self.title, self.first_name, self.middle_initials, self.last_name))

    def full_name(self):
        return self.__str__()

    def collaborations(self):
        return self.__class__.objects.filter(
            projects__members=self.id).distinct().exclude(id=self.id)


class ResourceType(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    icon = models.ImageField(null=True, upload_to="icons", blank=True)

    def __str__(self):
        return self.id


class Resource(models.Model):
    type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    url = models.URLField()
    researcher = models.ForeignKey(Researcher, on_delete=models.SET_NULL,
                                   null=True, related_name="resources")

    def __str__(self):
        return "%s(%s)" % (self.type.id, self.researcher.full_name())
        

class Project(models.Model):
    id = models.SlugField(_("label"), primary_key=True, max_length=200, help_text="no spaces or punctuation except hyphen")
    name = models.CharField(max_length=200)
    short_description_en = models.TextField(_("Short description (English)"))
    short_description_fr = models.TextField(_("Short description (French)"))
    long_description_en = models.TextField(_("Long description (English)"), blank=True)
    long_description_fr = models.TextField(_("Long description (French)"), blank=True)
    members = models.ManyToManyField(Researcher, related_name="projects", verbose_name=_("contributors"))
    logo = models.ImageField(null=True, upload_to="photos", blank=True)
    # fields related to software projects only
    licence = models.CharField(max_length=50, blank=True)
    documentation = models.URLField(blank=True, help_text=_("URL of the project documentation"))
    download = models.URLField(blank=True, help_text=_("For software projects, URL where the software can be downloaded"))
    source_code = models.URLField(blank=True, help_text=_("For open-source software projects, URL where the source code is available"))
    
    def __str__(self):
        return self.name
    
    def editable_by(self, user):
        return Project.objects.filter(id=self, members__user=user).exists()
        
    def users(self):
        return [member.user for member in self.members.all()]
