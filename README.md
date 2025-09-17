# MyPlugin

A simple Open edX plugin app for testing.

## Install

Inside LMS or CMS container:

```bash
pip install -e .
```

## Verify

```bash
./manage.py lms shell
```

```python
from django.apps import apps
[app.verbose_name for app in apps.get_app_configs()]
```

You should see **"My Plugin App"**.

## Test

- Visit: [http://localhost:18000/api/myplugin/](http://localhost:18000/api/myplugin/)
- Run: `./manage.py lms hello`
