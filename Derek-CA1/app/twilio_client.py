from twilio.rest import Client

# twilio_sid = "AC50c7bd2126893e87804f224bc6716103"
# twilio_token = "72ade69ed01dc1685c93e532b862556b"

twilio_sid = "ACc14127f85a8ba1af23949d90c04bc9a6"
twilio_token = "3c3c5ace80d0423990fb7de4466dc27c"
phone_num = "+12512629258"
passwd = "iloveIOT123iloveIOT123"

class TwilioClient:
    def __init__(self, twilio_sid, twilio_token, from_num):
        self.server = None
        self.sid = twilio_sid
        self.token = twilio_token
        self.from_num = from_num

    def notifyDetected(self, targets, body):
        client = Client(self.sid, self.token)
        print(body)
        for target in targets:
            # message = client.messages.create(
            #     from_="whatsapp:+12512629258", body=body, to="whatsapp:+65" + target
            # )
            # print(target)
            
            message = client.messages.create(
                     body=body,
                     from_=f'{self.from_num}',
                     to = target
                     # to='+6588582480'
                 )
            print("twilio client loop {}".format(target, message.status))

        print("Sent!")


# tc = TwilioClient(twilio_sid,twilio_token,phone_num)
# tc.notifyDetected(['+6588582480'],'I love IOT')