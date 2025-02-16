# Email and PDF Telegram Integration Bot

## Features
1. **Email Monitoring**:
Automatically monitors a specified email inbox to extract attachments or messages matching specific criteria (e.g., sender or subject).
2. **Telegram Integration**:
Sends extracted documents (PDFs or other file types) or plaintext messages to a defined Telegram channel or chat using a Telegram bot.
3. **PDF Retrieval from Websites**:
Retrieves PDFs from specified links on websites for further processing and sending.
4. **Modular System**:
Designed to be adaptable for additional use cases, enabling the transmission of various types of files or messages to Telegram.
5. **Command-Line Interface (CLI)**:
Allows users to interact with the script through CLI parameters to define its behavior.
6. **Configurable Parameters**:
    - Email server settings (IMAP).
    - Telegram bot token and channel ID.
    - Sender email to monitor.
    - External PDF links.

## System Workflow
1. **Email Parsing**:
The system connects to the specified email server using credentials, monitors emails from specific senders, and extracts matching documents or data.
2. **Document Processing**:
Extracted PDFs or messages are processed and prepared for Telegram transmission.
3. **Telegram Delivery**:
Using the provided bot token, the documents or messages are sent to the designated Telegram channel.
4. **Optional PDF Retrieval from Links**:
Provides support for downloading and sending documents from fixed URLs (use case involves website PDF links).

## Project Requirements
### 1. Python Packages
You will need the following libraries to run the system:
- **pip**: For installing dependencies.
- **requests**: For interacting with Telegram's API and downloading web content.
- **imaplib** (built-in library): For handling email protocol (IMAP).
- **email** (built-in library): For parsing email messages.

### 2. Configuration Parameters
The system relies on a set of environment variables or direct configuration in the script. These include:

| Variable Name | Purpose |
| --- | --- |
| `IMAP_SERVER` | The IMAP server address of your email provider. |
| `IMAP_PORT` | The port number to connect to the IMAP server. |
| `EMAIL_ACCOUNT` | Email address for logging into the IMAP server. |
| `PASSWORD` | Password for the email account. |
| `SENDER_TO_MONITOR` | Specific sender email to monitor. |
| `TELEGRAM_BOT_TOKEN` | Bot token for the Telegram bot. |
| `TELEGRAM_CHANNEL_ID` | Telegram channel or chat ID to send documents to. |
| `IPERAL_PDF_LINK` | (Optional) URL for retrieving a specific PDF file. |
## Command Line Interface (CLI) Parameters
his application provides a command-line interface (CLI) to perform certain tasks, such as checking emails and sending attachments to Telegram, or fetching and sending specific PDFs.
### Arguments
- `-b, --birri`:
Check for new emails from a specific sender and send the attachments to Telegram.
- `-i, --iperal`:
Fetch the Iperal menu PDF and send it to a Telegram chat.

### Example Usage
To check for emails and send attachments:
``` bash
python main.py --birri
```
To fetch and send the Iperal menu PDF:
``` bash
python main.py --iperal
```
If no argument is provided, the script will display a message prompting the user to specify an action.
## Key Functions
### 1. `check_emails()`
- Monitors the email inbox for new messages.
- Filters messages based on predefined criteria (e.g., specific sender).
- Downloads and processes attachments (e.g., PDF files).

### 2. `send_document_to_telegram(file_path)`
- Sends a local file (such as a PDF) to a Telegram channel using the bot API.

### 3. `send_msg_to_telegram_channel(message)`
- Sends a plaintext message directly to the Telegram channel.

### 4. `check_and_send()`
- Combines email monitoring and Telegram document/message sending.
- Ensures extracted files or messages from emails are delivered to Telegram.

### 5. `check_and_send_iperal()`
- A specialized implementation to fetch a document (PDF) from a predefined URL and send it to Telegram.

## Extending the System
The modularity of the project allows easy customization and modification for other purposes:
1. Integrate new sources like APIs or other websites.
2. Add support for different document formats (e.g., images, text files).
3. Enhance message parsing for more precise filtering or extraction.
4. Configure dynamic Telegram channels based on content.

## How to Set Up
### 1. Clone the Repository
``` bash
git clone <repository_url>
cd <repository_directory>
```
### 2. Install Dependencies
Use pip to ensure all necessary packages are installed:
``` bash
pip install requests
```
### 3. Configure Parameters
Replace the placeholder values in the script or environment variables with your specific information:
- Email server, email & password.
- Telegram bot token & channel ID.
- URL for PDF retrieval (if needed).

### 4. Run the Script
Execute the script using one of the CLI options depending on the mode of operation:
``` bash
python main.py --i
```
## Example Use Cases
1. **Weekly Menu Delivery**:
Automatically fetch weekly menus sent via email and share them in a workgroup Telegram channel.
2. **Report Distribution**:
Fetch reports or PDF documents from an external system or email, and automate their delivery to teams or stakeholders through Telegram.
3. **Promotional Notifications**:
Collect promotional material (e.g., brochures in PDF format) from emails or websites and distribute to Telegram followers.

## Notes and Recommendations
1. **Security**:
Ensure sensitive information (like email passwords or bot tokens) is stored securely, preferably in environment variables or a secure vault.
2. **Error Handling**:
Robust error handling is implemented, but be aware of dynamic content changes that may require updating filtering logic or configurations.
3. **IMAP Communication**:
Many email providers have disabled access using username and password, make sure to generate an app password to allow this program to work
