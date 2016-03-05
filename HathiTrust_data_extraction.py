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
import re
					
def enum_keyer(rec):
	tmp_enum_out = {}
	tmp_fields = ['enum_begin_volume','enum_end_volume','enum_begin_number','enum_end_number','enum_begin_part','enum_end_part','enum_begin_year','enum_end_year','enum_begin_rl','enum_end_rl','enum_begin_mi','enum_end_mi','enum_begin_sec','enum_end_sec','enum_begin_ser','enum_end_ser','enum_begin_sup','enum_end_sup','enum_begin_box','enum_end_box','enum_begin_month','enum_end_month','enum_begin_fasc','enum_end_fasc','enum_begin_index','enum_end_index','enum_begin_ch','enum_end_ch','enum_begin_facs','enum_end_facs','enum_begin_bull','enum_end_bull','enum_begin_book','enum_end_book','enum_begin_lvl','enum_end_lvl','enum_begin_fuz','enum_end_fuz','enum_begin_reel','enum_end_reel','enum_begin_carton','enum_end_carton','enum_begin_c','enum_end_c','enum_begin_misc','enum_end_misc','enum_err']
	for field in tmp_fields:
		tmp_enum_out[field] = ''
	tmp_err = {}
	#strip whitespace around the string
	rec = rec.strip()	
	#lowercase string
	rec = rec.lower()
	rec = re.sub('\"', '', rec)
	rec = re.sub('\+', '', rec)
	rec = re.sub('\(', '', rec)
	rec = re.sub('\)', '', rec)
	#print "orig rec", rec
	field = rec.split(' ')
	countofperiod = rec.count(".")
	for indivfield in field:
		lastvar = ''
		tmp_enum_out['misc'] = ''
#	if len(field) == 1:
		if "." in indivfield:
			tmp_enum = indivfield.split('.')
			if tmp_enum[0].startswith('v'):
				label = "volume"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('n'):
				label = "number"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('p'):
				label = "part"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('y'):
				label = "year"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('rl'):
				label = "rl"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('mi'):
				label = "mi"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('sec'):
				label = "sec"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('ser'):
				label = "ser"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('sup'):
				label = "sup"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('box'):
				label = "sec"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('mo'):
				label = "mo"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('fasc'):
				label = "fasc"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('index'):
				label = "index"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('ch'):
				label = "ch"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('facs'):
				label = "facs"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('bull'):
				label = "bull"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('bk'):
				label = "bk"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('lvl'):
				label = "lvl"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('fuz'):
				label = "fuz"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('reel'):
				label = "reel"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('carton'):
				label = "carton"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			elif tmp_enum[0].startswith('c'):
				label = "c"
				lblbeginrange = 'enum_begin_'+label
				lblendrange = 'enum_end_'+label	
				if "-" in tmp_enum[1]:
					tmp_range = tmp_enum[1].split('-')
					tmp_enum_out[lblbeginrange] = tmp_range[0].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_range[1].lstrip("0")
				else:
					tmp_enum_out[lblbeginrange] = tmp_enum[1].lstrip("0")
					tmp_enum_out[lblendrange] = tmp_enum[1].lstrip("0")
			else:
				tmp_err = tmp_enum
				#print tmp_err
		else:
			tmp_enum_out['misc'] = tmp_enum_out['misc'], indivfield
	return tmp_err, tmp_enum_out
	#if (countofperiod+2) < len(tmp_enum_out):
		#print countofperiod, "::::", rec, "::::", tmp_enum_out
		
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
#strip leading 0s from tokens
	for i in range(len(reclist)):
		reclist[i] = reclist[i].lstrip("0")
#join fragements back together
	output = ' '.join(reclist)
	output = output.strip()
	ouput = output.lstrip("0")
	return output    	

