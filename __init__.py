# -*- coding: utf-8 -*-

import base64
import logging

from . import models

from odoo.addons.payment import reset_payment_provider, setup_provider
from odoo.tools import file_open

_logger = logging.getLogger(__name__)

PROVIDER_XMLID = 'euplatesc_payment_provider.payment_provider_euplatesc'
PROVIDER_NAME = 'EuPlătesc'
ICON_PATH = 'euplatesc_payment_provider/static/img/icon.png'


def _apply_branding(env):
    """Force the EuPlătesc provider display name and kanban icon.

    Kept as a Python hook because the provider record lives in a
    `noupdate="1"` data file, which prevents XML re-import on upgrade,
    and because Image fields set via `<field type="base64" file="...">`
    are not reliably refreshed on existing records.
    """
    provider = env.ref(PROVIDER_XMLID, raise_if_not_found=False)
    if not provider:
        return
    vals = {}
    if provider.name != PROVIDER_NAME:
        vals['name'] = PROVIDER_NAME
    try:
        with file_open(ICON_PATH, 'rb') as f:
            vals['image_128'] = base64.b64encode(f.read())
    except FileNotFoundError:
        _logger.warning("EuPlătesc icon not found at %s", ICON_PATH)
    if vals:
        provider.write(vals)


def post_init_hook(env):
    setup_provider(env, 'euplatesc')
    _apply_branding(env)


def uninstall_hook(env):
    reset_payment_provider(env, 'euplatesc')
