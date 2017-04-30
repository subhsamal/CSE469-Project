
'''command line utility that will convert between three different address types.
Logical, Physical and Cluster.
argparse python module is used— this is a Parser for command-line options, arguments and sub-commands'''

import argparse



def address_parser():
    parser = argparse.ArgumentParser(description = 'This is a program for address conversion, address of a given type is converted between 3 different types')
    #create a group for mutually exclusive arguments
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-L', '--logical', action = 'store_true',
        help = 'Calculate the logical address from either the cluster address or the physical address. Either –c or –p must be given.') #action = 'store_true' saves the appropriate boolean value.
    group.add_argument('-P', '--physical', action = 'store_true',
        help = 'Calculate the physical address from either the cluster address or the logical address. Either –c or –l must be given.')
    group.add_argument('-C', '--cluster', action = 'store_true',
        help = 'Calculate the cluster address from either the logical address or the physical address. Either –l or –p must be given.')
    parser.add_argument('-b', '--partition_start', metavar = 'offset', type = int, default = 0,
        help = 'This specifies the physical address (sector number) of the start of the partition, and defaults to 0 for ease in working with images of \
                a single partition. The offset value will always translate into logical address 0.')
    #metavar provides a different name for optional argument in help messages.
    parser.add_argument('-B', '--byte-address', action = 'store_true',
        help = 'Instead of returning sector values for the conversion, this returns the byte address of the calculated value, which is the number of \
                sectors multiplied by the number of bytes per sector.')
    parser.add_argument('-s', '--sector-size', metavar = 'bytes', type = int,
        help = 'When the –B option is used, this allows for a specification of bytes per sector other than the default 512. Has no affect on output without –B.')
    parser.add_argument('-l', '--logical-known', metavar = 'address', type = int,
        help = 'This specifies the known logical address for calculating either a cluster address or a physical address. When used with the –L option, \
                this simply returns the value given for address.')
    parser.add_argument('-p', '--physical-known', metavar = 'address', type = int,
        help = 'This specifies the known physical address for calculating either a cluster address or a logical address. When used with the –P option, \
                this simply returns the value given for address.')
    parser.add_argument('-c', '--cluster-known', metavar = 'address', type = int,
        help = 'This specifies the known cluster address for calculating either a logical address or a physical address. When used with the –C option, \
                this simply returns the value given for address. Note that options –k, -r, -t, and –f must be provided with this option.')
    parser.add_argument('-k', '--cluster_size', metavar = 'sectors', type = int, help = 'This specifies the number of sectors per cluster.')
    parser.add_argument('-r', '--reserved', metavar = 'sectors', type = int, help = 'This specifies the number of reserved sectors in the partition.')
    parser.add_argument('-t', '--fat_tables', metavar = 'tables', type = int, help = 'This specifies the number of FAT tables, which is usually 2.')
    parser.add_argument('-f', '--fat_length', metavar = 'sectors', type = int, help = 'This specifies the length of each FAT table in sectors.')
    return parser


def address_physical(logical_address = None, cluster_address = None, offset = 0):
    #Calculates the physical address value given either a logical address or cluster address.
    if logical_address is None and cluster_address is None:
        raise Exception ('At least one of logical or cluster address should be given to calculate physical address')
    if logical_address is not None:
        physical_address = args.partition_start + args.logical_known #partition_start metavar is offset and default value = 0
    elif cluster_address is not None:
        if args.cluster_size is None or args.fat_tables is None or args.fat_length is None or args.reserved is None:
            raise Exception ('all of -k, -t, -f and -r need to be provided along with -c to calculate P')
        physical_address = args.partition_start + args.reserved + (args.fat_tables * args.fat_length) + (args.cluster_known -2) * args.cluster_size
    else:
        physical_address = None

    return physical_address



def address_logical(physical_address = None, cluster_address = None, offset = 0):
    #calculates the logical address value given either a physcial or cluster address, first convvert to physical address
    if physical_address is None and cluster_address is None:
        raise Exception ('At least one of the physical_address or cluster_address should be provided to calculate logical_address')
    if cluster_address is not None:
        if args.cluster_size is None or args.fat_tables is None or args.fat_length is None or args.reserved is None:
            raise Exception ('all of -k, -t, -f and -r need to be provided to calculate L')
        logical_address = args.partition_start + ((cluster_address - 2) * args.cluster_size) + args.reserved + (args.fat_tables * args.fat_length)
    elif physical_address is not None:
        logical_address = physical_address - offset
    else:
        logical_address = None
    #logical_address = logical_address - offset
    return logical_address


def address_cluster(physical_address = None, logical_address = None, offset = 0):
    if physical_address is None and logical_address is None:
        raise Exception ('At least one of the physical_address or logical_address should be provided to calculate logical_address')
    if logical_address is not None:
        if args.cluster_size is None or args.fat_tables is None or args.fat_length is None or args.reserved is None:
            raise Exception ('all of -k, -t, -f and -r need to be provided to calculate C')
        cluster_address = (logical_address - args.reserved - (args.fat_tables * args.fat_length)) // (args.cluster_size) + 2   #// for integer output
    elif physical_address is not None:
        cluster_address = physical_address - offset
    else:
        cluster_address = None
    return cluster_address


def main():
    #parser = argparse.ArgumentParser()   take this part into a separate function
    parser = address_parser()

    global args # args is global, so can be used within any function
    args = parser.parse_args() #The return value from parse_args() is a Namespace containing the arguments to the command.

    if args.physical:
        print(address_physical(logical_address = args.logical_known, cluster_address = args.cluster_known, offset = args.partition_start))
    if args.logical:
        print ("I am here")
        print(address_logical(physical_address1 = args.physical_known, cluster_address1 = args.cluster_known, offset = args.partition_start))
    if args.cluster:
        print(address_cluster(physical_address = args.physical_known, logical_address = args.logical_known, offset = args.partition_start))



if __name__ == '__main__':
    main()
