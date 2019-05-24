![SEQing logo](Seqing.png)
# SEQing [seeking]
Plotly - Dash: interactive web-based tool for visualization of iCLIP-seq and RNA-seq data.
# Project Title

The goal of this project is to develop a generalized, web based, interactive visualisation and exploration tool for iCLP and rna_seq data. The idea is to have a single running inside a groups network, allowing members to access and explore their experimental data with only a web browser and no local installations needed. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The file [requirenments.txt] (requirenments.txt) can be used to install all needed needed dependencies for the project. Python 3.5 or higher is requried, it is recommend you setup a virtual environment for this project.

Once you have setup your virtual environment run the following code to install the dependencies:
```
pip install -r requirenments.txt
```

### Installing


## Deployment

### Minimal startup

Once you have activated your virtual env you can perform a minimal startup of the tool with the following command:
```
python validator.py some_gene_annotation_file
```
Note that some_gene_annotation_file is either a bed12 or gtf file containing gene annotations for the organism of your choice. You can also provide mroe than one file. Please ensure that all files have the correct file extension and do NOT have a header line.

If everything works you should be able to connect to the dashboard via your browser and select genes from the dropsown to display their associated gene models.

### Adding iCLIP and binding site data

One of the key features of this tool is the interactive visualisation of raw iCLIp data. This data should be passed in the form of 4 column bedgraph files. Example:
```
python validator.py some_gene_annotation_file -bsraw prefix_your_iCLIP_data_file
```
The program will automatically treat everything before the first underscore in the filename as a prefix. This prefix will be used to match a raw iCLIP file to a corresponding binding site file, if provided. An example:
```
python validator.py some_gene_annotation_file -bsraw prefix_your_iCLIP_data_file -bsdata prefix_your_binding_site_data_file
```
These files should be 6 column bed files. The two files with the same prefix will be treated as a dataset b the tool and their graphs will be grouped together. Please note that a data set consists of maximal two files, it must have a raw iCLIP file and may have a binding site file. You can have multiple datasets, just pass multiple files to the command line options, seperated by spaces.

### Displaying descriptions and sequences

Apart from visualising iCLIP and binding site information the program can also show gene descriptions:
```
python validator.py some_gene_annotation_file -desc description_file
```
Here description_file should be a tab seperated csv file containing the following columns and header:
```
ensembl_gene_id	description	external_gene_name	gene_biotype
``` 
For this option the program only takes a single file.

You can also provide dna sequences in fasta format for visualisation:
```
python validator.py some_gene_annotation_file -seqs sequence_file
```
There are a few limitations:
* The fields in the desriptions of the fasta entries should either be seperated by a space or colon, with the first field being the gene name:
```
>ENST00000631435.1 cds chromosome:GRCh38:CHR_HSCHR7_2_CTG6:142847306:142847317:1 gene:ENSG00000282253.1 gene_biotype:TR_D_gene

>AT1G03993.1::Chr1:23311-24099
```
* Your sequences have to cover the whole region of the genes as defined in the gene annotations. The program will automatically construct a master sequence if mutliple isoforms of the gene are provided, but the individual isoform sequences have to be continuous.

### Colors

The current default color palette consists of four colors. Colors will be reused should more than four datasets be provided. You can provide your own colors usig a command similar to the following:
```
python validator.py some_gene_annotation_file -colors 'rgb(46, 214, 26)' 'rgb(255, 87, 51)'
```
You can provide how many colors you need, they will be associated to datasets based on the order they are provided.

###Sorting

Should you have multiple datasets you might want to take a look at the option to provide expressions for sorting. Graphs for datasets can be toggled on and off in the visualisation. Depending on the way the user does this, the order in which datasets are displayed may change. Therefore the graphs are sorted by default in ascending order using the prefix. However you might have a need for more complex soting, like the following example:
```
python validator.py some_gene_annotation_file -bsraw 8pref26_iCLIP 8pref30_iCLIP -k 'lambda x : x[-2:]' 'True' -k 'lambda x : x[:1]' 'False'
```
Take note of the -k option. It allows you to provide arguments for the list.sort function of python. In this case we provide 2 different sets of arguments, the first sorts the prefixes by the last two characters, descending and the second sorts them by the first character, in ascending order. Each -k has to be followed by a string containing the desired lambda expression and a bool telling the program wether to revert the order(default is ascneding).
## Built With

## Contributing


## Versioning


## Authors


## License


## Acknowledgments

