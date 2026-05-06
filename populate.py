

import sys, os, django
from unidecode import unidecode
#sys.path.append(os.path.expanduser("~/dev"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "incf_france.settings")

django.setup()

from directory.models import Researcher, Laboratory, Team, Project


# People to contact about INCF French Node

people = """
Viktor; Jirsa; viktor.jirsa@univ-amu.fr;
Marmaduke; Woodman; marmaduke.woodman@univ-amu.fr;
Romain; Brette; romain.brette@inserm.fr;
Marcel; Stimberg; marcel.stimberg@inserm.fr;
Pierre; Yger; pierre.yger@inserm.fr;
Olivier; Marre; olivier.marre@gmail.com; http://oliviermarre.free.fr/index.html
Ryad; Benosman; ryad.benosman@upmc.fr;
Samuel; Garcia; samuel.garcia@cnrs.fr;
Denis; Engemann; denis.engemann@gmail.com;
Alexandre; Gramfort; alexandre.gramfort@inria.fr;
Alain; Destexhe; destexhe@unic.cnrs-gif.fr;
Bartosz; Telenczuk; bartosz.telenczuk@unic.cnrs-gif.fr;
Nicolas; Rougier; Nicolas.Rougier@inria.fr;
Simon; Thorpe; simon.thorpe@cerco.ups-tlse.fr;
Martial; Mermillod; martial.mermillod@upmf-grenoble.fr;
Sylvain; Saïghi; sylvain.saighi@ims-bordeaux.fr;
Pierre; Baudot; pierre.baudot@gmail.com;
Christoph; Pouzat; christophe.pouzat@ovh.fr;
#Jean-Baptiste; Poline; jbpoline@gmail.com;
Yves; Frégnac; fregnac@unic.cnrs-gif.fr;
Jean-Luc; Anton; Jean-Luc.Anton@univ-amu.fr;
Pierre; Kornprobst; pierre.kornprobst@inria.fr;
Laurent; Perrinet; laurent.perrinet@gmail.com;
Michel; Dojat; Michel.Dojat@ujf-grenoble.fr;
Peter Ford; Dominey; peter.dominey@inserm.fr; Stem Cell and Brain Research Institute, Inserm (Lyon)
Jan; Antolik; antolikjan@gmail.com;
Gaël; Varoquaux; gael.varoquaux@normalesup.org
Bertrand; Thirion; bertrand.thirion@inria.fr
Andrew; Davison; andrew.davison@unic.cnrs-gif.fr
Camille; Maumet; camille.maumet@inria.fr
"""
#neurostic folks?

teams = """
jirsa; Theoretical Neurosciences Group; Groupe ‘Neurosciences Théoriques’; ins; jirsa,woodman
brette; Computational neuroscience of sensory systems; Neurosciences computationnelles des systèmes sensoriels; institut-vision; brette,stimberg,yger
picaud; Retinal information processing - Pharmacology and Pathology; Transmission de l’information visuelle, pharmacotoxicité rétinienne et neuroprotection; institut-vision; marre
benosman; Vision and natural computation; Vision and natural computation; institut-vision; benosman,antolik
ravel-buonviso; Coding and Memory in Olfaction; Codage et mémoire olfactive; crnl; garcia
parietal; Parietal; Parietal; neurospin; gramfort,engemann,varoquaux,thirion
destexhe; Oscillatory and stochastic dynamics in thalamo-cortical networks; Dynamique oscillante et stochastique des réseaux thalamocorticaux; unic; destexhe, telenczuk
davison; Neuroinformatics for data-driven modeling and neuromorphic computing; Neuroinformatics for data-driven modeling and neuromorphic computing; unic; davison
mnemosyne; MNEMOSYNE; MNEMOSYNE; inria-bordeaux; rougier
maos; Mémoire et apprentissage des objets et des scènes; Memory and learning of objects and scenes; cerco; thorpe
psm; Perception et sensori-motricité; Perception and sensory motor research ; lpnc; mermillod
goaillard; Robustesse de l'excitabilité; Robustness of excitability; unis; baudot
stats-map5; Statistique; Statistics; map5; pouzat
cognisciences; Cognisciences: intégration et plasticité synaptique dans le cortex visuel; Cognisciences: synaptic integration and functional plasticity in primary visual cortex; unic; fregnac
invibe; Inférence et comportements visuels; Inference in visual behaviours; int; perrinet
irmf; Centre IRMf; fMRI Centre; int; anton
biovision; Equipe Biovision; Biovision team; inria-sophia; kornprobst
barbier; Neuroimagerie fonctionnelle et perfusion cérébrale; Functional neuroimaging and brain perfusion; gin; dojat
dominey; Human and robot cognitive systems; Human and robot cognitive systems; sbri; dominey
as2n; AS2N; AS2N; ims; saighi
visages; VisAGeS - Vision, Action and information manaGement System in health; VisAGeS - Vision, Action and information manaGement System in health; irisa; maumet
"""

