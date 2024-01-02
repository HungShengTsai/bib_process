# bib_process
This script abbreviates the journal names according to the built-in data file `journals.json` from [betterbib](https://github.com/nschloe/betterbib). This data file should satisfiy the requirements in most cases but users can customize the abbreviations in their own json file as well. In addition, it also capitalizes the title of citations. The entries of `@article` type citations are also checked. 

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
