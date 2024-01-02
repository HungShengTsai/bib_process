# bib_process
There are some bibtex tools out there to help abbreviate journal names. However, I found that those packages are often over-complicated with many functions and require extra dependencies which sometimes break in my early trial due to lack of maintenance. For the sole purpose of abbreviating journal names, this script provides a lightweight way to transform your latex bib file without extra dependencies. This script abbreviates the journal names according to the built-in data file `journals.json` from [betterbib](https://github.com/nschloe/betterbib). This data file should satisfiy the requirements in most cases but users can customize the abbreviations in their own json file as well. 

## Usage

```bash
./run_citation_process.sh
```

Several possible citation files in the same directory will be recommended.
Next, please input the `.bib` filename to process
```bash
enter filename: bib_filename
```

If all the citations are processed correctly, you will see
```bash
All conversion successful.
```
Otherwise, some citations with missing entries will be collected in a separate `.bib` file with `_fail.bib` filename.

Users can specify their own extra abbreviation rules through customized json file with additionl argument to the python script as `--user-json` (refer to `./data/customize_journal.json` for an example). The customized abbreviation rules would override the default one in the case of conflict. 

For certain words that do not need capitalization in a title, please add them into the `.txt` file 
at `./data/exclude_word.txt`.

Required entries for a typical `@article` citation can be specified in the `./data/required_entry.txt` file.

## Acknowledgement
This development is motivated by Junxian He.
Part of the code regarding journal abbreviations is adopted from [bib-journal-abbreviation](https://github.com/jxhe/bib-journal-abbreviation.git).
