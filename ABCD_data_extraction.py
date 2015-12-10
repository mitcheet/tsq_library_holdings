#!/usr/bin/env python

import csv
from pymarc import reader
from os import listdir
from re import search
import string  
import thread
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
	return output    
	      
searchstring = '.mrc'
savefile = 'nrlf.csv'
# Iteration over all arguments:
for eachArg in sys.argv:   
        searchstring = eachArg
        savefile = './'+eachArg+'.csv'
SRC_DIR = './Data'

# get a list of all .mrc files in source directory
file_list = filter(lambda x: search(searchstring, x), listdir(SRC_DIR))
match_auth = ''
key_index = {'bib_id': '035a', 'bib_format': 'LDR', 'isbn_issn': '022', 'oclc_number': '001', 'author': 'abcde', 'title': '245', 'edition': '260', 'language': '008-35-37', 'extent_300': '300', 'imprint': '260', 'location_code': '950l', 'location_name': '950', 'mfhd_id': '950','item_id': '950', 'item_barcode': '950', 'item_enum': 'none', 'item_type_name': 'none', 'free_text': 'none captured', 'item_status_desc': 'unknown', 'item_status_date': '01/01/1982', 'matchkey': 'matching', 'oclcnumber_enum_key':'', 'pub_date':'', 'lc_class':'', 'enum_key':''}
key_fields = ['bib_id', 'bib_format', 'isbn_issn', 'oclc_number', 'author', 'title', 'edition', 'language', 'extent_300', 'imprint', 'location_code', 'location_name', 'mfhd_id','item_id', 'item_barcode', 'item_enum', 'item_type_name', 'free_text', 'item_status_desc', 'item_status_date', 'matchkey','oclcnumber_enum_key', 'pub_date', 'lc_class', 'enum_key']
csv_out = csv.DictWriter(open(savefile, 'w'), fieldnames=key_fields, delimiter = '\t', quotechar = '', quoting = csv.QUOTE_NONE)
for item in file_list:
	fd = file(SRC_DIR + '/' + item, 'r')
	print item
	reader = reader.MARCReader(fd, hide_utf8_warnings=True, to_unicode=False) 
	for record in reader:
		tmptitle = ''
		tmpauthor = ''
###bib_id
		try:
			tmpfields = record.get_fields('035')
			for field in tmpfields:
				tmpfield = field.value()
				if tmpfield.startswith('.b'):
					key_index['bib_id'] = tmpfield
		except Exception, err:
			print traceback.format_exc()
			break
###bib_format	
		try:
			tmpfield = record.leader
			#print tmpfield
			key_index['bib_format'] = tmpfield[:8]
			key_index['bib_format'] = key_index['bib_format'][6:]
		except Exception, err:
			print traceback.format_exc()
			break
###isbn_issn	
		try:
			if key_index['bib_format'] == 'am':
				key_index['isbn_issn'] = record.isbn()
			if key_index['bib_format'] == 'as':
				key_index['isbn_issn'] = record.issn()
		except Exception, err:
			#print traceback.format_exc()
			a = 1
###oclc_number	
		try:
			tmpfields = record.get_fields('001')
			for field in tmpfields:
				tmpfield = field.value()
				key_index['oclc_number'] = tmpfield.strip()
		except Exception, err:
			print traceback.format_exc()
			break
##author	
		tmpauthor = ''
		try:
			tmpauthor = record.author()
			key_index['author'] = tmpauthor.translate(string.maketrans("",""), string.punctuation)
		except:
			tmpauthor = "abcde"
			key_index['author'] = tmpauthor
			
###title	
		try:
			tmptitle = record.title()
			key_index['title'] = tmptitle.translate(string.maketrans("",""), string.punctuation)
			#print key_index['title']
		except Exception, err:
			print traceback.format_exc()
			break
###'edition': '260'
		try:
			tmpfields = record.get_fields('260')
			for field in tmpfields:
				tmpfield = field.value()
				key_index['edition'] = tmpfield.translate(string.maketrans("",""), string.punctuation)
		except Exception, err:
			print traceback.format_exc()
			break				
###'language', '008-35-37', pubdate
		try:
			tmpfields = record.get_fields('008')
			for field in tmpfields:
				tmpfield = field.value()
				key_index['language'] = tmpfield[:38]
				key_index['language'] = key_index['language'][35:]
				key_index['pub_date'] = tmpfield[:11]
				key_index['pub_date'] = key_index['pub_date'][7:]
		except Exception, err:
			print traceback.format_exc()
			break
###'extent_300': '300',
		try:
			tmpfields = record.get_fields('300')
			for field in tmpfields:
				tmpfield = field.value()
				key_index['extent_300'] = tmpfield.translate(string.maketrans("",""), string.punctuation)
		except Exception, err:
			print traceback.format_exc()
			break
###'imprint': '260'
		try:
			tmpfields = record.get_fields('260')
			for field in tmpfields:
				tmpfield = field.value()
				key_index['imprint'] = tmpfield.translate(string.maketrans("",""), string.punctuation)
		except Exception, err:
			print traceback.format_exc()
			break
###'item_enum': 'none', 'item_type_name': 'none', 'free_text': 'none captured', 'item_status_desc': 'unknown', 'item_Status_Date': '01/01/1982'
		key_index['mfhd_id'] = "mfhd_id"
		key_index['item_enum'] = "item_enum"
		key_index['item_type_name'] = "item_type_name"
		key_index['free_text'] = "free_text"						
		key_index['item_status_desc'] = "item_status_desc"
		key_index['item_status_date'] = "01/01/1982"
###Matchkey

		if key_index['author'] == None:
			tmprec = key_index['title']
		else:	
			tmprec = key_index['title']  + ' ' + key_index['author']
		key_index['matchkey'] = fingerprint_keyer(tmprec)	
		
###', 'pubdate':'', ', 'govdoc_flag':'', 

###'location_code': '950l' and location_name, 'enum_key':'', 'oclcnumber_enum_key':', 'lc_class':'
		try:
			tmpfields = record.get_fields('950')
			for field in tmpfields:
				try:
					#print field
					#print field.get_subfields('c')
					if field.get_subfields('l')[0].startswith('n'):
						key_index['location_name'] = key_index['location_code'] = field.get_subfields('l')[0]
						key_index['item_barcode'] = (field.get_subfields('i')[0])
						try:
							key_index['lc_class'] = (field.get_subfields('a')[0][:2])
						except:
							key_index['lc_class'] = ''
						key_index['item_id'] = (field.get_subfields('y')[0])
						if field.get_subfields('c'):
							#print field
							key_index['item_enum'] = field.get_subfields('c')[0]
							key_index['enum_key'] = numeric_keyer(field.get_subfields('c')[0])
							key_index['oclcnumber_enum_key'] = key_index['oclc_number'] + key_index['enum_key']
							#print key_index
						else:
							key_index['item_enum'] = ''
							key_index['enum_key'] = ''
							key_index['oclcnumber_enum_key'] = key_index['oclc_number']
	
						csv_out.writerow(key_index)
				except Exception, err:
					print "No location code", field
					print traceback.format_exc()

		except Exception, err:
			print field
			print record
			print traceback.format_exc()
			break