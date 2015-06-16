from __future__ import unicode_literals, absolute_import, print_function, division
# noinspection PyUnresolvedReferences
from six.moves.urllib.parse import parse_qsl

import argparse


class DecodeMappingAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        values = dict(parse_qsl(values))
        setattr(namespace, self.dest, values)