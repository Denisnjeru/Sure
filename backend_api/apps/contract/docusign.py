
import sys
sys.path.insert(1, '../../backend')
from settings import development as settings
import jwt
from jose import jws
from cryptography.hazmat.primitives import serialization as crypto_serialization
import time
from django.http import HttpResponseRedirect, HttpResponse
import base64
import requests
import os
from docusign_esign import RecipientViewRequest, EnvelopeDefinition, Document, Signer, SignHere, Tabs, Recipients, ApiClient, EnvelopesApi, Text, DateSigned, CarbonCopy
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
from datetime import date
from rest_framework.decorators import api_view

def docusign_token():
     iat = time.time()
     exp = iat+(3600*24)
     payload = {
         "sub": settings.client_user_id,
         "iss": settings.CLIENT_AUTH_ID,
         "iat": iat, # session start_time
         "exp": exp, # session end_time
         "aud":"account-d.docusign.com",
         "scope":"signature"
      }
     with open('private_key.pem', "rb") as key_file:
       private_key = crypto_serialization.load_pem_private_key(key_file.read(), password=None)
     key = private_key.private_bytes(crypto_serialization.Encoding.PEM, crypto_serialization.PrivateFormat.PKCS8, crypto_serialization.NoEncryption())
     jwt_token = jws.sign(payload, key, algorithm='RS256')
     return jwt_token

def create_jwt_grant_token():
    token = docusign_token()
    logger.info('TOKEN',token)
    return token

print(create_jwt_grant_token())

# @csrf_exempt
# def docusign_signature(request):
#     try:
#         token = create_jwt_grant_token()
#         post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': token}
#         base_url = 'https://account-d.docusign.com/oauth/token'
#         r = requests.post(base url, data=post data)
#         token = r.json()
#         data = json.loads(request.body)
#         signer_email = data['email']
#         signer_name = data['full_name']
#         signer_type = data['type']
#         #document that are to be signed
#         with open(os.path.join(BASE DIR,'/home/gathage/Downloads/sample.docx'), 'rb') as file: # Your docusign file path
#             content_bytes = file.read()
#         base64_file_content = base64.b64encode(content_bytes).decode('ascii')
#
#         if signer_type == 'embedded':
#             url, envelope id = signature by_embedded(token, base64 file_ content, signer name, signer email)
#         elif signer type 'email':
#             envelope_id = signature_by_email(token, base64_file_content, signer_name, signer_email)
#             url = ''
#         return JsonResponse({ 'docsign_url': url, 'envelope_id': envelope id, 'message':'Docusign', 'error': " }, status=status.HTTP 200_OK)
#     except Exception as e:
#         return JsonResponse({ 'docsign_url': 'envelope_id': 'message':'Internal server error', 'error': In docusign_signature: '+str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
# def signature_by_email(token, base64_file_content, signer_name, signer_email):
#     try:
#         # Create the document model
#         document = Document( # create the DocuSign document object
#             document_base64 = base64_file_content,
#             name = 'Example document', # can be different from actual file name
#             file extension = 'docx', # many different document types are accepted
#             document_id = '1' # a label used to reference the doc
#         )
#         sign_here = SignHere(
#             document_id = '1',
#             page_number = '1',
#             recipient_id = '1',
#             tab_label = 'SignHereTab',
#             y_position='513',
#             x_position='80'
#         )
#         today = date.today()
#         curr_date = today.strftime('%d/%m/%Y')
#         sign_date = DateSigned(
#             document id = '1',
#             page number = '1',
#             recipient_id= '1',
#             tab_label = 'Date',
#             font='helvetica',
#             value=curr_date,
#             tab_id='date',
#             font_size='size16',
#             y_position='55',
#             x_position='650'
#         )
#         text_name = Text(
#             document_id = '1',
#             page_number = '1',
#             recipient_id = '1',
#             tab_label = 'Name',
#             font='helvetica',
#             bold='true',
#             value=signer_name,
#             tab_id='name',
#             font_size='size16',
#             y_position='280',
#             x_position='54'
#         )
#         text_email = Text( document_id = '1', page number = '1', recipient id= '1', tab label = 'Email', font.'helvetica', bold.'true', value=signer_email, tab_id='email', font_size='size16', y position.'304', x position.'82'
# ) # Pixels from Left = 82 Email # Pixels from Top = 306 signer_tab = Tabs(sign_here_tabs=[sign_here], text_tabs =[text_name, text_email, sign_date]) signer = Signer( email = signer email, name.signer name, recipient id = '1', routing order = '1', tabs =signer tab ) # create a cc recipient to receive a copy of the documents ccl = CarbonCopy( email=signer_email, name=signer_name, recipient  id='2', routing order.'2'
# ) # Next, create the top level envelope definition and populate it. envelope definition = EnvelopeDefinition( email_subject = 'Please sign this document sent from the Python SDK', documents = [document], # The Recipients object wants arrays for each recipient type recipients = Recipients(signers.[signer], carbon copies.[cc1]), status = 'sent' # requests that the envelope be created and sent.
# ) try: #STEP-2 create/send envelope api_client = ApiClient() api_client.host = 'https://demo.docusign.net/restapi' api client.set default header('Authorization', 'Bearer ' + token['access token'])
# envelope api = EnvelopesApi(api client) results = envelope api.create envelope(account id.account id, envelope definition =envelope definition) envelope_id = results.envelope_id return envelope_id except Exception as e: return JsonResponse({ 'docsign url': ", 'envelope id': ", 'message':'Internal server error', 'error': 'In signature by email: '+str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) except Exception as e: return 3sonResponse({ 'docsign url': 'envelope id': ", 'message':'Internal server error', 'error': 'In signature by email: '+str(e) status=status.HTTP_500_INTERNAL_SERVER_ERROR)
