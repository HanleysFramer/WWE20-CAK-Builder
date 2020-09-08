import os
import os.path
import itertools
import struct
import sys
from operator import itemgetter
from _hashbin.fnv_hash import fnv1a_64
from _hashbin.crc import Crc32c

def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def get_dir_and_files(dir, files):   #gets list of files and folders in directory
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            files.append(f.path)

    for dir in list(subfolders):
        sf, f = get_dir_and_files(dir, files)
        subfolders.extend(sf)
        files.extend(f)

    return subfolders, files

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def XOR_op(a,b):
    a = bytes_to_int(a)
    b = bytes_to_int(b)
    return hex(a ^ b)

def hexstring_to_bytes(hexstring):
    hexstring = hexstring[2:]

    if len(hexstring) == 7:                 #failsafe lol
        hexstring = '0' + hexstring
    if len(hexstring) == 6:
        hexstring = '00' + hexstring
    if len(hexstring) == 5:
        hexstring = '000' + hexstring
    if len(hexstring) == 4:
        hexstring = '0000' + hexstring
    if len(hexstring) == 3:
        hexstring = '00000' + hexstring
    if len(hexstring) == 1:
        hexstring = '0000000' + hexstring

    return bytearray.fromhex(hexstring)

def hexstring_to_bytes_swap(hexstring):
    hexstring = hexstring[2:]

    if len(hexstring) == 7:                 #failsafe lol
        hexstring = '0' + hexstring
    if len(hexstring) == 6:
        hexstring = '00' + hexstring
    if len(hexstring) == 5:
        hexstring = '000' + hexstring
    if len(hexstring) == 4:
        hexstring = '0000' + hexstring
    if len(hexstring) == 3:
        hexstring = '00000' + hexstring
    if len(hexstring) == 1:
        hexstring = '0000000' + hexstring
    hexstring = hexstring[2:]

    return bytearray.fromhex(hexstring)

def byte_swap(a):
    return a[::-1]

def cake_str_formatting(cake_folders, cake_files):
    cake_folders = [i.replace(".\\_root\\","/") for i in cake_folders]      #Format Strings List
    cake_folders = [i.replace(".\\_root","_root") for i in cake_folders]
    cake_folders = [i.replace("\\","/") for i in cake_folders]

    cake_files = [i.replace(".\\_root\\","") for i in cake_files]      #Format Strings List
    cake_files = [i.replace("\\","/") for i in cake_files]

    for i in cake_folders: 
        if " " in i:     
            exit("Subdirectory Folders contain invalid characters. Bake unsuccessful.")
    for i in cake_files:      
        if " " in i:
            exit("Subdirectory Files contain invalid characters. Bake unsuccessful.")
    for i in cake_files:                                                 #Format loose files in '_root' dir
        if "./" in i:
            i = i.replace("./", "")

    cake_folders = sorted(cake_folders)
    cake_folders = [i[1:] for i in cake_folders if i != "_root" or i == "_root"] #gotta be a better way to do this lol
    cake_folders = [i.replace("root", "_root") for i in cake_folders]
    for i in cake_folders:
        if i == "_root":
            cake_folders.insert(0, cake_folders.pop(cake_folders.index(i)))
    cake_files.sort()
    return cake_folders, cake_files

def get_bake_key(bake_file_6through9):
    bake_file_6through9 = bake_file_6through9 - 6
    hash_list = [b'\x7A\xE1\x83\xCB' , b'\x32\x8D\x16\xC7', b'\xB6\x6F\x36\x1D', b'\x35\x7A\x86\xF8']
    hash_key = hash_list[bake_file_6through9]
    return hash_key

def get_cake_folder_hashes(folder_list):
    out_list = []
    for i in folder_list:
        i = str.lower(i)
        i = (fnv1a_64(bytes(i, 'utf-8')))
        out_list.append(i)
    return out_list

def get_cake_file_hashes(file_list):
    out_list = []
    for i in file_list:
        i = str.lower(i)
        i = (fnv1a_64(bytes(i, 'utf-8')))
        out_list.append(i)
    return out_list

