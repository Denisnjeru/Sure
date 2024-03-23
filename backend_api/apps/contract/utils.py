import aspose.words as aw
import os

from django.core.files import File
from django.urls import reverse
from datetime import date

from apps.common.utils import send_email


def contract_update_request_email(contract, target, requester):
    """
    Send contract update request email
    """
    email_body = f"Dear {contract.live_editor.first_name}, \n {requester.first_name} ({requester.username}) is requesting for a contract update."
    data = {
        "email_body": email_body,
        "to_email": contract.live_editor.email,
        "email_subject": "Contract Update Request",
    }
    send_email(data)

def contract_revision_changes(revision, compare_revision):
    # load first document
    doc = aw.Document(revision.document.path)

    # load second document
    doc2 = aw.Document(compare_revision.document.path)

    # compare documents
    doc.compare(doc2, "user", date.today())

    # save the document to get the revisions
    if (doc.revisions.count > 0):
        filepath = "/home/gathage/Downloads/" + str(revision.contract.id) + "_" + str(revision.id) + ".docx"
        doc.save(filepath)
        with open(filepath, 'rb') as fi:
            revision.changes = File(fi, name=os.path.basename(fi.name))
            revision.save()
    else:
        filepath = "/home/gathage/Downloads/sample.docx"
        with open(filepath, 'rb') as fi:
            revision.changes = File(fi, name=os.path.basename(fi.name))
            revision.save()
