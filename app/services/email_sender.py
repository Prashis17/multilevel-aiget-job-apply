import asyncio
import smtplib
from email.message import EmailMessage

from app.config.settings import get_settings
from app.schemas.workflow import GeneratedEmail, RecruiterContact


class EmailSender:
    def __init__(self, rate_limit_seconds: int = 180) -> None:
        self.rate_limit_seconds = rate_limit_seconds

    async def send(self, recipient: RecruiterContact, generated: GeneratedEmail) -> str:
        settings = get_settings()
        if not recipient.email:
            return "skipped_no_recipient"
        if not settings.smtp_host or not settings.smtp_username or not settings.smtp_password:
            return "dry_run_no_smtp_configured"

        message = EmailMessage()
        message["Subject"] = generated.subject
        message["From"] = settings.smtp_from or settings.smtp_username
        message["To"] = recipient.email
        message.set_content(f"{generated.body}\n\n{generated.signature}")

        await asyncio.to_thread(self._send_smtp, message)
        await asyncio.sleep(self.rate_limit_seconds)
        return "sent"

    def _send_smtp(self, message: EmailMessage) -> None:
        settings = get_settings()
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
            smtp.starttls()
            smtp.login(settings.smtp_username, settings.smtp_password)
            smtp.send_message(message)

