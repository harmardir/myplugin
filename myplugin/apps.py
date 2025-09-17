from django.apps import AppConfig
from edx_django_utils.plugins.constants import PluginURLs, PluginSettings

class MyPluginConfig(AppConfig):
    name = "myplugin"
    verbose_name = "My Plugin App"

    plugin_app = {
        PluginURLs.CONFIG: {
            "lms.djangoapp": {
                PluginURLs.NAMESPACE: "myplugin",
                PluginURLs.REGEX: r"^api/myplugin/",
                PluginURLs.RELATIVE_PATH: "urls",
            },
        },
        PluginSettings.CONFIG: {
            "lms.djangoapp": {
                "common": {
                    PluginSettings.RELATIVE_PATH: "settings.common",
                },
                "devstack": {
                    PluginSettings.RELATIVE_PATH: "settings.devstack",
                },
                "production": {
                    PluginSettings.RELATIVE_PATH: "settings.production",
                },
            },
        },
    }
