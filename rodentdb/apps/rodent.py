from confapp import conf
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget

from rodentdb.models import Rodent
from .permissions_list import PermissionsListApp

class RodentForm(ModelFormWidget):

    FIELDSETS = [
        ("species", "strain_name", "common_name"),
        ("background", "background_other", " "),
        ("genotype", "genotype_other", " "),
        ("model_type", "model_type_other", " "),
        "origin",
        ("availability", "mta", 'lab'),
        "link",
        "comments",
        'PermissionsListApp'
    ]

    INLINES = [PermissionsListApp]

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_TAB

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mta.checkbox_type = ""

        self.background_other.label = "&nbsp"
        self.background.changed_event = self.__on_background

        self.genotype_other.label = "&nbsp"
        self.genotype.changed_event = self.__on_genotype

        self.model_type_other.label = "&nbsp"
        self.model_type.changed_event = self.__on_model_type

        self.__on_background()
        self.__on_genotype()
        self.__on_model_type()

    @property
    def title(self):
        try:
            return self.model_object.strain_name
        except AttributeError:
            pass  # apparently it defaults to App TITLE

    def __on_background(self):
        if self.background.value == "other":
            self.background_other.show()
        else:
            self.background_other.hide()

    def __on_genotype(self):
        if self.genotype.value == "other":
            self.genotype_other.show()
        else:
            self.genotype_other.hide()

    def __on_model_type(self):
        if self.model_type.value == "other":
            self.model_type_other.show()
        else:
            self.model_type_other.hide()


class RodentApp(ModelAdminWidget):

    UID = 'rodentdb'
    MODEL = Rodent

    TITLE = 'Rodents'

    EDITFORM_CLASS = RodentForm

    LIST_DISPLAY = [
        "species",
        "strain_name",
        "common_name",
        "background",
        "genotype",
        "model_type",
        "origin",
        "mta",
        "availability",
    ]

    LIST_FILTER = [
        "species",
        "background",
        "genotype",
        "model_type",
        "mta",
        "availability",
    ]

    SEARCH_FIELDS = [
        "species__icontains",
        "strain_name__icontains",
        "common_name__icontains",
        "background__icontains",
        "genotype__icontains",
        "model_type__icontains",
        "origin__icontains",
    ]

    USE_DETAILS_TO_EDIT = False  # required to have form in NEW_TAB

    LAYOUT_POSITION = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU = 'left'
    ORQUESTRA_MENU_ORDER = 1
    ORQUESTRA_MENU_ICON = 'database'
