from confapp import conf
from pyforms_web.organizers import no_columns, segment
from pyforms_web.basewidget import BaseWidget
from pyforms_web.web.middleware import PyFormsMiddleware
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget
from pyforms.controls import ControlEmptyWidget, ControlFileUpload, ControlButton
from rodentdb.models import Rodent
from rodentdb.admin import RodentResource

from users.apps._utils import FormPermissionsMixin
from users.apps._utils import limit_choices_to_database
from tablib.core import Dataset, UnsupportedFormat
import shutil
from os.path import dirname
# FIXME import this when users model is not present


class RodentImportWidget(BaseWidget):
    TITLE = 'Import Rodent'   
    
    LAYOUT_POSITION = conf.ORQUESTRA_NEW_WINDOW
    CREATE_BTN_LABEL = '<i class="upload icon"></i>Import'
    HAS_CANCEL_BTN_ON_ADD = False

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._csv_file = ControlFileUpload(label='Import CSV')
        self._import_btn = ControlButton(
            '<i class="upload icon"></i>Import',
            default=self.__import_evt,
            label_visible=False,
            css='basic blue',
            helptext='Import Rodent from CSV file',
        )

        self.formset = [
            '_csv_file',
            '_import_btn'
        ]

    def __import_evt(self):

        rodent_resource = RodentResource()

        if self._csv_file.filepath is not None:
            dataset = Dataset()

            try:
                with open(self._csv_file.filepath, 'r') as f:
                    imported_file = dataset.load(f.read())
            except UnsupportedFormat as uf:
                raise Exception("Unsupported format. Please select a CSV file with the Rodent template columns")
            finally:
                shutil.rmtree(dirname(self._csv_file.filepath))

            # Test the import first
            result = rodent_resource.import_data(dataset, dry_run=True, use_transactions=True, collect_failed_rows=True)
            if result.has_validation_errors():
                val_errors = ''
                for err in result.invalid_rows:
                    val_errors += f'row {err.number}:<br><ul>'
                    for key in err.field_specific_errors:
                        val_errors += f'<li>{key} &rarr; {err.field_specific_errors[key][0]}</li>'
                    for val in err.non_field_specific_errors:
                        val_errors += f'<li>Non field specific &rarr; {val}</li>'
                    val_errors += '</ul>'
                raise Exception(f"Validation error(s) on row(s): {', '.join([str(err.number) for err in result.invalid_rows])} <br>{val_errors}")
            elif result.has_errors():
                raise Exception(f"Error detected that prevents importing on row(s): {', '.join([str(num) for num, _ in result.row_errors()])}")
            else:
                rodent_resource.import_data(dataset, dry_run=False, use_transactions=True)
            
            self.success("Rodent file imported successfully!")


class RodentForm(FormPermissionsMixin, ModelFormWidget):

    CLOSE_ON_REMOVE = True

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
            return ModelFormWidget.title.fget(self)

    def get_fieldsets(self, default):
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
            )
        ]
        if self.object_pk:  # editing existing object
            default += [("maintainer", "ownership", "created", "modified")]

        return default

    def get_related_field_queryset(self, field, queryset):
        animaldb = self.model._meta.app_label
        queryset = limit_choices_to_database(animaldb, field, queryset)
        return queryset

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

    UID = "rodentdb"
    MODEL = Rodent

    TITLE = "Rodents"

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

    STATIC_FILES = ['rodentdb/icon.css']  # required for the menu icon CSS

    LAYOUT_POSITION = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU = "left"
    ORQUESTRA_MENU_ORDER = 1
    ORQUESTRA_MENU_ICON = "large congento-rodent"

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

        self._import_btn = ControlButton(
            '<i class="upload icon"></i>Import',
            default=self.__import_evt,
            label_visible=False,
            css='basic blue',
            helptext='Import Rodent from CSV file',
        )

        super().__init__(*args, **kwargs)

    def get_toolbar_buttons(self, has_add_permission=False):
        toolbar = super().get_toolbar_buttons(has_add_permission)
        return tuple([no_columns(toolbar, "_import_btn")])
    
    def __import_evt(self):
        RodentImportWidget(parent_win=self)
