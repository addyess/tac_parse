import json
import csv
import gzip
import sys

def parse(file_obj):
    log = []
    reader = csv.DictReader(file_obj, fieldnames=['_time','_nas_name', '_username', '_nas_port', '_nac_address', '_acct_type'], restkey='__arguments__', delimiter='\t')
    for row in reader:
        row.update(dict(r.split('=') for r in row['__arguments__']))
        del row['__arguments__'] 
        log.append(row)
    return log

def parse_gz(fullPathName):
    with gzip.open(fullPathName) as f:
        return parse(f)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Parse a tacacs+ log file into JSON')
    parser.add_argument('ins', nargs = '*', type=argparse.FileType('r'))
    parser.add_argument('--out', nargs = '?', default=sys.stdout, type=argparse.FileType('w'))
    args = parser.parse_args()

    r = []

    for f in args.ins:

        if f.name.endswith('.gz') :
            l = parse_gz(f.name)
        else :
            l = parse(f)
            
        for row in l:
            row['_log'] = f.name
        
        r.extend(l)
    
    args.out.write(json.dumps(r))