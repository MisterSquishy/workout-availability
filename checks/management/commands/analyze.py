from django.core.management.base import BaseCommand
import sendgrid
import os
from sendgrid.helpers.mail import *
from checks.models import Check
from checks.serializers import CheckSerializer
from django.db.models import Max, Sum, F
from django.contrib.postgres.aggregates import BoolOr
from django.forms.models import model_to_dict
import csv
import base64
from python_http_client.exceptions import BadRequestsError

CSV_PATH = os.getcwd() + '/data.csv'
HEADERS = ['location','slot_time','filled_seats','total_seats']

class Command(BaseCommand):
    def handle(self, **options):
        self.summarize()
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("pdavids219+isthisseattaken@gmail.com")
        to_email = Email("ald64@comcast.net")
        subject = "Some data for you"
        content = Content("text/plain", "Please enjoy this data I compiled for you. I hope it brings you joy.\n\nIt is with great shame I report that some rows have a taken_seats and total_seats value of -2. This indicates that the class filled up prior to our first check. Wowee!")
        with open(CSV_PATH, 'rb') as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.file_type = "text/csv"
        attachment.filename= "soulcycle.csv"
        attachment.disposition = "attachment"
        attachment.content_id = "SoulCycle"
        attachment.content = encoded
        mail = Mail(from_email, subject, to_email, content)
        mail.add_attachment(attachment)
        personalization = Personalization()
        personalization.add_to(to_email)
        personalization.add_bcc(Email("pdavids@comcast.net"))
        mail.add_personalization(personalization)
        try:
            response = sg.client.mail.send.post(request_body=mail.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except BadRequestsError as e:
            print(e.body)
        finally:
            os.remove(CSV_PATH)

    def summarize(self):
        qs = Check.objects.raw('SELECT MAX(id) id, location, slot_time, CASE ' +
            'WHEN BOOL_OR(is_full) then MAX(open_seats + taken_seats) ' +
            'ELSE MAX(taken_seats) END filled_seats, ' +
            'MAX(open_seats + taken_seats) total_seats ' +
            'FROM checks_check ' +
            'WHERE venue=\'SoulCycle\' ' +
            'GROUP BY location, slot_time ' +
            'ORDER BY location, slot_time DESC')
        with open(CSV_PATH, 'w', newline='') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(HEADERS)
            for check in qs:
                row = []
                for field in HEADERS:
                    row.append(str(getattr(check, field)))
                csvwriter.writerow(row)
