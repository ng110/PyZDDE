from __future__ import print_function
import os as os
from struct import unpack #, pack 
import pyzdde.zfileutils as zfile
#import ctypes as _ctypes

testdir = os.path.dirname(os.path.realpath(__file__))

def get_full_path(filename):
    """returns the full path name.
    Assumption: the files are in the same directory as this file
    """
    return os.path.join(testdir, filename)


def read_n_bytes(fileHandle, formatChar):
    """read n bytes from file. The number of bytes read is specified by the
    ``formatChar``
    
    fileHandle : file handle
    formatChar : 'c' (1), 'h' (2), 'i' (4), 'd' (8), 'f' (4)
    """
    nbytes = None    
    bytes2read = {'c':1, 'h':2, 'i':4, 'd':8, 'f':4}    
    packedBytes = fileHandle.read(bytes2read[formatChar])
    if packedBytes:
        nbytes = unpack(formatChar, packedBytes)[0] 
    return nbytes
    
    
def compare_files_nbytes(filename1, filename2, formatChar):
    """compare byte chunks in files ``filename1`` and ``filename2`` from beginning
    to end. The chunks size is determined by ``formatChar`` 
    """
    #FIXME!!! function doesn't work for formatChar = 'h'
    format_size = {'c':1, 'h':2, 'i':4, 'd':8, 'f':4}
    retVal = False
    i = 0    
    with open(filename1, 'rb') as f1, open(filename2, 'rb') as f2:
        while True:
            nbytes_f1 = read_n_bytes(f1, formatChar)
            nbytes_f2 = read_n_bytes(f2, formatChar)
            if nbytes_f1 and nbytes_f2:
                assert nbytes_f1 == nbytes_f2, \
                ("{} in file1 mismatached with {} in file 2 at byte offset {}."
                .format(nbytes_f1, nbytes_f2, i*format_size[formatChar]))
                i += 1
            elif nbytes_f1 and not nbytes_f2:
                print("Incomplete comparison as file1 ended. Matched upto {} bytes"
                      .format(i*format_size[formatChar]))
                break;
            elif not nbytes_f1 and nbytes_f2:
                print("Incomplete comparison as file2 ended. Matched upto {} bytes"
                      .format(i*format_size[formatChar]))
                break;
            else:
                print("Files match")
                retVal = True
                break;
    return retVal
    

   
def test_zrdfileutils():
    """test the zrdfileutils functions
    """
    # Test the functions on uncompressed ZRD files
    zrd_filename = 'Color_Fringes_TenRays_NoSplit.ZRD' # 'TESTRAYS.ZRD'
    zrd_data_0 = zfile.readZRDFile(get_full_path(zrd_filename), 'uncompressed')
    #print(zrd_data_0[0])
    #zfile.writeZRDFile(a, 'TESTRAYS_uncompressed.ZRD','uncompressed')
    zrd_filename_to_write = 'uncompressed_write.ZRD'
    zfile.writeZRDFile(zrd_data_0, get_full_path(zrd_filename_to_write), 'uncompressed')
    #b = zfile.readZRDFile('TESTRAYS_uncompressed.ZRD','uncompressed')
    zrd_data_1 = zfile.readZRDFile(get_full_path(zrd_filename_to_write),'uncompressed')
    
    # Compare the written file to the read file
    assert len(zrd_data_0) == len(zrd_data_1)
    assert zrd_data_0[0].version == zrd_data_1[0].version
    assert zrd_data_0[0].n_segments == zrd_data_1[0].n_segments
    compare_files_nbytes(get_full_path(zrd_filename), get_full_path(zrd_filename_to_write), 'i')
     
    # Test of compressed file read/write
    #zfile.writeZRDFile(a, 'TESTRAYS_compressed.ZRD','compressed')
    #c = zfile.readZRDFile('TESTRAYS_compressed.ZRD','compressed')
    print("DONE")


if __name__ == '__main__':
    test_zrdfileutils()
    #zrd_filename = 'Color_Fringes_TenRays_NoSplit.ZRD'
    #zrd_filename_to_write = 'uncompressed_write.ZRD'
    #compare_files_nbytes(get_full_path(zrd_filename), get_full_path(zrd_filename_to_write), 'i')