def sort_hashes(input_list):
    input_list.sort()
    return input_list 

def get_file_data(curr_file_path):
    curr_file.insert(0, ".\\_root")
    curr_2 = intersperse(curr_file, "\\")
    curr_2 = ''.join(curr_2)
    size = os.path.getsize(curr_2)
    filecrc32c = "00000000"

    # with open(curr_2, "rb") as f:
    #     filecrc32c = f.read()
    #     filecrc32c = Crc32c().process(filecrc32c).finalhex()

    return size, filecrc32c

def get_file_folderpath(curr_file):
                curr_folder= curr_file[1:-1]
                curr_folder= intersperse(curr_folder, "/")
                curr_folder= ''.join(curr_folder)
                return curr_folder

def swap_bytes_2(a):
    a = bytearray.fromhex(crcfile)
    a = bytes_to_int(a)
    a = a.to_bytes(4, byteorder = 'little')
    return a

def ulong_fnv1a64(i):
    i = i.to_bytes(8, byteorder='little')
    return i
    
def get_folder_str_off(input_list, n):
    input_list = input_list[:n]
    input_list = intersperse(input_list, ".")
    a = len(''.join(input_list)) + 1
    if a == 1:
        a = 0

    return a 

def get_folder_subfldr(input_list, n):
    selected_folder = input_list[n]
    b = []
    c = []
    a = len(selected_folder)
    count = 0

    if "_root" == selected_folder:
        n=-1
        for i in input_list:
            if "/" not in i:
                n+=1
        count = n
    else:
        if selected_folder.count("/") == 0:

            for i in input_list:
                if i.count("/") == 1:
                    b.append(i)
            for i in b:
                if i[:a] == selected_folder:
                    c.append(i)
                    # print(i)
                    # count += 1
            for i in c:
                if len(i[a:]) > 1:
                    count += 1
        else:
            for x in input_list:
                if (selected_folder + "/") in x[:a+1]:
                    e = x[:a+1]
                    slash_count = x.count("/")
                    slash_counta= e.count("/")
                    if slash_count == slash_counta: 
                        count += 1

    # if selected_folder.count("/") > 1:
    #     count = selected_folder.count("/") - 1
    if count < 0:
        count = 0
    return count

def get_folder_loose_files(input_list, file_list, n):
    selected_folder = input_list[n]

    if "_root" == selected_folder:
        n=0
        for i in file_list:
            if "/" not in i:
                n+=1
        count = n
        
    else:
        subfile_0 = []
        subfile_1 = []
        count = 0
        for i in file_list:
            if selected_folder in i:
                if i[len(selected_folder)] == "/":
                    subfile_0.append(i)
        
        for i in subfile_0:
            if selected_folder in i:
                i = i.replace(selected_folder, "")
                subfile_1.append(i)

        for i in subfile_1:
            if i.count("/") == 1:
                count += 1
    return count

def get_subfolder_string_loc(input_list, n, sf_count):
    selected_folder = input_list[n]
    # print(selected_folder)
    subf_list = []
    subf_list0= []
    root_list = []
    a = len(selected_folder)

    for i in input_list:
        if i[:a] == selected_folder:
            subf_list.append(i)

    for i in subf_list:
        if i.count("/") == 1:
            subf_list0.append(i)
        else:
            subf_list0.append(i)

    if "_root" == selected_folder:
        for i in input_list:
            if i.count("/") == 0:
                root_list.append(i)
        subf_list0 = root_list
            

    test = [i for i, item in enumerate(cake_folders) if item in subf_list0]
    test = test[:sf_count]
    test = [i+1 for i in test]


    if selected_folder.count("/") == 0:
        test = [i for i, item in enumerate(cake_folders) if item in subf_list0]
        test.pop(0)
        test = test[:sf_count]
    
    # print(test)
    return test

