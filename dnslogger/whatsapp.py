from twilio.rest import Client

client = Client()


from_whatsapp_number='whatsapp:+14155238886'

to_whatsapp_number='whatsapp:+6281808762209'

client.messages.create(body='logging telah dilakukan, terdadpat satu Query/Request yang tidak diinginkan!',
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)