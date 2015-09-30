import json
import csv
import gzip
import sys
import os
import time

def parse(file_obj, m_year=1900, timestamp_format=None):
    log = []
    reader = csv.DictReader(file_obj, fieldnames = ['time',
                                                    'nas_name',
                                                    'username',
                                                    'nas_port',
                                                    'nac_address',
                                                    'acct_type'], 
                            restkey='__arguments__', delimiter='\t')

    try:
        from dateutil import parser
        def parse_date(time_str):
            return parser.parse(time_str).strftime("%Y/%m/%d %H:%M:%S")
        
    except ImportError:
        sys.stderr.write('Improve Timestamp Parsing with "pip install python-dateutil"')

        def parse_date(time_str):
            '''
            tac_plus changed their date logging feature to not include the date in-order to match
            syslog.  This means if you're using later versions of tac_plus then you'll lose precision
            on your date formatting.  We'll try to grab it from the modified timestamp on the log file
            but there's no real luck it's correct.
            '''  
            
            date_formats = [
                '%b %d %H:%M:%S',       # ex) 'Sep 24 16:19:55'            Date Log without a year ( seen with shrubbery tac_plus F4.0.4.20 and beyond ) 
                '%a %b %d %H:%M:%S %Y', # ex) 'Sun Sep 20 07:00:01 2015'   Date Log with a year    ( seen with shrubbery tac_plus up through F4.0.4.19 )
            ]
    
            if timestamp_format:
                date_formats = [timestamp_format]
    
            the_date = time.gmtime(0)
            for fmt in date_formats:
                try:
                    the_date = time.strptime(time_str, fmt)
                    if the_date.tm_year == 1900:
                        the_date = time.strptime(time_str + ' {}'.format(m_year), fmt + " %Y") #reparse with this file's year appended
                except ValueError as e:
                    if timestamp_format:
                        raise e
            
            return time.strftime("%Y/%m/%d %H:%M:%S", the_date)
    
    for row in reader:
        row.update(dict(r.split('=') for r in row['__arguments__'] if '=' in r))
        row['time'] = parse_date(row['time'])

        # remove aggrivating ' <cr>' at the end of every cmd statement
        if row.has_key('cmd') and row['cmd'].endswith(' <cr>') :
            row['cmd'] = row['cmd'][:-len(' <cr>')] 

        del row['__arguments__'] 
        log.append(row)
    return log

def parse_gz(fullPathName, m_year, timestamp_format=None):
    with gzip.open(fullPathName) as f:
        return parse(f, m_year)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Parse a tacacs+ log file into JSON')
    parser.add_argument('ins',                nargs = '*', type=argparse.FileType('r'))
    parser.add_argument('--out',              nargs = '?', default=sys.stdout, type=argparse.FileType('w'))
    parser.add_argument('--timestamp_format', nargs = '?', default=None)
    args = parser.parse_args()

    r = []

    for f in args.ins:
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(f.name)
        m_year = time.localtime(mtime).tm_year
        if f.name.endswith('.gz') :
            l = parse_gz(f.name, m_year, args.timestamp_format)
        else :
            l = parse(f, m_year, args.timestamp_format)
            
        for row in l:
            row['logfile_name'] = f.name
        
        r.extend(l)
    
    args.out.write(json.dumps(r))