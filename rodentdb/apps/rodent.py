from confapp import conf
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget

from rodentdb.models import Rodent
# from .permissions_list import PermissionsListApp


class RodentForm(ModelFormWidget):

    FIELDSETS = [
        'public',
        ("species", "strain_name", "common_name"),
        "background",
        "genotype",
        "category",
        "origin",
        ("availability", "mta", 'lab'),
        "link",
        "comments",
        # 'PermissionsListApp'
    ]

    # INLINES = [PermissionsListApp]

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_TAB

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mta.checkbox_type = ""

    @property
    def title(self):
        try:
            return self.model_object.strain_name
        except AttributeError:
            pass  # apparently it defaults to App TITLE


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
        "category",
        "origin",
        "mta",
        "availability",
    ]

    LIST_FILTER = [
        "species",
        "background",
        "genotype",
        "category",
        "mta",
        "availability",
    ]

    SEARCH_FIELDS = [
        "species__icontains",
        "strain_name__icontains",
        "common_name__icontains",
        "background__icontains",
        "genotype__icontains",
        "category__icontains",
        "origin__icontains",
    ]

    USE_DETAILS_TO_EDIT = False  # required to have form in NEW_TAB

    LAYOUT_POSITION = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU = 'left'
    ORQUESTRA_MENU_ORDER = 1
    ORQUESTRA_MENU_ICON = 'paw green'
