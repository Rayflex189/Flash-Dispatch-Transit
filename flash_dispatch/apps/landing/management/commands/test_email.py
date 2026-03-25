from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime

class Command(BaseCommand):
    help = 'Test email configuration with Gmail'

    def handle(self, *args, **options):
        self.stdout.write('📧 Testing Gmail configuration...')
        
        try:
            # Test 1: Simple text email
            send_mail(
                'Test Email from Flash Dispatch',
                'This is a test email to verify your Gmail configuration.\n\nIf you received this, your email is working correctly!',
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('✅ Simple text email sent successfully!'))
            
            # Test 2: HTML email with template
            try:
                html_message = render_to_string('emails/auto_response.html', {
                    'name': 'Test User',
                    'subject': 'Email Configuration Test',
                    'date': datetime.now()
                })
                
                email = EmailMessage(
                    'HTML Test Email from Flash Dispatch',
                    html_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.EMAIL_HOST_USER]
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)
                
                self.stdout.write(self.style.SUCCESS('✅ HTML email with template sent successfully!'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠️ HTML email test failed: {e}'))
            
            self.stdout.write(self.style.SUCCESS('\n🎉 Email configuration is working properly!'))
            self.stdout.write(f'📧 Sent from: {settings.DEFAULT_FROM_EMAIL}')
            self.stdout.write(f'📧 Sent to: {settings.EMAIL_HOST_USER}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Email configuration error: {e}'))
            self.stdout.write('\n💡 Troubleshooting tips:')
            self.stdout.write('1. Enable "Less secure app access" or use App Password')
            self.stdout.write('2. Check if 2-Factor Authentication is enabled')
            self.stdout.write('3. Verify your email and password in .env file')
            self.stdout.write('4. Check if Gmail is blocking the sign-in attempt')
            self.stdout.write('5. Visit: https://myaccount.google.com/apppasswords')