###Old setup stuff, remove once working
#searchstring = '.mrc'
savefile = '../data/output/ht/hathi.tsv'	
#SRC_DIR = './Data'
# get a list of all .mrc files in source directory
#file_list = filter(lambda x: search(searchstring, x), listdir(SRC_DIR))
my008_match = {}
source_file = '../data/ht/hathi_full_20151101.txt'
key_fields = ['volumeidentifier', 'access', 'rights', 'htrecordnumber', 'item_enum', 'source', 'source_record_number', 'oclc_numbers', 'isbn_numbers', 'issn_numbers', 'lccn_numbers', 'title', 'imprint', 'rights_determination_code', 'date_updated', 'govdoc_flag', 'pub_date', 'pub_place', 'language', 'bib_format']
key_fields_out =  ['datasource','bib_id', 'bib_format', 'govdoc_flag','isbn_issn', 'oclc_number', 'author', 'title', 'edition', 'imprint', 'extent_300','language', 'location_code', 'location_name', 'mfhd_id','item_id', 'item_barcode', 'item_enum', 'item_type_name', 'free_text', 'item_status_desc', 'item_status_date', 'matchkey','oclcnumber_enum_key', 'pub_date', 'lc_class', 'call_no', 'enum_key', 'enum_begin_volume','enum_end_volume','enum_begin_number','enum_end_number','enum_begin_part','enum_end_part','enum_begin_year','enum_end_year','enum_begin_rl','enum_end_rl','enum_begin_mi','enum_end_mi','enum_begin_sec','enum_end_sec','enum_begin_ser','enum_end_ser','enum_begin_sup','enum_end_sup','enum_begin_box','enum_end_box','enum_begin_month','enum_end_month','enum_begin_fasc','enum_end_fasc','enum_begin_index','enum_end_index','enum_begin_ch','enum_end_ch','enum_begin_facs','enum_end_facs','enum_begin_bull','enum_end_bull','enum_begin_book','enum_end_book','enum_begin_lvl','enum_end_lvl','enum_begin_fuz','enum_end_fuz','enum_begin_reel','enum_end_reel','enum_begin_carton','enum_end_carton','enum_begin_c','enum_end_c','enum_begin_misc','enum_end_misc', 'enum_err']
myinputfile = csv.DictReader(open(source_file, 'rb'), fieldnames=key_fields, delimiter='\t', quotechar = '"', quoting = csv.QUOTE_NONE)
key_index = {'bib_id': '035a', 'bib_format': 'LDR', 'isbn_issn': '022', 'oclc_number': '001', 'author': 'abcde', 'title': '245', 'edition': '260', 'language': '008-35-37', 'extent_300': '300', 'imprint': '260', 'location_code': '950l', 'location_name': '950', 'mfhd_id': '950','item_id': '950', 'item_barcode': '950', 'item_enum': 'none', 'item_type_name': 'none', 'free_text': 'none captured', 'item_status_desc': 'unknown', 'item_status_date': '01/01/1982', 'matchkey': 'matching', 'oclcnumber_enum_key': '', 'pub_date': '', 'lc_class': '', 'enum_key': ''}
csv_out = csv.DictWriter(open(savefile, 'w'), fieldnames=key_fields_out, delimiter = '\t', quotechar = '', quoting = csv.QUOTE_NONE)
for recordset_in in myinputfile:
	try:
		#print recordset_in
		key_index['datasource'] = "HATHI"
		key_index['bib_id'] = recordset_in['volumeidentifier']
		key_index['bib_format'] = recordset_in['bib_format']
		key_index['isbn_issn'] = recordset_in['isbn_numbers'], " ", recordset_in['issn_numbers']
		key_index['oclc_number'] = recordset_in['oclc_numbers'].strip()
		key_index['author'] = ''
		key_index['title'] = recordset_in['title'].translate(string.maketrans("",""), string.punctuation)
		key_index['edition'] = ''
		key_index['imprint'] = recordset_in['imprint'].translate(string.maketrans("",""), string.punctuation)
		key_index['extent_300'] = ''
		key_index['language'] = recordset_in['language']
		key_index['location_code'] = recordset_in['source']
		key_index['location_name'] = recordset_in['source']
		key_index['mfhd_id'] = ''
		key_index['item_id'] = recordset_in['volumeidentifier']
		key_index['item_barcode'] = recordset_in['htrecordnumber']
		key_index['item_enum'] = recordset_in['item_enum']
		key_index['item_type_name'] = recordset_in['rights_determination_code']
		key_index['free_text'] = recordset_in['rights']
		key_index['item_status_desc'] = recordset_in['access']
		key_index['item_status_date'] = recordset_in['date_updated']
###Matchkey
		tmprec = recordset_in['title']
		
		key_index['matchkey'] = fingerprint_keyer(tmprec)
		key_index['enum_key'] = numeric_keyer(key_index['item_enum'])
		key_index['lc_class'] = ''
		key_index['oclcnumber_enum_key'] = key_index['oclc_number'] + key_index['enum_key']
###generate normalized enumeration
		enum_err, enum_normalized = enum_keyer(key_index['item_enum'])
		key_index['enum_err'] = ' '.join(enum_err)
		tmp_fields = ['enum_begin_volume','enum_end_volume','enum_begin_number','enum_end_number','enum_begin_part','enum_end_part','enum_begin_year','enum_end_year','enum_begin_rl','enum_end_rl','enum_begin_mi','enum_end_mi','enum_begin_sec','enum_end_sec','enum_begin_ser','enum_end_ser','enum_begin_sup','enum_end_sup','enum_begin_box','enum_end_box','enum_begin_month','enum_end_month','enum_begin_fasc','enum_end_fasc','enum_begin_index','enum_end_index','enum_begin_ch','enum_end_ch','enum_begin_facs','enum_end_facs','enum_begin_bull','enum_end_bull','enum_begin_book','enum_end_book','enum_begin_lvl','enum_end_lvl','enum_begin_fuz','enum_end_fuz','enum_begin_reel','enum_end_reel','enum_begin_carton','enum_end_carton','enum_begin_c','enum_end_c','enum_begin_misc','enum_end_misc','enum_err']
		for field in tmp_fields:
			key_index[field] = enum_normalized[field]
###Process008
		try:
			key_index['pub_date'] = recordset_in['pub_date']
		except:
			key_index['pub_date'] = ''
		try:
			key_index['govdoc_flag'] = recordset_in['govdoc_flag']
		except:
			key_index['govdoc_flag'] = ''
			
#output
#		print key_index
		csv_out.writerow(key_index)			
	except Exception, err:
		print "I broke on record "
		print recordset_in
		print traceback.format_exc()
	