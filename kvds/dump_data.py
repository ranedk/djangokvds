#! /usr/bin/python

import urllib, urllib2, simplejson, sys, types
from optparse import OptionParser

def make_request(url, path, data={}):
    if options.verbose:
        print "making request", url + path + "/", urllib.urlencode(data)
    response = simplejson.loads(
        urllib2.urlopen(
            url + path + "/", urllib.urlencode(data)
        ).read()
    )
    return response

def urlencode2(d):
    a = []      
    for k in d:
        v = d[k]
        if type(v) == types.ListType:
            for x in v:
                a.append(urllib.urlencode({k: x}))
        if type(v) == types.TupleType:
            for x in v:
                a.append(urllib.urlencode({k: x}))
        else:
            a.append(urllib.urlencode({k: v}))
    return "&".join(a)

def kvds_multi(keys, url):
    global options
    q = urlencode2({ 'key':keys })
    response = simplejson.loads(
        urllib2.urlopen(
            url + "kvds/", q
        ).read()
    )
    return response

def main ():
    usage = "usage: %prog [options] kvds-hostname"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file",action = 'store', dest="filename",
                      help="output the data dump to file")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    
    parser.add_option("-m", "--mysqldump", action="store", dest="sqlfilename",
                      help="output the data dump to a sql file, Use 'mysql -uUser -pPasswd dbname < dump.sql' to dump file to mysql database")
    
    parser.add_option("-t", "--table", action="store", dest="tablename",
                      help="Table name for mysql dump")
    global options
    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        parser.error("KVDS server name required")
    url = args[0]

    response = make_request(url, "prefix",dict(prefix=''))
    res = {}

    def init_res():
        i = 0
        count = 100
        while i < len(response):
            if options.verbose:
                print "Getting " + str(i) + " Keys Data"
            keys = response[i:i+count]
            i = i + count
            result = kvds_multi(keys, url)
            res.update(result)

    if options.filename:
        if not res:
            init_res()
        FILE = open(options.filename,"w")
        print "dumping Data to File:  %s..." % options.filename 
        for r in res.keys():
            FILE.write('%s || %s\n' % (r, res[r]))
        FILE.close()

    if options.sqlfilename:
        if not options.tablename:
            parser.error("Table name for mysql dump missing ! use -t option")
        if not res:
            init_res()
        SQLFILE = open(options.sqlfilename,"w")
        print "dumping SQL Data to File:  %s..." % options.sqlfilename
        result = ",".join([str((str(k),str(simplejson.dumps(v)))) for k,v in res.items()])
        SQLFILE.write("INSERT INTO %s (key,value) VALUES %s\n" % (options.tablename,result))
        SQLFILE.close()

    if not options.filename and not options.sqlfilename:
        if not res:
            init_res()
        for r in res.keys():
            print '%s || %s\n' % (r, res[r])

if __name__ == "__main__":
    main()
