# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from . import models  # noqa: F401


def uninstall_hook(cr, registry):
    """Remove the model metadata of ``vendor_payment`` manually.

    ``vendor_payment`` shares the physical table ``account_payment``
    with ``account.payment`` (``_table = "account_payment"``). During a normal
    uninstall Odoo unlinks the ``ir.model`` record of this model, which triggers
    ``ir.model._drop_table()`` and would run ``DROP TABLE account_payment
    CASCADE`` -- destroying the real ``account.payment`` data.

    To avoid that, we delete the ORM metadata of this model with raw SQL,
    bypassing the ``ir.model`` unlink machinery, so the shared table is left
    untouched.
    """
    cr.execute(
        """
        DELETE FROM ir_model_data
        WHERE model IN ('ir.model', 'ir.model.fields')
          AND res_id IN (
              SELECT id FROM ir_model
              WHERE model = 'vendor_payment'
          )
        """
    )
    cr.execute("DELETE FROM ir_model_fields WHERE model = 'vendor_payment'")
    cr.execute("DELETE FROM ir_model WHERE model = 'vendor_payment'")
