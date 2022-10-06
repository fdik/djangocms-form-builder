import importlib

from django.conf import settings as django_settings

EMPTY_CHOICE = (("", "-----"),)

ADMIN_CSS = getattr(
    django_settings,
    "DJANGOCMS_FRONTEND_ADMIN_CSS",
    {},
)


FORM_OPTIONS = getattr(django_settings, "DJANGOCMS_FORMS_OPTIONS", {})


framework = getattr(django_settings, "DJANGOCMS_FRONTEND_FRAMEWORK", "bootstrap5")
theme = getattr(django_settings, "DJANGOCMS_FRONTEND_THEME", "djangocms_frontend")


SPACER_SIZE_CHOICES = (("mb-3", "Default"),)
TAG_CHOICES = (("div", "div"),)
FORM_TEMPLATE = getattr(django_settings, "FORM_TEMPLATE", None)

theme_render_path = f"{theme}.frameworks.{framework}"
theme_forms_path = f"{theme}.forms"


def render_factory(cls, theme_module, render_module):
    parents = tuple(
        getattr(module, cls, None)
        for module in (theme_module, render_module)
        if module is not None and getattr(module, cls, None) is not None
    )
    return type(cls, parents, dict())  # Empty Mix


def get_mixins(naming, theme_path, mixin_path):
    try:
        theme_module = importlib.import_module(theme_path) if theme_path else None
    except ModuleNotFoundError:
        theme_module = None
    try:
        render_module = importlib.import_module(mixin_path) if mixin_path else None
    except ModuleNotFoundError:
        render_module = None

    return lambda name: render_factory(
        naming.format(name=name), theme_module, render_module
    )


def get_renderer(my_module):
    if not isinstance(my_module, str):
        my_module = my_module.__name__
    return get_mixins(
        "{name}RenderMixin", theme_render_path, f"{my_module}.frameworks.{framework}"
    )


def get_forms(my_module):
    if not isinstance(my_module, str):
        my_module = my_module.__name__
    return get_mixins(
        "{name}FormMixin", theme_forms_path, f"{my_module}.frameworks.{framework}"
    )
