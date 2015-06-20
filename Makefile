import-wiki:
	python ./manage.py input from_fixture -f ../data/wiki.json -s WikiSource -m "naam=full_name&geboortedatum=birth_date" -a

import-telephone:
	python ./manage.py input from_mysql_table -f telefoonBoekGemeente -s PhoneBookSource -m "gemeente=district&lastname=last_name" 
