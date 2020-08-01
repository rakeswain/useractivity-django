# This file contains populatedb command
# The command can be used to add or update a user
#
# Usage: manage.py populatedb [-h] [-uid USERID] [-fn FIRSTNAME] [-ln LASTNAME]
#                            [-tz TIMEZONE] [--version] [-v {0,1,2,3}]
#                            [--settings SETTINGS] [--pythonpath PYTHONPATH]
#                            [--traceback] [--no-color] [--force-color]
#                            [--skip-checks]
#
#
# example :  $ python manage.py -uid abc -fn John -ln Doe -tz Asia/Kolkata

from userapi.models import User
from django.core.management.base import BaseCommand, CommandError
import pytz


def validate_timezone(s):
    """ Used to validate the given timezone input. """
    try:
        return pytz.timezone(s)
    except pytz.UnknownTimeZoneError:
        msg = f"Not a valid timezone : '{s}'"
        raise CommandError(msg)


class Command(BaseCommand):
    """ Takes the arguments from command line , parses  and handles them. """
    help = 'Used to populate the database.'

    def add_arguments(self, parser):
        """ Used for parsing the arguments. """
        parser.add_argument('-uid', '--userid', type=str, help='Define a user id', required=True)
        parser.add_argument('-fn', '--firstname', type=str, help='Define a user name')
        parser.add_argument('-ln', '--lastname', type=str, help='Define a user name')
        parser.add_argument('-tz', '--timezone', help='Define a time zone', type=validate_timezone)

    def handle(self, *args, **options):
        """ Used for handling the arguments. """

        user_id = options['userid'].upper()

        # If first name is given the uses it or uses an empty string
        if options['firstname'] is not None:
            first_name = options['firstname']
        else:
            first_name = ""
        # If last name is given the uses it or uses an empty string
        if options['lastname'] is not None:
            last_name = options['lastname']
        else:
            last_name = ""
        username = first_name + ' ' + last_name
        # If timezone is given then takes it or uses default timezone as UTC
        if options['timezone'] is not None:
            timezone = options['timezone']
        else:
            timezone = "UTC"

        u, created = User.objects.get_or_create(id=user_id, real_name=username, tz=timezone)
        # If user is created prints success or raises an error
        if created:
            self.stdout.write(self.style.SUCCESS(f'User {user_id} created successfully'))
        elif u:
            self.stdout.write(self.style.ERROR(f'ERROR : User {user_id} already exists'))
