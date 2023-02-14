from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags

from ..models import Instructor


def sendPrefrncesEmail():
    instructor = Instructor.objects.first()
    message = 'Dear ' + instructor.name + ',\n\n' + 'Please fill your preferences in the following link:\n\n' + 'http://localhost:3000/instructor/' + instructor.secret_token + '\n\n' + 'Best Regards,\n'
    html_message = '<p>Dear ' + instructor.name + ',</p><p>Please fill your preferences in the following link:</p><p><a href="http://localhost:3000/instructor/' + instructor.secret_token + '">http://localhost:3000/instructor/' + instructor.secret_token + '</a></p><p>Best Regards,</p>'
    send_mail('Please fill your preferences', strip_tags(html_message), settings.EMAIL_HOST_USER, ['ahmedalghamdi2000@hotmail.com'], fail_silently=False, html_message=html_message)

    # instructors = Instructor.objects.all()
    # for instructor in instructors:
    #     message = 'Dear ' + instructor.name + ',\n\n' + 'Please fill your preferences in the following link:\n\n' + 'http://localhost:3000/instructor/' + instructor.secret_token + '\n\n' + 'Best Regards,\n'
    #     html_message = '<p>Dear ' + instructor.name + ',</p><p>Please fill your preferences in the following link:</p><p><a href="http://localhost:3000/instructor/' + instructor.secret_token + '">http://localhost:3000/instructor/' + instructor.secret_token + '</a></p><p>Best Regards,</p>'
    #     send_mail('Please fill your preferences', strip_tags(html_message), settings.EMAIL_HOST_USER, [instructor.university_id + '@uj.edu.sa'], fail_silently=False, html_message=html_message)
