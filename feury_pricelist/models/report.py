# -*- coding: utf-8 -*-

import io
import logging
import os
import random
import string
import tempfile
import base64
from PyPDF2 import PdfFileReader, PdfFileWriter

from odoo import api, models, tools, _
from odoo.modules import get_resource_path, get_module_path
from odoo.exceptions import UserError, ValidationError


LOGGER = logging.getLogger(__name__)


MODULE_NAME = 'feury_pricelist'
PDF_FOLDER = os.path.join('static', 'src', 'pdf')


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


def read_docs(doc_names, FOLDER=PDF_FOLDER):
    docs = []
    doc_names = [doc_names] if isinstance(doc_names, str) else doc_names
    for doc_name in doc_names:
        doc_path = get_resource_path(MODULE_NAME, FOLDER, doc_name)

        with open(doc_path, 'rb') as f:
            docs.append(f.read())
    return docs[0] if len(docs)==1 else docs


DEFAULT_COVER_PAGE_PDF = 'catalog_cover_page.pdf'


class PDFReport(models.Model):
    _inherit = 'ir.actions.report'

    def _post_pdf(self, save_in_attachment, pdf_content=None, res_ids=None):
        CUSTOMER_PRICELIST = self.env['customer.pricelist']

        def default_report():
            return super(PDFReport, self)._post_pdf(
                save_in_attachment,
                pdf_content=pdf_content,
                res_ids=res_ids
            )

        def default_report_with_cover_page():
            report = default_report()
            cover_page_doc = self.env.company.pricelist_catalog_cover_page
            COVER_PAGE_PDF = base64.b64decode(cover_page_doc) \
                if cover_page_doc \
                else read_docs(DEFAULT_COVER_PAGE_PDF)

            return append_pdfs((COVER_PAGE_PDF, report))

        model = self.model
        report_name = self.report_name

        if model=='customer.pricelist' and report_name == 'feury_pricelist.report_pricelist_catalog':
            return default_report_with_cover_page()

        return default_report()
