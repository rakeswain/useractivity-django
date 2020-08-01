# This file contains addactivty command
# The command can be used to add the start time and end time of actives of a user
#
# Usage: manage.py addactivity [-h] -uid USERID -s STARTTIME -e ENDTIME
#                              [-tz TIMEZONE] [--version] [-v {0,1,2,3}]
#                              [--settings SETTINGS] [--pythonpath PYTHONPATH]
#                              [--traceback] [--no-color] [--force-color]
#                              [--skip-checks]
#
# Format for start time and end time - YYYY-MM-DD.HH:MM
#
# example :  $ python manage.py -uid abc -s 2020-12-12.10:30 -e 2020-12-12.10:30

from userapi.models import ActivityPeriod, User
from django.core.management.base import BaseCommand, CommandError
import datetime
import pytz


def valid_date(s):
    """
        Checks if the given datetime string matches the required format , if yes then returns the datetime object
        else raises CommandError : Not valid date time string
    """
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d.%H:%M")
    except ValueError:
        msg = f"Not a valid date time string : '{s}'"
        raise CommandError(msg)


class Command(BaseCommand):
    """ Takes the arguments from command line , parses  and handles them"""
    help = 'Used to update user activity'

    def add_arguments(self, parser):
        """ Used for parsing the arguments. """

        parser.add_argument('-uid', '--userid', type=str, help='Define a user id', required=True)
        parser.add_argument("-s",
                            "--starttime",
                            help="Format for start time - YYYY-MM-DD.HH:MM",
                            required=True,
                            type=valid_date)
        parser.add_argument("-e",
                            "--endtime",
                            help="Format for end time - YYYY-MM-DD.HH:MM",
                            required=True,
                            type=valid_date)

    def handle(self, *args, **options):
        """ Used for handling the arguments. """

        start_time = options['starttime']
        end_time = options['endtime']
        user_id = options['userid']

        # Checks if user exists
        try:
            user = User.objects.get(id=user_id) or None
        except User.DoesNotExist:
            raise CommandError(f"User {user_id} doesnt exist")

        # replacing the timezone of start_time with user's timezone
        start_time = start_time.replace(tzinfo=pytz.timezone(user.tz))
        # replacing the timezone of end_time with user's timezone
        end_time = end_time.replace(tzinfo=pytz.timezone(user.tz))

        created = ActivityPeriod.objects.create(user=user, start_time=start_time, end_time=end_time)

        if created is not None:
            self.stdout.write(self.style.SUCCESS(f'User {user_id} created successfully'))
        else:
            raise CommandError(f"Activity period could not created")
