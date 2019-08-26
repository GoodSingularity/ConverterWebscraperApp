#!/bin/bash
if [ $# != 2 ]
then
	echo "Not equal"
else
	curl -X GET $1 > $2
	echo "Get page source"
	echo "Applying reg_expr"
	grep -Eo "([A-Z]\w+.)+(\w+|\w-[0-9]+.)\w+" < $2 |sort -u > "$2.out"
	rm $2
fi