def get_subfile_string_loc(input_list, folders_list, sfile_count):
    curr_folder = folders_list[n]
    file_list   = []
    file_b = []
    file_c = []
    loose ="."
    z = "."

    for i in input_list:
        if curr_folder in i:
            if i[len(curr_folder)] == "/":
                file_list.append(i)
        else:
            if curr_folder == "_root":
                if i.count("/") == 0:
                    file_c.append(i)
                    loose = "true"
    for i in file_list:
        slash_count = curr_folder.count("/")
        slash_counta= i.count("/")
        if slash_count == (slash_counta - 1):
            file_b.append(i)
            z = "true"

    
    if z == "true":
        index = [i for i, item in enumerate(input_list) if item in file_b]
    else:
        index = [i for i, item in enumerate(input_list) if item in file_list]
        
    if loose == "true":
        index_b = [i for i, item in enumerate(input_list) if item in file_c]

    if loose == ".":
        return index
    else:
        return index_b

def file_string(input_list, n):
    curr_file = input_list[n]
    lst = input_list[:input_list.index(curr_file)+1]
    lst = intersperse(lst, "_")
    lst = ''.join(lst)
    lst = len(lst) + n
    lst = lst - len(curr_file)
    return lst

def get_file_header(input_list):
    curr_2 = intersperse(curr_file, "\\")
    curr_2 = ''.join(curr_2)

    with open(curr_2, "rb") as f:
        f.seek(8)
        file_type = f.read(4)
    if file_type == b'\x3f\x04\x00\x00':
        file_type = b'\x00\x00\x00\x00' 
    if file_type == b'\x00\x00\x00\x10':
        file_type = b'\x00\x00\x00\x00' 
    if file_type == b'\x2C\x00\x00\x00':
        print("Chunk1-pc.arc baked!")
        file_type = b'\x00\x00\x00\x00' 

    return file_type

def get_file(input_list):  
    curr_2 = intersperse(curr_file, "\\")
    curr_2 = ''.join(curr_2)

    with open(curr_2, "rb") as f:
        file_type = f.read()

    return file_type          

# # # Initial Data # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # 
 
curr_directory = os.chdir(".\\_Cake")  #Home Directory
home_path = os.getcwd()
files = "."
BakedFile = "bakedfile06.cak"
Cake_Flavor = (BakedFile[10:])[:1]


if int(Cake_Flavor) not in range(6,10):
    print(BakedFile, "not in range 6 through 9. Cannot continue.")
    exit("Please rebake within range 'BakedFile06' through 'BakedFile09'...")

Cake_Key = get_bake_key(int(Cake_Flavor))                               #Get main file hash

cake_folders, cake_files = get_dir_and_files(curr_directory, files)     #Grab File/Folder data
cake_files_count   = len(cake_files) 
cake_folders_count = len(cake_folders)

cake_folders, cake_files = cake_str_formatting(cake_folders, cake_files)
cake_folder_hashes       = get_cake_folder_hashes(cake_folders)         #Grab Folder FNV Hash
cake_file_hashes         = get_cake_file_hashes(cake_files)             #Grab File FNV Hash
# ***********************************************************************

print("Baking", cake_files_count, "files...")
print("Baking", cake_folders_count, "folders...")
print("Baking 1 cake... ")

