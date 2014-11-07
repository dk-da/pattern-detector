# -*- coding: utf-8 -*-$

def check(obj):
	return obj['pos0'] == 'COMPOUND'  and\
		len(obj['token0'].decode('utf-8')) > 1 and\
		( pattern1(obj) or pattern2(obj) or pattern3(obj) or pattern4(obj) )

def pattern1(obj):
	if obj['token+1'] == '에서':
		if obj['pos-2'] == 'ADDR':
			if obj['pos-1'] == 'COMPOUND':
				return True
		if obj['pos-1'] == 'ADDR':
			return True
		if obj['token+2'] == '개최':
			return True
		if obj['token0'] == '인근':
			return False
	
	if obj['token+2'] == '에서':
		if obj['pos+1'] == 'COMPOUND':
			return True
	
	if obj['token+3'] == '에서':
		if obj['pos+1'] == 'COMPOUND':
			if obj['pos+2'] == 'COMPOUND':
				return True
	
	return False

def pattern2(obj):
	if obj['pos-2'] == 'SN':
		if obj['token-1'] == '일':
			if obj['token0'] != '오전' and obj['token0'] != '오후' and obj['token0'] != '새벽' and obj['token0'] != '저녁':
				if obj['pos+1'] != 'JKO' and not obj['pos+1'].startswith('XSV') and not obj['pos+1'].startswith('XSA'):
					if obj['pos+2'] != 'JKO':
						return True
	return False

def pattern3(obj):
	if obj['pos-1'] == 'ADDR':
		if obj['pos-2'] == 'ADDR':
			return True
	return False

def pattern4(obj):
	if obj['pos+1'] == 'SN':
		if obj['token+2'] == '층':
			if obj['token0'] != '지상' and obj['token0'] != '지하':
				return True
	return False

