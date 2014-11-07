# -*- coding: utf-8 -*-
import json
from eunjeon import ma
from patterns import check


def make_addr_dic():
	d = {}
	with open('addr_term_list.txt') as f:
		for line in f:
			line = line.strip()
			term, tag = line.split()
			if tag == 'nlj40':
				continue
			if term in d:
				pass
			else:
				d[term] = tag
	with open('aoi_term_list.txt') as f:
		for line in f:
			line = line.strip()
			term, tag = line.split()
			if tag == 'nlj40':
				continue
			if term in d:
				pass
			else:
				d[term] = tag

	return d

#addr_dic = make_addr_dic()

with open('training.json') as f:
	for line in f:
		article_list = json.loads(line)

t = 0
f = 0
recall_list = []
for article in article_list:
	print '#### START OF ARTICLE ####'
	print article['contents']
	print '#### END OF ARTICLE ####'
	print ''
	print '#### START of detecting result ####'

	poi_list = article['poi']

	recall_mother_set = set()
	recall_son_set = set()
	for poi in poi_list:
		recall_mother_set.add(poi)
	
	result = ma(article['contents'])
	
	token_list = []
	token_list.append(result[0])  # padding
	token_list.append(result[0])  # padding
	token_list.append(result[0])  # padding
	for token in result:
		token_list.append(token)
		if token['token'] == '.':
			token_list.append(result[0])  # sentence segmentation
			token_list.append(result[0])  # sentence segmentation
			token_list.append(result[0])  # sentence segmentation
			token_list.append(result[0])  # sentence segmentation
	token_list.append(result[0])  # padding
	token_list.append(result[0])  # padding
	token_list.append(result[0])  # padding
	

	for i, token in enumerate(token_list):
		if token['pos'] == 'BOS/EOS':
			continue
		
		obj = {}
		obj['token0'] = token_list[i]['token']
		obj['pos0'] = token_list[i]['pos']
		obj['token-1'] = token_list[i-1]['token']
		obj['pos-1'] = token_list[i-1]['pos']
		obj['token+1'] = token_list[i+1]['token']
		obj['pos+1'] = token_list[i+1]['pos']
		obj['token-2'] = token_list[i-2]['token']
		obj['pos-2'] = token_list[i-2]['pos']
		obj['token+2'] = token_list[i+2]['token']
		obj['pos+2'] = token_list[i+2]['pos']
		obj['token-3'] = token_list[i-3]['token']
		obj['pos-3'] = token_list[i-3]['pos']
		obj['token+3'] = token_list[i+3]['token']
		obj['pos+3'] = token_list[i+3]['pos']
		obj['token-4'] = token_list[i-4]['token']
		obj['pos-4'] = token_list[i-4]['pos']
		obj['token+4'] = token_list[i+4]['token']
		obj['pos+4'] = token_list[i+4]['pos']

		if check(obj):
			if obj['token0'] in poi_list:
				print '# Result:', True
				t += 1
				recall_son_set.add(obj['token0'])
			else:
				print '# Result:', False
				f += 1

		#if check(obj):
		#if obj['token0'] in poi_list:
			print obj['token-4'], obj['pos-4']
			print obj['token-3'], obj['pos-3']
			print obj['token-2'], obj['pos-2']
			print obj['token-1'], obj['pos-1']
			print '*', obj['token0'], obj['pos0']
			print obj['token+1'], obj['pos+1']
			print obj['token+2'], obj['pos+2']
			print obj['token+3'], obj['pos+3']
			print obj['token+4'], obj['pos+4']
			print ''

		recall = float(len(recall_son_set)) / float(len(recall_mother_set))
		recall_list.append(recall)
	
	print '#### END of detecting result ####'
	print ''


print "tp:", t
print "fp:", f
print 'precision:', float(t) / float(t + f)

recall_sum = 0.0
for recall in recall_list:
	recall_sum += recall
recall_final = recall_sum / float(len(recall_list))

print 'recall:', recall_final

