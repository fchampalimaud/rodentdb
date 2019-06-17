from confapp import conf
from pyforms_web.web.middleware import PyFormsMiddleware
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget

from rodentdb.models import Rodent
# from .permissions_list import PermissionsListApp


class RodentForm(ModelFormWidget):

    FIELDSETS = [
        'public',
        ("strain_name", "common_name", "origin", " "),
        ("species", "background", "genotype", "category"),
        ("availability", "mta"),
        "link",
        ("comments", "line_description"),
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

    def get_fieldsets(self, default):
        user = PyFormsMiddleware.user()
        if user.is_superuser:
            default += [("maintainer", "ownership"),]
        return default


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
        "ownership",
    ]

    SEARCH_FIELDS = [
        "strain_name__icontains",
        "common_name__icontains",
        "origin__icontains",
        "line_description__icontains",
        "comments__icontains",
    ]

    USE_DETAILS_TO_EDIT = False  # required to have form in NEW_TAB

    LAYOUT_POSITION = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU = 'left'
    ORQUESTRA_MENU_ORDER = 1
    ORQUESTRA_MENU_ICON = 'paw green'

    @classmethod
    def has_permissions(cls, user):
        if user.is_superuser:
            return True

        if user.groups.filter(name="Rodent Facility").exists():
            return True

        return False
