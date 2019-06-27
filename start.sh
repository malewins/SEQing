#!/bin/bash

case $1 in
1)
echo "case " $1 ": Default case"
python validator.py annotations/Araport11_protein_coding.201606.bed annotations/Araport11_non_coding.2016016.bed  -bsraw annotations/8GFPLL36_unique.merged.xlsite.bedgraph annotations/8GFPLL24_unique.merged.xlsite.bedgraph -bsdata annotations/8GFPLL36_bsites.bed annotations/8GFPLL24_bsites.bed -desc annotations/ath_gene_descriptions.csv -seqs annotations/Araport11_protein_coding.201606.fa annotations/Araport11_non_coding.2016016.fa -colors 'rgb(46, 214, 26)' 'rgb(255, 87, 51)' -port ${2:-8060} -k 'lambda x : x[-2:]' 'True' -k 'lambda x : x[:1]' 'False' -config config_sample.cfg
;;
2)
echo "case " $1 ": Minimal case for testing"
python validator.py annotations/Araport11_protein_coding.201606.bed annotations/Araport11_non_coding.2016016.bed
;;
3)
echo "case " $1 ": Default colors"
python validator.py annotations/Araport11_protein_coding.201606.bed annotations/Araport11_non_coding.2016016.bed  -bsraw annotations/8GFPLL36_unique.merged.xlsite.bedgraph annotations/8GFPLL24_unique.merged.xlsite.bedgraph -bsdata annotations/8GFPLL36_bsites.bed annotations/8GFPLL24_bsites.bed -desc annotations/ath_gene_descriptions.csv -seqs annotations/Araport11_protein_coding.201606.fa annotations/Araport11_non_coding.2016016.fa -port ${2:-8060} -k 'lambda x : x[-2:]' 'True' -k 'lambda x : x[:1]'
;;
4)
echo "case " $1 ": Only gene annotations"
python validator.py annotations/Araport11_protein_coding.201606.bed -port ${2:-8060}
;;
5)
echo "case " $1 ": Only gene annotations and 4 raw data"
python validator.py annotations/Araport11_protein_coding.201606.bed annotations/Araport11_non_coding.2016016.bed  -bsraw annotations/8GFPLL36_unique.merged.xlsite.bedgraph annotations/8GFPLL24_unique.merged.xlsite.bedgraph annotations/7GFPLL36_unique.merged.xlsite.bedgraph annotations/7GFPLL24_unique.merged.xlsite.bedgraph -port ${2:-8060} -desc annotations/ath_gene_descriptions.csv
;;
6)
echo "case " $1 ": only signficant bs data"
python validator.py annotations/Araport11_protein_coding.201606.bed annotations/Araport11_non_coding.2016016.bed -bsdata annotations/8GFPLL36_bsites.bed annotations/8GFPLL24_bsites.bed -desc annotations/ath_gene_descriptions.csv -seqs annotations/Araport11_protein_coding.201606.fa annotations/Araport11_non_coding.2016016.fa -port ${2:-8060}
;;
7)
echo "case " $1 ": No data sets"
python validator.py annotations/Araport11_protein_coding.201606.bed annotations/Araport11_non_coding.2016016.bed -desc annotations/ath_gene_descriptions.csv -seqs annotations/Araport11_protein_coding.201606.fa annotations/Araport11_non_coding.2016016.fa -port ${2:-8060}
;;
8)
echo "case " $1 ": Colors and names but no data sets"
python validator.py annotations/Araport11_protein_coding.201606.bed annotations/Araport11_non_coding.2016016.bed -desc annotations/ath_gene_descriptions.csv -seqs annotations/Araport11_protein_coding.201606.fa annotations/Araport11_non_coding.2016016.fa -colors 'rgb(46, 214, 26)' 'rgb(255, 87, 51)' -port ${2:-8060}
;;
9)
echo "case " $1 ": no data sets, no descriptions, nonexisting gene annotation file"
python validator.py annotations/Araport11_protein_coding.201606.bed annotations/Araport11_non_coding.2016016.bed ddfd.bed ddd.gtf -seqs annotations/Araport11_protein_coding.201606.fa annotations/Araport11_non_coding.2016016.fa -colors 'rgb(46, 214, 26)' 'rgb(255, 87, 51)' -port ${2:-8060}
;;
10)
echo "case " $1 ": no gene annotations, should not start at all"
python validator.py -bsraw annotations/8GFPLL36_unique.merged.xlsite.bedgraph annotations/8GFPLL24_unique.merged.xlsite.bedgraph -bsdata annotations/8GFPLL36_bsites.bed annotations/8GFPLL24_bsites.bed -desc annotations/ath_gene_descriptions.csv -seqs annotations/Araport11_protein_coding.201606.fa annotations/Araport11_non_coding.2016016.fa -colors 'rgb(46, 214, 26)' 'rgb(255, 87, 51)' -port ${2:-8060}
;;
11)
echo "case " $1 ": Test with gtf files"
python validator.py annotations/Araport11_GFF3_genes_transposons.201606.gtf -bsraw annotations/8GFPLL36_unique.merged.xlsite.bedgraph annotations/8GFPLL24_unique.merged.xlsite.bedgraph -bsdata annotations/8GFPLL36_bsites.bed annotations/8GFPLL24_bsites.bed -desc annotations/ath_gene_descriptions.csv -seqs annotations/Araport11_protein_coding.201606.fa annotations/Araport11_non_coding.2016016.fa -colors 'rgb(46, 214, 26)' 'rgb(255, 87, 51)' -port ${2:-8060}
;;
12)
echo "case " $1 ": Test with human gtf file"
python validator.py annotations/Homo_sapiens.GRCh38.96.chr.gtf  -bsraw annotations/8GFPLL36_unique.merged.xlsite.bedgraph annotations/8GFPLL24_unique.merged.xlsite.bedgraph -bsdata annotations/8GFPLL36_bsites.bed annotations/8GFPLL24_bsites.bed -desc annotations/ath_gene_descriptions.csv -seqs annotations/Araport11_protein_coding.201606.fa annotations/Araport11_non_coding.2016016.fa -colors 'rgb(46, 214, 26)' 'rgb(255, 87, 51)' -port ${2:-8060}
;;
13)
echo "case " $1 ": Test with different organism gtfs"
python validator.py annotations/Araport11_GFF3_genes_transposons.201606.gtf -bsraw annotations/8GFPLL36_unique.merged.xlsite.bedgraph annotations/8GFPLL24_unique.merged.xlsite.bedgraph -bsdata annotations/8GFPLL36_bsites.bed annotations/8GFPLL24_bsites.bed -seqs annotations/Araport11_protein_coding.201606.fa annotations/Araport11_non_coding.2016016.fa -desc annotations/ath_gene_descriptions.csv -colors 'rgb(46, 214, 26)' 'rgb(255, 87, 51)' -port ${2:-8060}
;;
14)
echo "case " $1 ": Test with different organism gtfs"
python validator.py annotations/Araport11_GFF3_genes_transposons.201606.gtf -bsraw annotations/8GFPLL36_unique.merged.xlsite.bedgraph annotations/8GFPLL24_unique.merged.xlsite.bedgraph -bsdata annotations/8GFPLL36_bsites.bed annotations/8GFPLL24_bsites.bed -seqs annotations/Araport11_protein_coding.201606.fa annotations/Araport11_non_coding.2016016.fa -desc annotations/ath_gene_descriptions.csv -colors 'rgb(46, 214, 26)' 'rgb(255, 87, 51)' -port ${2:-8060}
;;
15)
echo "case " $1 ": Default case with the splicing feature"
python validator.py annotations/Araport11_protein_coding.201606.bed annotations/Araport11_non_coding.2016016.bed  -bsraw annotations/8GFPLL36_unique.merged.xlsite.bedgraph annotations/8GFPLL24_unique.merged.xlsite.bedgraph -bsdata annotations/8GFPLL36_bsites.bed annotations/8GFPLL24_bsites.bed -desc annotations/ath_gene_descriptions.csv -seqs annotations/Araport11_protein_coding.201606.fa annotations/Araport11_non_coding.2016016.fa -colors 'rgb(46, 214, 26)' 'rgb(255, 87, 51)' -port ${2:-8060} -k 'lambda x : x[-2:]' 'True' -k 'lambda x : x[:1]' 'False' -splice_data \
../LL18_bedgraphs/9.91_LL18.bedgraph ../LL18_bedgraphs/Col21_LL18.bedgraph ../LL18_bedgraphs/D1c1_LL18.bedgraph
;;
esac