if __name__ == '__main__':

    ###FolderStrings_Blocks Write #########
    with open(os.path.join(os.path.dirname(__file__), 'string_block_folders.bin'), 'wb') as f:

        for i in cake_folders:                                  #Writes Folders to String Block
            i = i.encode(encoding='UTF-8',errors='strict')
            i = i + b'\x00'
            f.write(i)
        f.close()

    ###FileStrings_Blocks Write #########
    with open(os.path.join(os.path.dirname(__file__), 'string_block_files.bin'), 'wb') as f:

        for i in cake_files:                                    #Writes Files to String Block
            i = i.encode(encoding='UTF-8',errors='strict')
            i = i + b'\x00'
            f.write(i)
        f.close()    

    ###FolderHash_Block Write ######
    with open(os.path.join(os.path.dirname(__file__), 'folderhash_block.bin'), 'wb') as f:  
        n = -1
        folderhashes_indices, sorted_cake_folderhashes = zip(*sorted(enumerate(cake_folder_hashes), key=itemgetter(1)))
        for i in sorted_cake_folderhashes:
            n += 1
            a = sorted_cake_folderhashes[n].to_bytes(8, byteorder='little')
            f.write(a)
            b = folderhashes_indices[n].to_bytes(4, byteorder='little')
            f.write(b)

    ###FileHash_Block   Write #########
    with open(os.path.join(os.path.dirname(__file__), 'filehash_block.bin'), 'wb') as f:
        n = -1
        filehash_indices, sorted_cake_filehashes = zip(*sorted(enumerate(cake_file_hashes), key=itemgetter(1)))
        for i in sorted_cake_filehashes:
            n += 1
            a = sorted_cake_filehashes[n].to_bytes(8, byteorder='little')
            f.write(a)
            b = filehash_indices[n].to_bytes(4, byteorder='little')
            f.write(b)

    ###Folders_Block    Write #########
    with open(os.path.join(os.path.dirname(__file__), 'folders_block.bin'), 'wb') as f:
        n =-1
        for i in cake_folder_hashes:
            n += 1
            fhash = ulong_fnv1a64(i)
            f.write(fhash)

            folder_offset = get_folder_str_off(cake_folders, n)
            folder_offset = folder_offset.to_bytes(4, byteorder='little')
            f.write(folder_offset)

            folder_subfolder_count = get_folder_subfldr(cake_folders, n)                            #get subfolders
            folder_subfolder_count_byte = folder_subfolder_count.to_bytes(4, byteorder='little')
            f.write(folder_subfolder_count_byte)

            folder_subfile_count   = get_folder_loose_files(cake_folders, cake_files, n)            #get loose files
            folder_subfile_count_byte   = folder_subfile_count.to_bytes(4, byteorder='little')
            f.write(folder_subfile_count_byte)

            if folder_subfolder_count != 0:                 #subfolder(s) string index
                b = get_subfolder_string_loc(cake_folders, n, folder_subfolder_count)
                for i in b:
                    i = i.to_bytes(4, byteorder='little')
                    f.write(i)

            if folder_subfile_count != 0:                   #subfiles(s) string index
                a = get_subfile_string_loc(cake_files, cake_folders, cake_files_count)
                for i in a:
                    i = i.to_bytes(4, byteorder='little')
                    f.write(i)


        # (fnv1a_64(bytes(input_cak, 'utf-8')))

    ###Files_Block      Write #########
    with open(os.path.join(os.path.dirname(__file__), 'files_block.bin'), 'wb') as f:
        off_0 = ''.join(cake_folders)           #get_fileblock_start
        off_0 = len(off_0) + cake_folders_count 
        folders_block_size = os.path.getsize(os.path.join(os.path.dirname(__file__),      'folders_block.bin'))
        folderhash_block_size = os.path.getsize(os.path.join(os.path.dirname(__file__),   'folderhash_block.bin'))
        filehash_block_size = os.path.getsize(os.path.join(os.path.dirname(__file__),     'filehash_block.bin'))
        string_fldrs_block_size = os.path.getsize(os.path.join(os.path.dirname(__file__), 'string_block_folders.bin'))
        string_files_block_size = os.path.getsize(os.path.join(os.path.dirname(__file__), 'string_block_files.bin'))

        files_start_offset = (folders_block_size + folderhash_block_size + filehash_block_size + string_files_block_size + string_fldrs_block_size)
        files_start_offset = files_start_offset + (28 * cake_files_count) + 88

        size_list = [00,00]
        n = -1

        for i in cake_files:                    #get_filesize and file_folder

            n += 1

            string_off = file_string(cake_files, (cake_files.index(i)))
            string_off = string_off + off_0 - n
            curr_file  = i.split('/')
            curr_size , crcfile  = get_file_data(curr_file)
            file_type = get_file_header(curr_file)

            size_list.append(curr_size)
            sum_list = size_list[:-1]
            file_size_sum = sum(sum_list)

            curr_file0 = curr_file[-1]
            curr_file_folder = get_file_folderpath(curr_file)
            if "" == curr_file_folder:  #loose file check
                curr_file_folder = "_root"
            folder_index = cake_folders.index(curr_file_folder) #get_filesfolderindex
               
            offset = string_off.to_bytes(4, byteorder='little')
            f.write(offset)
            folder_index = folder_index.to_bytes(4, byteorder='little')
            f.write(folder_index)
            crcfile = swap_bytes_2(crcfile)
            curr_size= curr_size.to_bytes(4, byteorder='little')
            f.write(crcfile)        #write crc
            f.write(curr_size)      #write size

            file_offset = files_start_offset + file_size_sum
            file_offset = file_offset.to_bytes(4, byteorder='little')
            f.write(file_offset)   #write offset
            f.write(b'\x00\x00\x00\x00')
            f.write(file_type)

    ###StringMerge 
    os.chdir(sys.path[0])
    filenames = ['string_block_folders.bin', 'string_block_files.bin']
    with open('strings.bin', 'wb') as outfile:
        for fname in filenames:
            with open(fname, 'rb') as infile:
                outfile.write(infile.read())

    ###BakedHeader_Block      Write #########
    filenames = ['folderhash_block.bin', 'filehash_block.bin', 'files_block.bin', 'folders_block.bin', 'strings.bin']

    with open(BakedFile, 'wb') as bakedfile:     ###GathersAndWritesHeader_Data 
        header = b'\x46\x44\x49\x52\x06\x08\x40\x00'
        null_block = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        file_count_bytes = cake_files_count.to_bytes(4, byteorder='little')
        fldr_count_bytes = cake_folders_count.to_bytes(4, byteorder='little')
        bakedfile.write(header)
        bakedfile.write(file_count_bytes)
        bakedfile.write(fldr_count_bytes)

        size = 0
        start= 88
        string_size = 0
        n = -1

        for fname in filenames:                 
            with open(fname, 'rb') as infile:
                n+=1
                a = infile.read()
                size0 = len(a)

                size1 = size0.to_bytes(4, byteorder='little')
                bakedfile.write(size1)
                if n < 5:
                    filecrc32c = a
                    filecrc32c = Crc32c().process(filecrc32c).finalhex()
                    filecrc32c = bytearray.fromhex(filecrc32c)
                    filecrc32c = byte_swap(filecrc32c)
                    bakedfile.write(filecrc32c)

                    offset = size + 88
                    offset = offset.to_bytes(4, byteorder='little')
                    bakedfile.write(offset)

                    size += size0

        bakedfile.write(null_block)
        files_start_offset = files_start_offset.to_bytes(4, byteorder='little')
        bakedfile.write(files_start_offset)

    with open(BakedFile, 'ab') as bakedfile:     ###GathersAndWritesHeader_Block
        for fname in filenames:
            with open(fname, 'rb') as infile:
                bakedfile.write(infile.read())

        n = -1
        for i in cake_files:                  ###get_files
            n += 1
            string_off = file_string(cake_files, (cake_files.index(i)))
            string_off = string_off + off_0 - n
            curr_file  = i.split('/')
            a = [".\\_Cake\\_root"]
            curr_file = a + curr_file
            a = get_file(cake_files)
            bakedfile.write(a)

  
    ### debug prints
    # print("\n" + "General Info:" + "\n")
    # print(cake_folders)
    # print(cake_files)
    # print(cake_folder_hashes)
    # print(cake_file_hashes)
    # print(os.getcwd())

os.remove('folderhash_block.bin')
os.remove('filehash_block.bin')
os.remove('files_block.bin')
os.remove('folders_block.bin')
os.remove('strings.bin')
os.remove('string_block_folders.bin')
os.remove('string_block_files.bin')

print('\n', '\n', '\n')
input("Directory baked succesfully!")