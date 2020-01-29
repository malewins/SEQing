import filetype as ft
import pandas as pd
import numpy as np
import gzip
import zipfile
import bz2


class FileInput:
    """Decorator for file checking"""
    def __init__(self, file_path, file_type, zipped, header_present):
        self.file_path = file_path
        self.file_type = file_type
        self.zipped = zipped
        self.header_present = header_present


def check_input_file(file_path):
    """A function to test the input file and classifies it by content"""
    # try to guess file type by analysing the head
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
        return FileInput(file_path, 'unsupported', False, False)

    head_dtypes = np.array(file_head.dtypes)
    # check for header (no numbers in first row)
    header_present = not any(cell == np.int for cell in head_dtypes)

    header = pd.Series()
    if header_present:
        header = file_head.iloc[0]
        if file_zipped:
            file_head = pd.read_csv(file_path, compression='infer', sep='\t', header=None, nrows=5, skiprows=1, comment='#')
        else:
            file_head = pd.read_csv(file_path, sep='\t', header=None, nrows=5, skiprows=1, comment='#')

    # assign file type by shape of table
    head_dim = file_head.shape
    # check for BED4
    if head_dim[1] == 4:
        return FileInput(file_path, 'BED4', file_zipped, header_present)
    # check for BED6
    elif head_dim[1] == 6:
        return FileInput(file_path, 'BED4', file_zipped, header_present)
    # check for GFF or GTF
    elif head_dim[1] == 9:

        if not header.empty:
            for col in header:
                if 'gff-version 3' in col:
                    return FileInput(file_path, 'GFF3', file_zipped, header_present)
                else:
                    return FileInput(file_path, 'GTF', file_zipped, header_present)

    elif head_dim[1] == 12:
        return FileInput(file_path, 'BED12', file_zipped, header_present)
    else:
        # unsupported format
        return FileInput(file_path, 'unsupported', False, header_present)



