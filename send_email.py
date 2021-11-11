import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders


def send_mail(
    send_from,
    send_to,
    subject,
    message,
    files=[],
    server="",
    port=587,
    username="",
    password="",
    use_tls=True,
):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """

    if server == "gmail":
        server = "smtp.gmail.com"
    elif server == "outlook":
        server = "smtp.office365.com"

    mensage = MIMEMultipart()
    mensage["From"] = send_from
    mensage["To"] = COMMASPACE.join(send_to)
    mensage["Date"] = formatdate(localtime=True)
    mensage["Subject"] = subject

    mensage.attach(MIMEText(message, "html"))

    for path in files:
        part = MIMEBase("application", "octet-stream")
        with open(path, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", "attachment; filename={}".format(Path(path).name)
        )
        mensage.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, mensage.as_string())
    smtp.quit()
