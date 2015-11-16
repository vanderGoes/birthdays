from __future__ import unicode_literals, absolute_import, print_function, division
import six


def output_person(person):
    basic_info = [
        person.initials if person.initials else "",
        person.first_name if person.first_name else "",
        person.prefix if person.prefix else "",
        person.last_name if person.last_name else "",
        person.full_name if person.full_name else "",
        person.birth_date.strftime("%d-%m-%Y") if person.birth_date else ""
    ]
    extra_info = [
        "{} -> {}".format(key, value) for key, value in six.iteritems(person.props)
    ]
    print("Basic info:", ", ".join(basic_info))
    print("Extra info:", ", ".join(extra_info))
    print("Source info:", ", ".join([source.__class__.__name__ for source in person.sources.all()]))
    print()