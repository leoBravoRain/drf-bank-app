import os
from typing import List

import resend
from pydantic import BaseModel

resend.api_key = os.environ.get("RESEND_API_KEY")


class EmailPayload(BaseModel):
    to: List[str]
    subject: str
    html: str
    from_: str


def send_email(payload: EmailPayload):

    params = {
        "from": payload.from_,
        "to": payload.to,
        "subject": payload.subject,
        "html": payload.html,
    }

    # def send_blocking():
    #     return resend.Emails.send(params)

    # email = await asyncio.to_thread(send_blocking)

    # print('Email was sent', email)

    # return {"status": "sent", "id": email['id']}
    try:
        print("TRYING TO SEND EMAIL")
        print(params)
        email = resend.Emails.send(params)
        print("Email sent succesfully", email)
        return {"status": "sent", "id": email["id"]}
    except Exception as e:
        return {"error": str(e)}
