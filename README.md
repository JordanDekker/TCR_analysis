# TCR repertoire analysis
  
## Description
Performs a TCR repertoire analysis using immunarch [https://immunarch.com/index.html] & VDJtools [https://vdjtools-doc.readthedocs.io/en/master/index.html].

As input you need output file from IMGT-High-V-Quest [http://www.imgt.org/HighV-QUEST/home.action] (only the IMGT-3NT-files). Put all files in a single directory with a `metadata.tsv` file. This metadata file should have the following format:
| file.name                                  |Sample  | Type     |col_name2  |...  |
|---------------------------------------------|--------|----------|-----------|-----|
| ~/Documents/your_dir/sample1_-3nt.txt       |sample1 | cHL      |Positive   |...  |
| ~/Documents/your_dir/sample2_-3nt.txt       |sample2 | cHL      |Negative   |...  |
| ~/Documents/your_dir/sample3_-3nt.txt       |sample3 | Reactive |Positive   |...  |
| ~/Documents/your_dir/sample4_-3nt.txt       |sample4 | Reactive |Negative   |...  |
| ...                                         |...     | ...      |...        |...  |

The first three columns are needed (file.name, Sample and Type). The metadata.tsv file can have as many different column names(EBV status, age(categorical), diagnosis type)

After the first run on IMGT-3NT-files, a new directory (/your_dirVDJtables/) is automatically made with VDJ count tables. Now you can run the analysis on the (new) directory with VDJ tables. 

## Installation 


### Prerequisites
* Linux
* Python
* Java Runtime Environment (JRE) v1.8
* R,  with packages immunarch (0.6.6) [https://immunarch.com/index.html] & Vegan (2.5-7) [https://cran.r-project.org/web/packages/vegan/index.html]

#### Set-up
1. `https://github.com/JordanDekker/TCR_analysis.git`
2. `sudo apt install cutadapt`
3. `pip install -r requirements/requirements.txt`

#### Usage

First a directory with VDJ table files or IMGT-3NT-files and one `metadata.tsv` file.

```bash
$ python app.py {options}
```
Options.

| Option         |default | description                                                                                                               |
|----------------|--------|---------------------------------------------------------------------------------------------------------------------------|
| -d --dir       |n/a     | Full path to the input directory (VDJ table files or IMGT-3NT-files)                                                      |
| -f --factor    |Type    | The factor you want to compare from the metadata file (e.g 'cHL' vs 'Reactive' or 'Positive' vs 'Negative')               |
| --TRB          |False   | Perform analysis only on the TRB genes                                                                                    |
| --TRG          |False   | Perform analysis only on the TRG genes                                                                                    |
| --productive   |False   | Perform analysis only on productive clonotypes (exclude non-productive)                                                   |

#### output
Output can be found in the /ouput folder.

## Examples

To run app.py with all the TRB and TRG combined
```bash
$ python app.py -d /home/name/Documents/dir_to_the_files 
```

To run app.py with only productive TRB clonotypes
```bash
$ python app.py -d /home/name/Documents/dir_to_the_files --TRB --productive
```

To run app.py with productive TRB and productive TRG seperate and compare the EBV status
```bash
$ python app.py -d /home/name/Documents/dir_to_the_files --TRB --productive -f EBV
```

## License

## Contact Information
*  Jordan Dekker - Jordandekker95@gmail.com
