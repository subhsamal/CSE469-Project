#Author: Rakeen Huq

#!/usr/bin/env python

import sys
import hashlib                 
import struct
import binascii
from binascii import hexlify


md5 = hashlib.md5();
sha1 = hashlib.sha1();

#Store the name of file
file = sys.argv[1]

f = open(file, 'rb');
while True:
        data = f.read()
        if not data:
            break
        md5.update(data)
        sha1.update(data)

#Remove the '.img' tag from the file
if file.endswith('.img'):
    file2 = file[:-4]

print("MD5: {0}".format(md5.hexdigest()));
print("SHA1: {0}".format(sha1.hexdigest()));

#Print MD5 to file
f1 = open("MD5-" + file2 + ".txt", 'w');
f1.write(md5.hexdigest())
f1.close();

#Print SHA1 to file
f2 = open("SHA1-" + file2 + ".txt", 'w');
f2.write(sha1.hexdigest())
f2.close();

f.close();
print("\n");
########################################### Partition Parsing Code ##################################################################

#Return the name of the partiton type
def partition_type(file_type_hex):
    file_system = { '0x0' : "Empty", '0x1' : "FAT12", '0x2' : "XENIX root", '0x3' : "XENIX usr",
                      '0x4' : "DOS 16-bit FAT for partitions smaller than 32 MB", '0x5' : "Extended", '0x6' : "DOS 16-bit FAT for partitions larger than 32 MB", '0x7' : "NTFS", '0x8' : "AIX" ,
                      '0x9' : "AIX Bootable" , '0xa' : "OS/2 Boot" , '0xb' : "DOS 32-bit FAT" , '0xc' : "Win95 FAT32" ,
                      '0xd' : "Reserved" , '0xe' : "Win95 FAT16" , '0xf' : "Win95 Ext" , '0x10' : "OPUS" ,
                      '0x11' : "FAT12 Hidden" , '0x12' : "Compaq Diag" , '0x13' : "N/A" , '0x14' : "FAT16 Hidden" ,
                      '0x15' : "Extended Hidden" , '0x16' : "FAT16 Hidden" , '0x17' : "NTFS Hidden" , '0x18' : "AST" ,
                      '0x19' : "Willowtech" , '0x1a' : "N/A" , '0x1b' : "Hidden FAT32" , '0x1c' : "Hidden FAT32X" ,
                     '0x1d' : "N/A" , '0x1e' : "Hidden FAT16X" }

    partition_type = file_system[file_type_hex]
    return partition_type

#For parsing offset ranges such as 12-16
def parse_offsets(array):
    if(len(array) == 4):
        offset_1 = struct.pack("<B", array[0]);
        offset_2 = struct.pack("<B", array[1]);
        offset_3 = struct.pack("<B", array[2]);
        offset_4 = struct.pack("<B", array[3]);
        combine = offset_1 + offset_2 + offset_3 + offset_4;
        data = struct.unpack("<L", combine)[0];
        return data;
    if(len(array) == 2):
        offset_1 = struct.pack("<B", array[0]);
        offset_2 = struct.pack("<B", array[1]);
        offset_3 = struct.pack("<B", 0);
        offset_4 = struct.pack("<B", 0);
        combine = offset_1 + offset_2 + offset_3 + offset_4;
        data = struct.unpack("<L", combine)[0];
        return data;

#Parse Partition to print out required values
def parse_partition(partition):
    typeof_partition = partition_type(hex(partition[4]))
    print("(" + str(hex(partition[4])) + ") " + typeof_partition + ", " + str(parse_offsets(partition[8:12])) + ", " + str(parse_offsets(partition[12:16])));
    
    if(str(hex(partition[4])) == "0x6"):
        vbr = parse_offsets(partition[8:12])*512;
        reserved_area = struct.unpack("<BB", mbr[vbr+14:vbr+16]);
        reserved_val = parse_offsets(reserved_area[0:2]);
        FAT16_size = struct.unpack("<BB", mbr[vbr+22:vbr+24]);
        FAT16_sectors = parse_offsets(FAT16_size[0:2]);
        print("Reserved area: \tStart sector: {} \tEnding sector: {}\tSize: {} sectors".format(partition[2], partition[6], reserved_val));
        print("Sectors per cluster: {} sectors".format(mbr[vbr+13]));
        print("FAT area: \tStart sector:  {} \tEnding sector: {}".format(parse_offsets(partition[8:12]), (mbr[vbr+16] * FAT16_sectors) + parse_offsets(partition[8:12]) ));
        print("# of FATS: {}".format(mbr[vbr+16]));
        print("The size of each FAT: {}".format(FAT16_sectors)) ;
        cluster2 = reserved_val + mbr[vbr+13] + (FAT16_sectors-mbr[vbr+16])*mbr[vbr+13];
        print("The first sector of cluster 2: {}".format(cluster2));
    elif(str(hex(partition[4]))  == "0xb"):
        vbr = parse_offsets(partition[8:12])*512;
        reserved_area = struct.unpack("<BB", mbr[vbr+14:vbr+16]);
        reserved_val = parse_offsets(reserved_area[0:2]);
        FAT32_size = struct.unpack("<BBBB", mbr[vbr+36:vbr+40]);
        FAT32_sectors = parse_offsets(FAT32_size[0:2]);
        print("Reserved area: \tStart sector: {} \tEnding sector: {}\tSize: {} sectors".format(partition[2], partition[6], reserved_val));
        print("Sectors per cluster: {} sectors".format(mbr[vbr+13]));
        print("FAT area: \tStart sector:  {} \tEnding sector: {}".format(parse_offsets(partition[8:12]), (mbr[vbr+16] * FAT32_sectors) + parse_offsets(partition[8:12])));
        print("# of FATS: {}".format(mbr[vbr+16]));
        print("The size of each FAT: {}".format(FAT32_sectors));
        cluster2 = reserved_val + mbr[vbr+13] + (FAT32_sectors-mbr[vbr+16])*mbr[vbr+13];
        print("The first sector of cluster 2: {}".format(cluster2))
    print("\n");
        
#IN order to find where the VBR starts(for FAT32/FAT16) multiply the starting sector by 512.


#Start to read the MBR and partitions
with open(file, "rb") as f:
    mbr = f.read()


partition_1 = struct.unpack("<BBBBBBBBBBBBBBBB", mbr[446:462])
parse_partition(partition_1);

partition_2 = struct.unpack("<BBBBBBBBBBBBBBBB", mbr[462:478])
parse_partition(partition_2);

partition_3 = struct.unpack("<BBBBBBBBBBBBBBBB", mbr[478:494])
parse_partition(partition_3);

partition_4 = struct.unpack("<BBBBBBBBBBBBBBBB", mbr[494:510])
parse_partition(partition_4);




      
                       




