from django.db import models


class Country(models.Model):
    """Country model"""
    # country code
    sortname = models.CharField(max_length=3)
    name = models.CharField(max_length=150)
    phonecode = models.IntegerField()

    def __str__(self):
        return "{}".format(self.name)


class State(models.Model):
    """State model"""
    name = models.CharField(max_length=30)
    # страна,к которой принадлежит область\штат
    # list(tuples,) tuple=(id in list,'afkorting','fulle name','code')
    # (155, 'NL', 'Netherlands The', 31),
    country_id = models.IntegerField()

    def __str__(self):
        return "{}".format(self.name)


class City(models.Model):
    """City"""
    name = models.CharField(max_length=30)
    state_id = models.IntegerField()

    def __str__(self):
        return "{}".format(self.name)
