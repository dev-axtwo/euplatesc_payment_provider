# -*- coding: utf-8 -*-

from odoo import api, fields, models

from odoo.addons.euplatesc_payment_provider import const


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('euplatesc', 'EuPlatesc')],
        ondelete={'euplatesc': 'set default'},
    )

    @api.depends('code', 'state', 'company_id')
    def _compute_journal_id(self):
        super()._compute_journal_id()
        for provider in self.filtered(lambda p: p.code == 'euplatesc' and not p.journal_id):
            journal = self.env['account.journal'].search(
                [
                    ('company_id', '=', provider.company_id.id),
                    ('type', '=', 'bank'),
                ],
                order='sequence, id',
                limit=1,
            )
            if journal:
                provider.journal_id = journal

    def _get_default_payment_method_codes(self):
        self.ensure_one()
        if self.code != 'euplatesc':
            return super()._get_default_payment_method_codes()
        return const.DEFAULT_PAYMENT_METHOD_CODES
