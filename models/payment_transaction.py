# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _compute_reference_prefix(self, separator, **values):
        """Build `{ORDER}-EUPL-{YYYYMMDD}` prefix for EuPlătesc transactions.

        Applies only when the provider is EuPlătesc AND at least one sale order
        is passed via the X2M command list on `sale_order_ids`. In all other
        cases we delegate to super() — in particular this preserves the stock
        sale override that returns joined order names for non-EuPlătesc
        providers, and the generic `tx-{datetime}` fallback.

        Suffix handling (-1, -2, ... for uniqueness within the same prefix) is
        done by the caller in `_compute_reference`, so we only need to emit the
        prefix itself.
        """
        provider_id = values.get('provider_id')
        command_list = values.get('sale_order_ids')
        if provider_id and command_list:
            provider = self.env['payment.provider'].browse(provider_id)
            if provider.exists() and provider.code == 'euplatesc':
                order_ids = self._fields['sale_order_ids'].convert_to_cache(
                    command_list, self,
                )
                orders = self.env['sale.order'].sudo().browse(order_ids).exists()
                if orders and len(orders) == len(order_ids):
                    order_part = separator.join(orders.mapped('name'))
                    today = fields.Date.context_today(self).strftime('%Y%m%d')
                    return f"{order_part}{separator}EUPL{separator}{today}"
        return super()._compute_reference_prefix(separator, **values)
