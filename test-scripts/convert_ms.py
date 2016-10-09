#!/usr/bin/python2.7
import sys

def main( file_path ):
    print( file_path )
    new_values = []

    with open(file_path, "r") as fi: 
        for l in fi:
            v = float(float(l.strip())) * 1000
            new_values.append(v)

    with open(file_path + "ms.dat", "w+") as fi:
        for v in new_values:
            fi.write(str(v))
            fi.write('\n')

if __name__ == "__main__":
    main( sys.argv[1] )
