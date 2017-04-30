


import argparse
import datetime
import sys



def mac_parser():
    #print ("I am inside mac_parser")
    parser = argparse.ArgumentParser(description = 'purpose of this task is to write code that performs the MAC conversion based on the following usage \
             specification and input/output scheme')
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-T', '--time', action = 'store_true', help = 'Use time conversion module. Either –f or –h must be given.')
    group.add_argument('-D', '--date', action = 'store_true', help = 'Use date conversion module. Either –f or –h must be given.')

    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-f', '--filename', help = 'This specifies the path to a filename that includes a hex value of time or date. Note that the hex value \
                        should follow this notation: 0x1234. For the multiple hex values in either a file or a command line input, we consider only one hex value so the \
                         recursive mode for MAC conversion is optional.')
    group.add_argument('-x', '--hexvalue',help = 'This specifies the hex value for converting to either date or time value. Note that the hex value \
                        should follow this notation: Ox1234. For the multiple hex values in either a file or a command line input, we consider only \
                        one hex value so the recursive mode for MAC conversion is optional.')
    return parser

def parse_Time(decimal):
    binary = '{0:016b}'.format(decimal)   #conver decimal value/integer value to binary
    #Assign Hour, Minute and Second from the binary value
    Hr = int (binary[0:5],2)
    Min = int (binary[5:11], 2)
    Sec = int (binary[11:16], 2) *2   # Since second ranges 0-29
    date = datetime.time(Hr, Min, Sec)     #this method stores in the format 00:00:00
    return date.strftime("Time: %I:%M:%S %p")

def parse_Date(decimal):
    binary = '{0:016b}'.format(decimal) #Decimal to binary
    Year = int (binary[0:7], 2) + 1980  #base address 1980 as Unix system developed in 1980
    Month = int (binary[7:11], 2)
    Day = int(binary[11:], 2)
    date = datetime.date(Year, Month, Day)
    #time_format_one = "%b %d, %Y"
    return date.strftime("Date: %b %d %Y")


def main():
    #print ("i am inside main")
    parser = mac_parser()
    global args
    global ampm

    args = parser.parse_args()

    if not args.date and not args.time:
        parser.print_help()
        sys.exit(1)

    if not args.filename and not args.hexvalue:
        parser.print_help()
        sys.exit(1)

    #get the hexvalue from the file
    if args.filename is not None:
        fhand = open(args.filename, 'r')
        hex_value = fhand.readline()
        fhand.close()
    else:                                           #else get it from the commandline
        hex_value = args.hexvalue


    #verify the hex input
    if ("0x" not in hex_value and len(hex_value) != 6):
        print ("invalid hex value!! provide in the format '0x****'")

    hex_value = hex_value[2:]          #remove 0x from the hex input

    #convert it to little endian
    hex_value1 = hex_value[2:]
    hex_value2 = hex_value[0:2]
    hex_value3 = hex_value1 + hex_value2

    decimal = int(hex_value3, 16)     #convert 2byte hex to 16 bit integer

    #parse time and date
    if args.time:
        print(parse_Time(decimal))

    elif args.date:
        print(parse_Date(decimal))

    else:
        pass


if __name__ == '__main__':
    main()
