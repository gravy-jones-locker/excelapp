import smtplib
import config
import traceback as tb
from email.mime.text import MIMEText

class ConversionError(Exception):
    pass

def handle_error(exception):

    """Parse exception thrown and process accordingly"""

    print(tb.format_exc())

    if type(exception) == ConversionError:
        return 201
    
    else:  # For any non-conversion errors return code 202
        
        notify_error_generic()
        return 202

def notify_error_generic():

    """Notify recipient of non-conversion (network) error"""

    subj = 'Disney xls conversion network error'
    msg = '''
    
    A network/non-conversion error was just tripped while using the
    disney xls conversion tool.'''

    send_email(subj, msg)

def notify_error_conversion(fname):

    """Notify recipient of conversion error while processing xls"""

    subj = 'Disney xls conversion error ATTENTION REQUIRED'

    msg = f'''

    A conversion error was just tripped while using the disney xls
    conversion tool.
    <br><br>
    The input file can be downloaded here:
    <br><br>
    {config.HOST_IP}/static/input/{fname}'''

    send_email(subj, msg)

def send_email(subj, msg):

    """Send an email with details of a recent notification (error)"""

    port = 465    
    user = config.EMAIL_SENDER

    msg = MIMEText(msg, 'html')
    msg['Subject'] = subj

    msg['From'] = config.EMAIL_SENDER

    with smtplib.SMTP_SSL(f'smtp.{user.split("@")[1]}', port) as session:
        
        session.login(user, config.EMAIL_PWORD)
        session.sendmail(user, [config.EMAIL_RECIPIENT], msg.as_string())

    

