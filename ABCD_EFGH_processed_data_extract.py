#!/usr/bin/env python
 
import csv
from pymarc import reader
from os import listdir
import re
from re import search
import string  
#import Levenshtein
#import thread
import time
import sys, getopt
import traceback

#Key generators - Numeric
def numeric_keyer(rec):
	recarray = reclist = output = ""
	rec = rec.strip()	#strip whitespace around the string
#lowercase string
	rec = rec.lower()
#remove all non-alpha num
	rec = rec.translate(string.maketrans("",""), string.punctuation)
	#rec = rec.translate(string.maketrans("",""), string.ascii_letters)
#split by whitespace split
	recarray = rec.split(" ")
#order tokens and dedup
	reclist = sorted(list(set(recarray)))
	reclist = [i for i in reclist if i != 'none']
#join fragements back together
	output = ' '.join(reclist)
	output = output.strip()
	output = output.lstrip("0")
	return output  
	
	
Unified_key_fs_out = ['SourceRLF', 'NRLF_bib_id','SRLF_bib_id','bib_format', 'isbn_issn','oclc_number','author', 'title',  'edition', 'language', 'extent_300', 'imprint','location_code','location_name','mfhd_id','item_id','item_barcode', 'NRLF_barcode', 'item_enum', 'NRLF_item_enum', 'item_type_name','free_text', 'item_status_desc','item_status_date', 'matchkey', 'oclcnumber_enum_key', 'pub_date', 'lc_class','enum_key', 'WESTTitle','WESTPrint ISSN','WESTPublisher','WESTOCLC Number','WESTProgram Abbrev','WESTnstitution Name','WESTCLC Symbol','WESTCLC HLC','WESTSummary Holdings/Materials Specified','WESTRecord Updated']
source_file = "../../output/rlf_unified_output_w_west.tsv"
myinputfile = csv.DictReader(open(source_file, 'rb'), fieldnames=Unified_key_fs_out, delimiter='\t', quotechar = '"', quoting = csv.QUOTE_NONE)
for inrec in myinputfile:
	#Strip spaces from searchstring
	#compnum = re.sub(r' ', '', inrec[searchstring])
	#Generate a numeric keyed version of the searchstring
	#inrec[searchstring] = numeric_keyer(inrec[searchstring])
	#Write out the list of variables with placeholders for matching
	#Unified_key_fs_out = [0'SourceRLF', 1'NRLF_bib_id',       2'SRLF_bib_id',        3'bib_format',        4'isbn_issn',        5'oclc_number',        6'author',        7'title',        8'edition',        9'language',        10'extent_300',        11'imprint',        12'location_code',        13'location_name',        14'mfhd_id',       15'item_id',        16'item_barcode', 17'NRLF_barcode',       18'item_enum', 19'NRLF_item_enum',        20'item_type_name',        21'free_text',        22'item_status_desc',        23'item_status_date', 24'matchkey',          25'oclcnumber_enum_key',        26'pub_date',        27'lc_class',        28'enum_key', 29'WESTTitle',30'WESTPrint ISSN',31'WESTPublisher',32'WESTOCLC Number',33'WESTProgram Abbrev',34'WESTnstitution Name',35'WESTCLC Symbol',36'WESTCLC HLC',37'WESTSummary Holdings/Materials Specified',38'WESTRecord Updated']
	#recordset[compnum] = ['SRLF', '', inrec['bib_id'], inrec['bib_format'], inrec['isbn_issn'], inrec['oclc_number'], inrec['author'], inrec['title'], inrec['edition'], inrec['language'], inrec['extent_300'], inrec['imprint'], inrec['location_code'], '', inrec['mfhd_id'], inrec['item_id'], inrec['item_barcode'], '', inrec['item_enum'], '',  inrec['item_type_name'], inrec['free_text'], inrec['item_status_desc'], inrec['item_status_date'],  searchstring, inrec['oclcnumber_enum_key'], inrec['pub_date'], inrec['lc_class'], inrec['enum_key'],'','','','','','','','','','']
	print numeric_keyer(inrec['title']) + '\t' + inrec['title'] + '\t' + inrec['item_enum'] + '\t' + inrec['NRLF_item_enum']