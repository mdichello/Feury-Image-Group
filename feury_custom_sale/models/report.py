import io
import base64

from PyPDF2 import PdfFileReader, PdfFileWriter

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


def append_pdfs(pdfs):
    # doc of type PDF
    result_pdf = PdfFileWriter()
    for pdf in pdfs:
        doc = PdfFileReader(io.BytesIO(pdf))
        for page in doc.pages:
            result_pdf.addPage(page)

    result = io.BytesIO()
    result_pdf.write(result)
    return result.getvalue()


class PDFReport(models.Model):
    _inherit = 'ir.actions.report'

    def _post_pdf(self, save_in_attachment, pdf_content=None, res_ids=None):
        def default_report():
            return super(PDFReport, self)._post_pdf(
                save_in_attachment,
                pdf_content=pdf_content,
                res_ids=res_ids
            )

        record = self.env[self.model].browse(res_ids[0])

        if self.model == 'mrp.production' and self.report_name == 'mrp.report_mrporder':
            if record.embellishment_id and record.embellishment_id.sew_stripe_ids:
                extra_pdfs = [
                    base64.b64decode(pdf) for pdf in
                    record.embellishment_id.mapped('sew_stripe_ids.per_print_file')
                ]
                default_report_pdf = default_report()
                extra_pdfs.insert(0, default_report_pdf)
                mrp_report_pdf = append_pdfs(extra_pdfs)
                return mrp_report_pdf

        return default_report()
