from setuptools import setup, find_packages

setup(
    name="myplugin",
    version="0.1.0",
    description="A demo Open edX plugin app",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "lms.djangoapp": [
            "myplugin = myplugin.apps:MyPluginConfig",
        ],
        "cms.djangoapp": [],
    },
)
