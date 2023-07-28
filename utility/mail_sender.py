"""Module for sending mails
"""
import smtplib


class MailSender:
    """Class to send email"""

    def __init__(self, smtp_host, smtp_port, sender_mail, sender_pw):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender_mail = sender_mail
        self.sender_pw = sender_pw

    def send(self, receiver, subject, content):
        """Send email to one receiver"""
        message = f'From: { self.sender_mail}\r\nTo: {receiver}\r\nSubject: {subject}\r\n\r\n'

        message += content
        # print(message)
        try:
            smtp_obj = smtplib.SMTP(self.smtp_host, self.smtp_port)
            smtp_obj.ehlo()
            smtp_obj.starttls()
            smtp_obj.ehlo()
            smtp_obj.login(self.sender_mail, self.sender_pw)
            smtp_obj.sendmail(self.sender_mail, receiver, message)
            smtp_obj.quit()
            # print("Successfully sent email")
            return True
        except smtplib.SMTPException:
            print("Error: unable to send email")

        return False

    def send_to_all_receivers(self):
        """To be implemented"""
        return False


if __name__ == "__main__":
    mail_sender = MailSender('smtp.office365.com', 587,
                             'yang.yu72@outlook.com', "Wilson@1989")
    mail_sender.send("yywilson@hotmail.com", "new test",
                     "hello, this is a test")
