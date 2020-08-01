from django.db import models


class User(models.Model):
    """ User model class to store user id, real name , timezone."""
    # Every user record must have a id which acts as a primary key and is unique
    # Real name is optional and can be updated later
    # If time zone is not given by the user then it is set to UTC.

    id = models.CharField(max_length=100, primary_key=True, null=False)
    real_name = models.CharField(max_length=100)
    tz = models.CharField(max_length=50)

    def __str__(self):
        return f"User ID : {self.id} | Real Name : {self.real_name}"


class ActivityPeriod(models.Model):
    """
    ActivityPeriod model class to store start time and end time of different activities of each user.
    """
    # ActivityPeriod is in one to many relationship with User.
    # i.e. One user can be related with many ActivityPeriod records.

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_period')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    def __str__(self):
        return f"User ID : {self.id} | Start Time : {self.start_time} - End Time : {self.end_time}"
