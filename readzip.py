import filetype as ft
import pandas as pd
import numpy as np
import gzip
import zipfile
import bz2


class FileInput:
    """Decorator for file checking"""

    def __init__(self, file_path, file_type, zipped):
        self.file_path = file_path
        self.file_type = file_type
        self.zipped = zipped


def check_input_file(file_path):
    """A function to test the input file and classifies it by content"""
    # try to guess file type by head
    guessed_type = ft.guess(file_path)
    file_zipped = False

    if guessed_type == None:
        # read uncompressed head
        file_head = pd.read_csv(file_path, sep='\t', header=None, nrows=5)

    elif guessed_type.mime in ['application/gzip', 'application/x-bzip2', 'application/zip']:
        # read compressed head
        file_head = pd.read_csv(file_path, compression='infer', sep='\t', header=None, nrows=5)
        file_zipped = True
    else:
        # return unsupported file type
        return FileInput(file_path, 'unsupported', False)

    head_dim = file_head.shape
    head_dtypes = np.array(file_head.dtypes)

    print(head_dtypes == [object, np.int64, np.int64, np.int64])
    print(head_dtypes == [object, np.int64, np.int64, np.float64])

    # check for BED4
    if head_dim[1] == 4:
        return FileInput(file_path, 'BED4', file_zipped)
    # check for BED6
    elif head_dim[1] == 6:
        return FileInput(file_path, 'BED4', file_zipped)
    # check for GFF or GTF
    elif head_dim[1] == 9:
        return FileInput(file_path, 'GFF/GTF', file_zipped)
    elif head_dim[1] == 12:
        return FileInput(file_path, 'BED12', file_zipped)
    else:
        # unsupported format
        return FileInput(file_path, 'unsupported', False)


readfiles = ['example_set/AtGRP7-ox_LL36.bedgraph',  # uncompressed
             'example_set/AtGRP7-ox_LL36.bedgraph.gz',  # gzipped
             'example_set/AtGRP7-ox_LL36.bedgraph.zip',  # zipped
             'example_set/AtGRP7-ox_LL36.bedgraph.bz2'  # gzipped
             ]

for file in readfiles:
    print(vars(check_input_file(file)))

'''

for file_to_read in readfiles:
    guessed_type = ft.guess(file_to_read)
    # None equals regular text files
    if guessed_type == None:
        #read with pandas
        print("Filetype of {f2r} is: {type}".format(type=guessed_type, f2r=file_to_read))
        data_file = pd.read_csv(file_to_read,sep='\t',header=None, nrows=4)
        print(data_file.head())
    elif guessed_type.mime in ['application/gzip', 'application/x-bzip2', 'application/zip']:
        # read with pandas and zip option
        print("Filetype of {f2r} is: {type}".format(type=guessed_type.mime, f2r=file_to_read))
        data_file = pd.read_csv(file_to_read, compression='infer',sep='\t',header=None,nrows=4)
        print(data_file.head())
'''
