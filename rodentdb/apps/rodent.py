from confapp import conf
from pyforms_web.organizers import no_columns, segment
from pyforms_web.web.middleware import PyFormsMiddleware
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget
from pyforms.controls import ControlEmptyWidget
from rodentdb.models import Rodent
# from .permissions_list import PermissionsListApp


class RodentForm(ModelFormWidget):

    # INLINES = [PermissionsListApp]

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_TAB

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mta.checkbox_type = ""
        self.mta.label_visible = False
        self.public.checkbox_type = ""
        self.public.label_visible = False

        self.origin_other_placeholder = ControlEmptyWidget()
        self.origin_other.label = "Please specify other origin"
        self.origin.changed_event = self.__on_origin

        self.__on_origin()

    @property
    def title(self):
        try:
            return self.model_object.strain_name
        except AttributeError:
            pass  # apparently it defaults to App TITLE

    def get_fieldsets(self, default):
        user = PyFormsMiddleware.user()

        default = [
            segment(
                ("species", "category"),
                ("strain_name", "common_name"),
                ("background", "zygosity"),
                ("reporter_gene", "inducible_cassette"),
                ("coat_color", " "),
                ("origin", "origin_other", "origin_other_placeholder"),
                ("availability", "link"),
                no_columns("mta"),
                no_columns("public"),
                "info:You can use the <b>Line description</b> field below to "
                "provide more details. Use the <b>Comments</b> field below for "
                "private notes.",
                ("line_description", "comments"),
            ),
            # 'PermissionsListApp'

        ]

        if user.is_superuser:
            default += [("maintainer", "ownership"),]

        return default

    def __on_origin(self):
        model = self.origin.queryset.model
        try:
            selected_value = model.objects.get(pk=self.origin.value)
        except model.DoesNotExist:
            self.origin_other.hide()
            self.origin_other_placeholder.show()
        else:
            if selected_value.name.lower() == "other":
                self.origin_other.show()
                self.origin_other_placeholder.hide()
            else:
                self.origin_other.hide()
                self.origin_other_placeholder.show()


class RodentApp(ModelAdminWidget):

    UID = 'rodentdb'
    MODEL = Rodent

    TITLE = 'Rodents'

    EDITFORM_CLASS = RodentForm

    LIST_DISPLAY = [
        "species",
        "category",
        "strain_name",
        "zygosity",
        "background",
        "origin",
        "mta",
        "availability",
    ]

    LIST_FILTER = [
        "species",
        "category",
        "zygosity",
        "background",
        "mta",
        "availability",
        "ownership",
        "public",
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

        if user.memberships.filter(
                group__accesses__animaldb=cls.MODEL._meta.app_label
        ).exists():
            return True

        return False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
