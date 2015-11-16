from __future__ import unicode_literals, absolute_import, print_function, division
# noinspection PyUnresolvedReferences
from six.moves.urllib.parse import parse_qsl

import argparse
from time import strptime
from datetime import datetime


class DecodeQueryAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        values = dict(parse_qsl(values))
        setattr(namespace, self.dest, values)


def parse_dutch_date(date_input):
    return datetime.strptime(date_input, "%d-%m-%Y")
