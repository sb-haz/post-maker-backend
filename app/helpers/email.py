'''
Imports
'''
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import os

from credentials import email_credentials as credentials


'''
Path to root directory
'''
ABSOLUTE_PATH = ""
ABSOLUTE_PATH_MEDIA = "resources/"


'''
Email credentials
'''
EMAIL_ADDRESS = credentials.email_address
EMAIL_PASSWORD = credentials.email_password


'''
Send email
'''
def send_email_with_attachment(user_email, username, tweet_id, tweet_author, filepath):
    
    # Convert to string
    tweet_id = str(tweet_id)
    
    # Email message
    msg = EmailMessage()
    msg["Subject"] = f"Your video is ready! ✅ #{tweet_id}"
    msg['From'] = formataddr(('Post Maker', EMAIL_ADDRESS))
    msg["To"] = user_email

    msg.set_content(f"Hey {username}, your video is ready! 🎉\n\nCaption:\n😂😂😂 (Twitter @ {tweet_author})\n\nOriginal Tweet: \nTwitter.com/t/status/{tweet_id}\n\n")

    # Add attachment
    with open(filepath, 'rb') as attachment:
        
        # File name
        file_name = os.path.basename(attachment.name)
        
        # Get file data
        file_data = attachment.read()
        
        # Set file type
        file_type = "video"
    
    # Attach to message
    msg.add_attachment(file_data, maintype=file_type, subtype=file_type, filename=file_name)

    # Login and send email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:   
            
            # Login
            try:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            except Exception as e:
                print(e)
            
            # Send email
            try:
                smtp.send_message(msg)
                print(f"Email sent to {user_email}")
            except Exception as e:
                print(e)
                
    except Exception as e:
        print(e)
        
    return True