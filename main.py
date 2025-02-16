import os
import argparse
import imaplib
import email
from email.header import decode_header
import requests
from datetime import datetime

# -------------------------
# Configuration
# -------------------------

IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.example.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", 993))
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT", "your-email@example.com")
PASSWORD = os.getenv("PASSWORD", "your-email-password")
SENDER_TO_MONITOR = os.getenv("SENDER_TO_MONITOR", "sender@example.com")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your-telegram-bot-token")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "your-telegram-channel-id")

IPERAL_PDF_LINK = os.getenv(
    "IPERAL_PDF_LINK",
    "https://example.com/menu.pdf"
)


def check_emails():
    """
    Fetch unseen emails from a specific sender and extract attachments.

    This function connects to an IMAP email server, searches for unseen emails from a
    specific sender, decodes attachment filenames and content, and retrieves the email
    subjects along with the attachments. After processing, the function marks the emails
    as seen.

    Returns:
        tuple: A tuple containing:
            attachments (list): A list of tuples, where each tuple contains the filename
                (str) and the content (bytes) of an attachment.
            email_subject (Optional[str]): The subject of the most recently processed email,
                or None if no email was successfully processed.
    """
    attachments = []
    email_subject = None

    # Connect to the mail server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.select("INBOX")

    # Search for unseen emails from a specific sender
    status, message_ids = mail.search(None, '(UNSEEN FROM "{}")'.format(SENDER_TO_MONITOR))
    if status == "OK":
        for msg_id in message_ids[0].split():
            res, msg_data = mail.fetch(msg_id, "(RFC822)")
            if res == "OK":
                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)

                # Decode subject for readability
                subject, encoding = decode_header(email_message["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                email_subject = subject

                # Walk through email parts to find attachments
                for part in email_message.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue

                    content_disposition = str(part.get("Content-Disposition", ""))
                    if "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            decoded_filename, fname_encoding = decode_header(filename)[0]
                            if isinstance(decoded_filename, bytes):
                                decoded_filename = decoded_filename.decode(
                                    fname_encoding if fname_encoding else "utf-8"
                                )
                            # Read the attachment directly into memory (bytes)
                            file_content = part.get_payload(decode=True)
                            attachments.append((decoded_filename, file_content))

                # Mark email as seen
                mail.store(msg_id, '+FLAGS', '\\Seen')

    mail.logout()
    return attachments, email_subject


def send_document_to_telegram(attachments):
    """
    Sends a list of file attachments to a Telegram bot's channel using the
    Telegram Bot API. Each attachment is sent as a document.

    Args:
        attachments (list of tuple): A list of tuples where each tuple contains
            the filename (str) and file bytes (bytes) to be sent as an
            attachment.

    Raises:
        ValueError: If the request to Telegram's API fails with a non-200
            status code.
    """
    # Send file attachments
    for filename, file_bytes in attachments:
        files = {"document": (filename, file_bytes)}
        response = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument",
            data={"chat_id": TELEGRAM_CHANNEL_ID},
            files=files,
        )
        if response.status_code != 200:
            print(f"Failed to send document '{filename}': {response.text}")


def send_msg_to_telegram_channel(msg_text):
    """
    Sends a message to a Telegram channel using the Telegram Bot API.

    This function sends a text message to a specific Telegram channel using the `sendMessage`
    endpoint of the Telegram Bot API. The bot token and the channel ID used in this function
    should already be configured as environment variables or constants. If the API call
    fails, the error response is printed.

    Args:
        msg_text: The message text to be sent to the Telegram channel.
    """
    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHANNEL_ID, "text": msg_text},
    )
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")


def check_and_send():
    """
    check_and_send()
    Checks for new emails, processes attachments, and sends them to a specified
    Telegram channel. If an email subject exists, it is formatted and sent as a
    text message to the channel. This function ensures timely notification and
    sharing of relevant email content.

    Raises:
        Any exception that might occur during the checking and sending of emails
        process will depend on the implementations of the underlying functions
        such as `check_emails()`, `send_msg_to_telegram_channel`, or
        `send_document_to_telegram`.
    """
    attachments, email_subject = check_emails()
    if attachments:
        # Send the email subject as a text message
        if email_subject:
            msg_text = "🍻 Birrificio: " + email_subject.lower().replace("fwd:", "").strip().capitalize()
            send_msg_to_telegram_channel(msg_text)
        # Sends the files on a channel
        send_document_to_telegram(attachments)
        print("New email found and processed.")
    else:
        print("No new emails.")


def check_and_send_iperal():
    """
    Checks the availability of a PDF file from the given URL and sends it to a Telegram
    channel if successfully fetched. The function appends the current Unix time to avoid
    cached results, formats a message with the current date, and sends the PDF
    document and the message to the specified Telegram channel.

    Raises:
        HTTPError: If the HTTP request from the provided URL fails.
    """
    # Gets the Unix time to append to the URL to avoid getting cached results
    unix_time = int(datetime.now().timestamp())
    response = requests.get(IPERAL_PDF_LINK + f"?{unix_time}")
    if response.status_code == 200:
        pdf_bytes = response.content
        pdf_filename = IPERAL_PDF_LINK.split("/")[-1]

        today_date = datetime.now().strftime("%d/%m/%Y")
        iperal_msg_text = f"🏪 Iperal: Menu settimana del {today_date}"
        send_msg_to_telegram_channel(iperal_msg_text)

        send_document_to_telegram([(pdf_filename, pdf_bytes)])
        print("PDF sent successfully.")
    else:
        print("Failed to fetch the PDF from the link.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CLI for checking emails or sending PDFs to Telegram.")
    parser.add_argument(
        "-b", "--birri",
        action="store_true",
        help="Check for new emails from the specific sender and send attachments to Telegram."
    )
    parser.add_argument(
        "-i", "--iperal",
        action="store_true",
        help="Fetch the Iperal menu PDF and send it to Telegram."
    )
    args = parser.parse_args()

    if args.birri:
        check_and_send()
    elif args.iperal:
        check_and_send_iperal()
    else:
        print("No action specified. Use --birri or --iperal.")
