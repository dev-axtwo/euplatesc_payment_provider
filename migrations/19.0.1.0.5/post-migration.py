# -*- coding: utf-8 -*-
"""Re-apply EuPlătesc branding (name + icon) on upgrade.

The provider record lives in a `noupdate="1"` data file so XML changes to
`name` do not propagate on upgrade, and the standalone image data file does
not reliably refresh `image_128` on pre-existing records either. This script
uses the shared helper from the module's `__init__` to write both fields.
"""

import logging

from odoo.addons.euplatesc_payment_provider import _apply_branding

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo.api import Environment, SUPERUSER_ID
    env = Environment(cr, SUPERUSER_ID, {})
    _apply_branding(env)
    _logger.info("EuPlătesc: branding refreshed (name + image_128)")
