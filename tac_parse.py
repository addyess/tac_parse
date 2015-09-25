import json
import csv
import gzip
import sys
import os
import time

def parse(file_obj, m_year=1900):
    log = []
    reader = csv.DictReader(file_obj, fieldnames = ['time',
                                                    'nas_name',
                                                    'username',
                                                    'nas_port',
                                                    'nac_address',
                                                    'acct_type'], 
                            restkey='__arguments__', delimiter='\t')

    def parse_date(time_str):
        '''
        tac_plus changed their date logging feature to not include the date in-order to match
        syslog.  This means if you're using later versions of tac_plus then you'll lose precision
        on your date formatting.  We'll try to grab it from the modified timestamp on the log file
        but there's no real luck it's correct.
        '''  
        
        date_formats = [
            '%b %d %H:%M:%S',       # Date Log without a year ( seen with tac_plus F4.0.4.20 and beyond ) 
            '%a %b %d %H:%M:%S %Y'  # Date Log with a year    ( seen with tac_plus up through F4.0.4.19 )
        ]

        the_date = time.gmtime(0)
        for fmt in date_formats:
            try:
                the_date = time.strptime(time_str, fmt)
                if the_date.tm_year == 1900:
                    the_date = time.strptime(time_str + ' {}'.format(m_year), fmt + " %Y") #reparse with this file's year appended
            except ValueError:
                pass             
        
        return time.strftime("%Y/%m/%d %H:%M:%S", the_date)
    
    for row in reader:
        row.update(dict(r.split('=') for r in row['__arguments__']))
        row['time'] = parse_date(row['time'])
        del row['__arguments__'] 
        log.append(row)
    return log

def parse_gz(fullPathName, m_year):
    with gzip.open(fullPathName) as f:
        return parse(f, m_year)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Parse a tacacs+ log file into JSON')
    parser.add_argument('ins', nargs = '*', type=argparse.FileType('r'))
    parser.add_argument('--out', nargs = '?', default=sys.stdout, type=argparse.FileType('w'))
    args = parser.parse_args()

    r = []

    for f in args.ins:
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(f.name)
        m_year = time.localtime(mtime).tm_year
        if f.name.endswith('.gz') :
            l = parse_gz(f.name, m_year)
        else :
            l = parse(f, m_year)
            
        for row in l:
            row['logfile_name'] = f.name
        
        r.extend(l)
    
    args.out.write(json.dumps(r))