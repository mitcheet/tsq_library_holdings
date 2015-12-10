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
#Input key fields
EFGH_key_fields_out =  ['bib_id', 'bib_format', 'isbn_issn', 'oclc_number', 'author', 'title', 'edition', 'imprint', 'extent_300','language', 'location_code', 'location_name', 'mfhd_id','item_id', 'item_barcode', 'item_enum', 'item_type_name', 'free_text', 'item_status_desc', 'item_status_date', 'matchkey','oclcnumber_enum_key', 'pub_date', 'lc_class', 'enum_key']
ABCD_key_fields_out =  ['bib_id', 'bib_format', 'isbn_issn', 'oclc_number', 'author', 'title', 'edition', 'imprint', 'extent_300', 'language', 'location_code', 'location_name', 'mfhd_id','item_id', 'item_barcode', 'item_enum', 'item_type_name', 'free_text', 'item_status_desc', 'item_status_date', 'matchkey','oclcnumber_enum_key', 'pub_date', 'lc_class', 'enum_key']
WEST_key_fields_out =  ['Title','Print ISSN','Publisher','OCLC Number','Program Abbrev','Institution Name','OCLC Symbol','OCLC HLC','Summary Holdings/Materials Specified','Record Updated']
#Full list of fields - just for documentation
#Unified_key_fields_out = ['SourceRLF', 'MatchedRLF_bibid', 'bib_id', 'bib_format', 'isbn_issn', 'oclc_number', 'author', 'title', 'edition', 'language', 'extent_300', 'imprint', 'location_code', 'location_name', 'mfhd_id','item_id', 'item_barcode', , 'MatchedRLF_barcode', 'item_enum', , 'MatchedRLF_item_enum', 'item_type_name', 'free_text', 'item_status_desc', 'item_status_date', 'matchkey','oclcnumber_enum_key', 'pub_date', 'lc_class', 'enum_key','WESTTitle','WESTPrint ISSN','WESTPublisher','WESTOCLC Number','WESTProgram Abbrev','WESTnstitution Name','WESTCLC Symbol','WESTCLC HLC','WESTSummary Holdings/Materials Specified','WESTRecord Updated']

#Source files - adjust to meet current filesystem
ABCD_source_file = "../rlfdata/ABCD_data_full.csv"
EFGH_source_file = "../rlfdata/EFGH_data_full.csv"
WEST_source_file = "../rlfdata/west.tsv"

#Key generators - Numeric
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
	output = output.lstrip("0")
	return output  
	
#Function to grap comparison string from command line	
if len(sys.argv) == 1:
	print ABCD_key_fields_out
else:
	for eachArg in sys.argv:   
		searchstring = eachArg

#Set default variables for gathering results
oclckey_match = {}
recordset = {}
recordset_west = {}


#open EFGH and read in entire oclc number set, bibiid); Use EFGH as base due to better metadata
myinputfile = csv.DictReader(open(EFGH_source_file, 'rb'), fieldnames=EFGH_key_fields_out, delimiter='\t', quotechar = '"', quoting = csv.QUOTE_NONE)
for inrec in myinputfile:
	#Strip spaces from searchstring
	compnum = re.sub(r' ', '', inrec[searchstring])
	#Generate a numeric keyed version of the searchstring
	inrec[searchstring] = numeric_keyer(inrec[searchstring])
	#Write out the list of variables with placeholders for matching
	#Unified_key_fs_out = [0'SourceRLF', 1'ABCD_bib_id',       2'EFGH_bib_id',        3'bib_format',        4'isbn_issn',        5'oclc_number',        6'author',        7'title',        8'edition',        9'language',        10'extent_300',        11'imprint',        12'location_code',        13'location_name',        14'mfhd_id',       15'item_id',        16'item_barcode', 17'ABCD_barcode',       18'item_enum', 19'ABCD_item_enum',        20'item_type_name',        21'free_text',        22'item_status_desc',        23'item_status_date', 24'matchkey',          25'oclcnumber_enum_key',        26'pub_date',        27'lc_class',        28'enum_key', 29'WESTTitle',30'WESTPrint ISSN',31'WESTPublisher',32'WESTOCLC Number',33'WESTProgram Abbrev',34'WESTnstitution Name',35'WESTCLC Symbol',36'WESTCLC HLC',37'WESTSummary Holdings/Materials Specified',38'WESTRecord Updated']
	recordset[compnum] = ['EFGH', '', inrec['bib_id'], inrec['bib_format'], inrec['isbn_issn'], inrec['oclc_number'], inrec['author'], inrec['title'], inrec['edition'], inrec['language'], inrec['extent_300'], inrec['imprint'], inrec['location_code'], '', inrec['mfhd_id'], inrec['item_id'], inrec['item_barcode'], '', inrec['item_enum'], '',  inrec['item_type_name'], inrec['free_text'], inrec['item_status_desc'], inrec['item_status_date'],  searchstring, inrec['oclcnumber_enum_key'], inrec['pub_date'], inrec['lc_class'], inrec['enum_key'],'','','','','','','','','','']


