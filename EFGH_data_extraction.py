#!/usr/bin/env python

import csv
from pymarc import reader
from os import listdir
from re import search
import string  
#import Levenshtein
#import thread
import time
import sys, getopt
import traceback

def fingerprint_keyer(rec):
	recarray = reclist = output = ""
	rec = rec.strip()	#strip whitespace around the string
#lowercase string
	rec = rec.lower()
#remove all non-alpha num
	rec = rec.translate(string.maketrans("",""), string.punctuation)
#split by whitespace split
	recarray = rec.split(" ")
#order tokens and dedup
	reclist = sorted(list(set(recarray)))
	reclist = [i for i in reclist if i != 'none']
#join fragements back together
	output = ' '.join(reclist)
	output = output.strip()
	ouput = output.lstrip("0")
	return output

def numeric_keyer(rec):
	recarray = reclist = output = ""
	rec = rec.strip()	#strip whitespace around the string
#lowercase string
	rec = rec.lower()
#remove all non-alpha num
	rec = rec.translate(string.maketrans("",""), string.punctuation)
	rec = rec.translate(string.maketrans("",""), string.ascii_letters)
#split by whitespace split
	recarray = rec.split(" ")
#order tokens and dedup	
	reclist = sorted(list(set(recarray)))
	reclist = [i for i in reclist if i != 'none']
#join fragements back together
	output = ' '.join(reclist)
	output = output.strip()
	ouput = output.lstrip("0")
	return output    	

###Old setup stuff, remove once working
#searchstring = '.mrc'
savefile = '../From_SRLF/srlf_for_loading.csv'	
#SRC_DIR = './Data'
# get a list of all .mrc files in source directory
#file_list = filter(lambda x: search(searchstring, x), listdir(SRC_DIR))
my008_match = {}
source_file = '../From_SRLF/srlf_data.tsv'
key_fields = ['bib_id', 'bib_format', 'isbn_issn', 'oclc_number', 'author', 'title', 'edition', 'imprint', 'extent_300','language', 'location_code', 'location_name', 'mfhd_id','item_id', 'item_barcode', 'item_enum', 'item_type_name', 'free_text', 'item_status_desc', 'item_status_date']
key_fields_out =  ['bib_id', 'bib_format', 'isbn_issn', 'oclc_number', 'author', 'title', 'edition', 'imprint', 'extent_300','language', 'location_code', 'location_name', 'mfhd_id','item_id', 'item_barcode', 'item_enum', 'item_type_name', 'free_text', 'item_status_desc', 'item_status_date', 'matchkey','oclcnumber_enum_key', 'pub_date', 'lc_class', 'enum_key']
biband008_fields = ['bib_id', 'field008']
myinputfile = csv.DictReader(open(source_file, 'rb'), fieldnames=key_fields, delimiter='\t', quotechar = '"', quoting = csv.QUOTE_NONE)
my008 = csv.DictReader(open('../From_SRLF/srlf_data_20141219_gd.out', 'rb'), fieldnames=biband008_fields, delimiter='\t', quotechar = '', quoting = csv.QUOTE_NONE)
for inrec in my008:
	my008_match[inrec['bib_id']] = inrec['field008']
key_index = {'bib_id': '035a', 'bib_format': 'LDR', 'isbn_issn': '022', 'oclc_number': '001', 'author': 'abcde', 'title': '245', 'edition': '260', 'language': '008-35-37', 'extent_300': '300', 'imprint': '260', 'location_code': '950l', 'location_name': '950', 'mfhd_id': '950','item_id': '950', 'item_barcode': '950', 'item_enum': 'none', 'item_type_name': 'none', 'free_text': 'none captured', 'item_status_desc': 'unknown', 'item_status_date': '01/01/1982', 'matchkey': 'matching', 'oclcnumber_enum_key': '', 'pub_date': '', 'lc_class': '', 'enum_key': ''}
csv_out = csv.DictWriter(open(savefile, 'w'), fieldnames=key_fields_out, delimiter = '\t', quotechar = '', quoting = csv.QUOTE_NONE)
for recordset_in in myinputfile:
	try:
		#print recordset_in
		key_index['bib_id'] = recordset_in['bib_id']
		key_index['bib_format'] = recordset_in['bib_format']
		key_index['isbn_issn'] = recordset_in['isbn_issn']
		key_index['oclc_number'] = recordset_in['oclc_number'].strip()
		key_index['author'] = recordset_in['author'].translate(string.maketrans("",""), string.punctuation)
		key_index['title'] = recordset_in['title'].translate(string.maketrans("",""), string.punctuation)
		key_index['edition'] = recordset_in['edition'].translate(string.maketrans("",""), string.punctuation)
		key_index['imprint'] = recordset_in['imprint'].translate(string.maketrans("",""), string.punctuation)
		key_index['extent_300'] = recordset_in['extent_300'].translate(string.maketrans("",""), string.punctuation)
		key_index['language'] = recordset_in['language']
		key_index['location_code'] = recordset_in['location_code']
		key_index['location_name'] = recordset_in['location_name']
		key_index['mfhd_id'] = recordset_in['mfhd_id']
		key_index['item_id'] = recordset_in['item_id']
		key_index['item_barcode'] = recordset_in['item_barcode']
		key_index['item_enum'] = recordset_in['item_enum']
		key_index['item_type_name'] = recordset_in['item_type_name']
		key_index['free_text'] = recordset_in['free_text']
		key_index['item_status_desc'] = recordset_in['item_status_desc']
		key_index['item_status_date'] = recordset_in['item_status_date']
###Matchkey
		if recordset_in['author'] == None:
			tmprec = recordset_in['title']
		else:	
			tmprec = recordset_in['title']  + ' ' + recordset_in['author']
		
		key_index['matchkey'] = fingerprint_keyer(tmprec)
		key_index['enum_key'] = numeric_keyer(key_index['item_enum'])
		key_index['lc_class'] = ''
		key_index['oclcnumber_enum_key'] = key_index['oclc_number'] + key_index['enum_key']
		try:
			key_index['pub_date'] = my008_match[key_index['bib_id']]
			key_index['pub_date'] = key_index['pub_date'][:11]
			key_index['pub_date'] = key_index['pub_date'][7:]
		except:
			key_index['pub_date'] = ''
			
#output
#		print key_index
		csv_out.writerow(key_index)			
	except Exception, err:
		print "I broke on record "
		print recordset_in
		print traceback.format_exc()
	