labs = """
ins; Institut de Neurosciences des Systèmes (UMR1106), Inserm et Aix-Marseille Université; Marseille; France; http://ins.univ-amu.fr
institut-vision; Institut de la Vision; Paris; France; http://www.institut-vision.org/
crnl; Centre de Recherche en Neurosciences de Lyon (Inserm U1028 - CNRS UMR5292), Université Claude-Bernard; Lyon; France; http://www-crnl.univ-lyon1.fr/
neurospin; NeuroSpin; Saclay; France; http://joliot.cea.fr/drf/joliot/Pages/Entites_de_recherche/NeuroSpin.aspx
unic; UNIC, CNRS FRE 3693; Gif-sur-Yvette; France; https://www.unic.cnrs-gif.fr/
inria-bordeaux; Institut des Maladies Neurodégénératives; Bordeaux; France; http://www.inria.fr/en/teams/mnemosyne
cerco; Centre de Recherche Cerveau & Cognition (UMR5549); Toulouse; France; http://cerco.ups-tlse.fr/
lpnc; Laboratoire de Psychologie et NeuroCognition (UMR5105); Grenoble; France; http://lpnc.univ-grenoble-alpes.fr/
unis; Unité de Neurobiologie des canaux Ioniques et de la Synapse (INSERM - Aix-Marseille Université, UMR_S 1072); Marseille; France; http://unis-neuro.com
map5; Mathématiques Appliquées à Paris 5 (MAP5-UMR 8145); Paris; France; http://map5.mi.parisdescartes.fr/
int; Institut de Neurosciences de la Timone; Marseille; France; http://www.int.univ-amu.fr/
inria-sophia;  INRIA / Université Côte d’Azur; Sophia Antipolis; France; https://team.inria.fr/biovision/
gin; Grenoble Institut des Neurosciences; Grenoble; France; https://neurosciences.univ-grenoble-alpes.fr/
sbri; Stem-cell and Brain Research Institute; Lyon; France; http://www.sbri.fr/
ims; Laboratoire de l'Intégration du Matériau au Système; Bordeaux; France; https://www.ims-bordeaux.fr/
irisa; Institut de Recherche en Informatique et Systèmes Aléatoires; Rennes; France; https://www.irisa.fr/en
"""

networks = """
GDR NeuralNet
NeuroSTIC
GDR BioComp
"""

projects = """
PyNN; davison,yger
OpenElectrophy; garcia
Tridesclous; garcia
Spyking Circus; yger,marre
Brian; brette,stimberg
The Virtual Brain; jirsa,woodman
MNE; engemann,gramfort
ReScience; rougier
SpikeNet; thorpe
Neo; davison,garcia
Elephant; davison
"""

for line in labs.split("\n"):
    if line:
        id, name, city, country, url = [part.strip() for part in line.split(";")]
        lab, created = Laboratory.objects.get_or_create(id=id)
        print(id)
        lab.name = name
        lab.city = city
        lab.country = country
        lab.url = url
        lab.save()

for line in people.split("\n"):
    if line and not line.startswith("#"):
        parts = [part.strip() for part in line.split(";")]
        first_names, last_name, email = parts[:3]
        print(unidecode(last_name.lower()))
        researcher, created = Researcher.objects.get_or_create(id=unidecode(last_name.lower()),
                                                               first_name=first_names,
                                                               last_name=last_name,
                                                               email=email)
        if created:
            researcher.save()

for line in teams.split("\n"):
    if line:
        team_id, name_en, name_fr, lab_id, members = [part.strip() for part in line.split(";")]
        lab = Laboratory.objects.get(id=lab_id)
        team, created = Team.objects.get_or_create(id=team_id, lab=lab)
        team.name_en = name_en
        team.name_fr = name_fr
        team.lab = lab
        team.save()

        members = [m.strip() for m in members.split(",")]
        for member_id in members:
            member_obj = Researcher.objects.get(id=member_id)
            member_obj.team = team
            member_obj.save()

for line in projects.split("\n"):
    if line and not line.startswith("#"):
        project_name, contributor_labels = [part.strip() for part in line.split(";")]
        project_label = project_name.replace(" ", "")
        contributors = [Researcher.objects.get(id=label.strip())
                        for label in contributor_labels.split(",")]
        print(project_label, project_name, contributors)
        project, created = Project.objects.get_or_create(id=project_label)
        project.name = project_name
        if created:
            project.save()
        for contributor in contributors:
            project.members.add(contributor)
        project.save()