#open ABCD and iterate through print where there are matches; in case of a match update hash values; otherwise write out new row
myinputfile = csv.DictReader(open(ABCD_source_file, 'rb'), fieldnames=ABCD_key_fields_out, delimiter='\t', quotechar = '"', quoting = csv.QUOTE_NONE)
for inrec in myinputfile:
	compnum = re.sub(r' ', '', inrec[searchstring])
	try:
		inrec[searchstring] = numeric_keyer(inrec[searchstring])
	except:
		continue
	#if the comparison field is already a location - then we have a match - Important - You must do bib or item-level comparisons here and accept the output (e.g. a bib-level output gives considerably fewer rows)
	if compnum in recordset:
		#Update keys where there is a match - write out bib id, barcode and enumeration
		recordset[compnum][1] = inrec['bib_id']
		recordset[compnum][17] = inrec['item_barcode']
		recordset[compnum][19] = inrec['item_enum']
		recordset[compnum][13] = inrec['location_code']
	else:
		#Otherwise we have a new record - write it to the dataset
		#Unified_key_fs_out = [0'SourceRLF', 1'ABCD_bib_id',       2'EFGH_bib_id',        3'bib_format',        4'isbn_issn',        5'oclc_number',        6'author',        7'title',        8'edition',        9'language',        10'extent_300',        11'imprint',        12'location_code',        13'location_name',        14'mfhd_id',       15'item_id',        16'item_barcode', 17'ABCD_barcode',       18'item_enum', 19'ABCD_item_enum',        20'item_type_name',        21'free_text',        22'item_status_desc',        23'item_status_date', 24'matchkey',          25'oclcnumber_enum_key',        26'pub_date',        27'lc_class',        28'enum_key', 29'WESTTitle',30'WESTPrint ISSN',31'WESTPublisher',32'WESTOCLC Number',33'WESTProgram Abbrev',34'WESTnstitution Name',35'WESTCLC Symbol',36'WESTCLC HLC',37'WESTSummary Holdings/Materials Specified',38'WESTRecord Updated']
		recordset[compnum] = ['ABCD', inrec['bib_id'], '', inrec['bib_format'], inrec['isbn_issn'], inrec['oclc_number'], inrec['author'], inrec['title'], inrec['edition'], inrec['language'], inrec['extent_300'], inrec['imprint'], '', inrec['location_code'], inrec['mfhd_id'], inrec['item_id'], '', inrec['item_barcode'],  '', inrec['item_enum'], inrec['item_type_name'], inrec['free_text'], inrec['item_status_desc'], inrec['item_status_date'],  searchstring, inrec['oclcnumber_enum_key'], inrec['pub_date'], inrec['lc_class'], inrec['enum_key'],'','','','','','','','','','']
	
	
#Prototype for Shared Print matches - Open WEST file and read in entire set into a variable
myinputfile = csv.DictReader(open(WEST_source_file, 'rb'), fieldnames=WEST_key_fields_out, delimiter='\t', quotechar = '"', quoting = csv.QUOTE_NONE)
for inrec in myinputfile:
	compnum = re.sub(r' ', '', inrec['OCLC Number'])
	try:
		compnum = numeric_keyer(inrec['OCLC Number'])
	except:
		continue
	#inrec['OCLC Number'] = numeric_keyer(inrec['OCLC Number'])
	recordset_west[compnum] = [inrec['Title'], inrec['Print ISSN'], inrec['Publisher'], inrec['OCLC Number'],inrec['Program Abbrev'],inrec['Institution Name'],inrec['OCLC Symbol'],inrec['OCLC HLC'],inrec['Summary Holdings/Materials Specified'],inrec['Record Updated']]

