#!/bin/bash

cd $(dirname $0)

echo -e "Possible citation files:"
# Using find to locate files with .bib extension and echo their filenames with line breaks
find $(dirname $0) -type f -name "*.bib" -exec basename {} \;

read -r -p "enter filename: " ini

ini=${ini//\\//} 

final=$ini"_converted"
final_err=$ini"_fail"

u_file="./data/customize_journal.json"
e_file="./data/exclude_word.txt"
r_file="./data/required_entry.txt"

cat $ini.bib | python3 citation_process.py -u $u_file -e $e_file -r $r_file > $final.bib 2> $final_err.bib

echo -e "New .bib file is saved as $final.bib."
# Check if the error log file is empty
if [[ -s "$final_err.bib" ]]; then
    echo -e "Entry-insufficient citations are saved in $final_err.bib."
else
    echo -e "All conversion successful."
    rm $final_err.bib
fi
