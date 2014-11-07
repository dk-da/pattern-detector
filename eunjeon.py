# -*- coding: utf-8 -*-
from pprint import pprint
import MeCab
import sys 
import string
import re


def ma(sentence):
	if type(sentence) == unicode:
		sentence = sentence.encode('utf-8')

	sentence = re.sub('([!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~])', r' \1 ', sentence)
	sentence = re.sub('\s{2,}', ' ', sentence)
	
	splited = sentence.split()
	
	t = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ko-dic")
	
	result_list = []
	
	m = t.parseToNode(sentence)
	
	while m:
		surface = m.surface
		features = m.feature.split(",")
		
		result = {}
		for i, split in enumerate(splited):
			idx =  split.find(surface)
			if idx >= 0:
				result['position'] = i+1
				splited[i] = splited[i][len(surface):]
				break
		
		result['token'] = m.surface
		result['pos'] = features[0]
		result['semantic'] = features[1]
		if result['pos'] == 'BOS/EOS':
			result['position'] = 0
		
		result_list.append(result)
		m = m.next
	
	chunk_list = []
	token = []
	for i, result in enumerate(result_list):
		if i == 0:
			prev = None
		else:
			prev = result_list[i-1]
		
		curr = result_list[i]
		
		if i == len(result_list) - 1:
			next = None
		else:
			next = result_list[i+1]
		
		
		if next == None or curr['position'] != next['position']:
			token.append(curr)
			chunk_list.extend(_chunking(token))
			token = []
		else:
			token.append(curr)
	
	for i, _ in enumerate(chunk_list):
		if chunk_list[i]['semantic'] == '지명':
			chunk_list[i]['pos'] = 'ADDR'
	
	return chunk_list

def _chunking(token):
	if type(token) != list or len(token) == 0:
		print "[_chunking] invalid input"
		exit(1)
	
	position = token[0]['position']
	chunk_list = []
	
	if len(token) == 1:
		chunk = token[0]
		if chunk['pos'].startswith('N'):
			chunk['pos'] = 'COMPOUND'
		chunk_list.append(chunk)
		return chunk_list
	
	chunk = {}
	for i, mol in enumerate(token):
		#########################
		if i == 0:
			prev = None
		else:
			prev = token[i-1]
		
		curr = token[i]
		
		if i == len(token)-1:
			next = None
		else:
			next = token[i+1]
		#########################
		
		if curr['pos'].startswith('N') or curr['pos'] == 'XPN' or curr['pos'] == 'XSN' or curr['pos'] == 'XR' or curr['pos'] == 'MM':
			if prev == None or (not prev['pos'].startswith('N') and prev['pos'] != 'XPN' and prev['pos'] != 'XSN' and prev['pos'] != 'XR' and prev['pos'] != 'MM'):
				chunk = {}
				chunk['token'] = curr['token']
				chunk['pos'] = 'COMPOUND'
				chunk['semantic'] = '*'
				chunk['position'] = position
			else:
				chunk['token'] += curr['token']
			
			if next == None or (not next['pos'].startswith('N') and next['pos'] != 'XPN' and next['pos'] != 'XSN' and next['pos'] != 'XR' and next['pos'] != 'MM'):
				chunk_list.append(chunk)
				chunk = {}
		else:
			chunk_list.append(curr)
			chunk = {}
	
	return chunk_list


def make_addr_dic():
	d = {}
	with open('addr_term_list.txt') as f:
		for line in f:
			line = line.strip()
			term, tag = line.split()
			if tag == 'nlj40':
				continue
			if term in d:
				continue
			else:
				d[term] = tag 
	with open('aoi_term_list.txt') as f:
		for line in f:
			line = line.strip()
			term, tag = line.split()
			if tag == 'nlj40':
				continue
			if term in d:
				continue
			else:
				d[term] = tag 
	return d
#addr_dic = make_addr_dic()


if __name__ == '__main__':
	#s = '서울에 사는 임동권이 심은 무궁화꽃이 피었습니다. 나는 오늘도 달린다. 시골식당은 맛있다. 이명박식당은 맛없다. 시골 이명박식당 '
	#s = "130322 [인천/청라] 강남 샤브샤브 칼국수 부대찌개"
	s = "3일부터 서울에서 개최되는 '국제산업박람회' 준비를 위해"
	result= ma(s)
	
	print s
	for elem in result:
		print elem['token'], elem['pos'], elem['semantic'], elem['position']

