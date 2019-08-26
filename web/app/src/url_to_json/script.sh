#!/bin/bash
if [ $# != 3 ]
then
	echo "Not equal"
else
	touch $2
	curl -X GET $1 > "$2"
	echo "Get page source"
	echo "Applying reg_expr"
	grep -Eo "$3" < $2 | sort -u > "/app/src/url_to_json/$2.out"
	rm $2
fi