#Final comparison and output - if we had multiple shared print groups to compare against or multiple holding locations we would need to iterate each time through - in other words - this is lazy	
#Print out the document header
print 'RecordSourceRLF' + '	' +  'ABCD_bibid' + '	' +  'EFGHbib_id' + '	' +  'bib_format' + '	' +  'isbn_issn' + '	' +  'oclc_number' + '	' +  'author' + '	' +  'title' + '	' +  'edition' + '	' +  'language' + '	' +  'extent_300' + '	' +  'imprint' + '	' +  'EFGHlocation_code' + '	' +  'ABCDlocation_code' + '	' +  'mfhd_id' + '	' + 'item_id' + '	' +  'EFGHitem_barcode' + '	' +  'ABCDRLF_barcode' + '	' +  'EFGHitem_enum' + '	' +  'ABCDRLF_item_enum' + '	' +  'item_type_name' + '	' +  'free_text' + '	' +  'item_status_desc' + '	' +  'item_status_date' + '	' +  'matchkey' + '	' + 'oclcnumber_enum_key' + '	' +  'pub_date' + '	' +  'lc_class' + '	' +  'enum_key' + '	' + 'WESTTitle' + '	' + 'WESTPrint ISSN' + '	' + 'WESTPublisher' + '	' + 'WESTOCLC Number' + '	' + 'WESTProgram Abbrev' + '	' + 'WESTnstitution Name' + '	' + 'WESTCLC Symbol' + '	' + 'WESTCLC HLC' + '	' + 'WESTSummary Holdings/Materials Specified' + '	' + 'WESTRecord Updated'
for inrec in recordset:
	#if we have a matching record in west by OCLC Number
	if recordset[inrec][5] in recordset_west and recordset[inrec][5] > '':
		print recordset[inrec][0] + '\t', recordset[inrec][1] + '\t', recordset[inrec][2] + '\t', recordset[inrec][3] + '\t', recordset[inrec][4] + '\t', recordset[inrec][5] + '\t', recordset[inrec][6] + '\t', recordset[inrec][7] + '\t', recordset[inrec][8] + '\t', recordset[inrec][9] + '\t', recordset[inrec][10] + '\t', recordset[inrec][11] + '\t', recordset[inrec][12] + '\t', recordset[inrec][13] + '\t', recordset[inrec][14] + '\t', recordset[inrec][15] + '\t', recordset[inrec][16] + '\t', recordset[inrec][17] + '\t', recordset[inrec][18] + '\t', recordset[inrec][19] + '\t', recordset[inrec][20] + '\t', recordset[inrec][21] + '\t', recordset[inrec][22] + '\t', recordset[inrec][23] + '\t', recordset[inrec][24] + '\t', recordset[inrec][25] + '\t', recordset[inrec][26] + '\t', recordset[inrec][27] + '\t', recordset[inrec][28] + '\t' + recordset_west[recordset[inrec][5]][0] + '\t' + recordset_west[recordset[inrec][5]][1] + '\t' + recordset_west[recordset[inrec][5]][2] + '\t' + recordset_west[recordset[inrec][5]][3] + '\t' + recordset_west[recordset[inrec][5]][4] + '\t' + recordset_west[recordset[inrec][5]][5]+ '\t' + recordset_west[recordset[inrec][5]][6] + '\t' + recordset_west[recordset[inrec][5]][7]+ '\t' + recordset_west[recordset[inrec][5]][8]+ '\t' + recordset_west[recordset[inrec][5]][9] + '\t' + 'WESTMATCH'
	else:
		print recordset[inrec][0] + '\t', recordset[inrec][1] + '\t', recordset[inrec][2] + '\t', recordset[inrec][3] + '\t', recordset[inrec][4] + '\t', recordset[inrec][5] + '\t', recordset[inrec][6] + '\t', recordset[inrec][7] + '\t', recordset[inrec][8] + '\t', recordset[inrec][9] + '\t', recordset[inrec][10] + '\t', recordset[inrec][11] + '\t', recordset[inrec][12] + '\t', recordset[inrec][13] + '\t', recordset[inrec][14] + '\t', recordset[inrec][15] + '\t', recordset[inrec][16] + '\t', recordset[inrec][17] + '\t', recordset[inrec][18] + '\t', recordset[inrec][19] + '\t', recordset[inrec][20] + '\t', recordset[inrec][21] + '\t', recordset[inrec][22] + '\t', recordset[inrec][23] + '\t', recordset[inrec][24] + '\t', recordset[inrec][25] + '\t', recordset[inrec][26] + '\t', recordset[inrec][27] + '\t', recordset[inrec][28] + '\t' + 'NOMATCH'
