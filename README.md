Birthdays
=========

A repo with some commands to import and combine scraped sources about people.

Install
-------

You can install all requirements in requirements.txt. 
On Caroline there is an alias to activate a virtual environment and go to the correct directory

```
start-bd
```

Database structure
------------------

There is a model called Person. A Person has a full_name and a birth_date. There is also a PersonSource.
A PersonSource describes information about somebody. 
If a source specifies a full_name and birth_date a Person is created or the source is added to a Person if a Person with the same
name and birth date exists. There is only one Person model. There are many "source" models that inherit from PersonSource.
Finally there is a GeneratedSource model. This is a PersonSource model who's instances are combinations of other PersonSources that together
supply a full_name and birth_date.

Import command
--------------

You can import data into instances of a model that inherits from PersonSource. You can import from a fixture or from a MySQL table.
Use ```python manage.py input from_fixture``` or ```python manage.py input from_mysql_table``` respectively.
With the -m flag it is possible to create a mapping between the input data and the data to be stored as a source (a model inheriting from PersonSource).
Data that is named or mapped to full_name, first_name, last_name, initials, prefix or birth_date will get stored directly on the source model.
All data that is named differently will end up under the props field which is a dictionary stored in a HStoreField.
For more details see ```python manage.py input -h```

Extend command
--------------

Once data is imported into a source the source can be used to create persons. You can use both 
```python manage.py extend add_to_master``` and ```python manage.py extend extend_master```. 
The commands will go through all data in the source. add_to_master will create new instances of Person when it finds a full_name and a birth_date in te source.
 extend_master will add additional sources to existing Person instances if it finds a Person with the same full_name as in the source.

Make file
---------

You can see a bunch of examples of how to import and create Person instances with described commands in the Makefile. 
Simply execute ```cat MakeFile``` to get a feel for what is possible. Do not execute these commands without thought. 
If you run a command twice it will double the amount of sources and/or double the amount of Persons without informing you.
It only makes sense to rerun a command if you have deleted all content of a source and the Persons created from that source.

Combine command
---------------

One command that I haven't been able to test on real sources is the combine command. The combine command aims to create possible new Persons from two sources.
A Person is defined as data that contains both a full_name and a birth_date. Sometimes only the combination of sources yields this results and combine will try to find such combinations in specified sources.
Currently never used, but I did provide some unit tests that prove that the code functions.

Next steps
----------

It would be very interesting to be able to split names based on Meertens Instituut data. Every PersonSource provides a split_full_name method, but by default it does nothing.
Splitting names will make it easier to combine information where only the last name and address is known (like with the phone book).
Using the Meertens Instituut data it will also be easier to split the pink and white pages of the phone book and get more reliable person data.
