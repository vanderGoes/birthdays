from __future__ import unicode_literals, absolute_import, print_function, division

from django.test import TestCase

from birthdays.models import NBASource


class TestCombineCommand(TestCase):

    def test_nba_split_name(self):
        instance = NBASource()
        instance.full_name = "Spek, H. van der"
        instance.split_full_name()
        self.assertEqual(instance.initials, "H.")
        self.assertEqual(instance.prefix, "van der")
        self.assertEqual(instance.last_name, "Spek")
        instance = NBASource()
        instance.full_name = "Berkers, F.C."
        instance.split_full_name()
        self.assertEqual(instance.initials, "F.C.")
        self.assertEqual(instance.prefix, None)
        self.assertEqual(instance.last_name, "Berkers")
        instance = NBASource()
        instance.full_name = "Berkers"
        instance.split_full_name()
        self.assertEqual(instance.initials, None)
        self.assertEqual(instance.prefix, None)
        self.assertEqual(instance.last_name, None)
