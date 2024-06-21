import requests, re, json
import requests
import time
import random
from hashlib import md5

from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
import csv

def test_if_zhcn(string): # Check whether it contains Chinese
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def translate(kw): # Youdao Translation, time-sensitive, 24.4.20
	if test_if_zhcn(kw):
		#!/usr/bin/env python
		# -*- encoding: utf-8 -*-
		headers = {
    	'Cookie': 'OUTFOX_SEARCH_USER_ID=-690213934@10.108.162.139; OUTFOX_SEARCH_USER_ID_NCOO=1273672853.5782404; fanyi-ad-id=308216; fanyi-ad-closed=1; ___rl__test__cookies=1659506664755',
    	'Host': 'fanyi.youdao.com',
    	'Origin': 'https://fanyi.youdao.com',
    	'Referer': 'https://fanyi.youdao.com/',
    	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    	}
		lts = str(int(time.time() * 100))
		salt = lts + str(random.randint(0, 9))
		sign_data = 'fanyideskweb' + kw + salt +'Ygy_4c=r#e#4EX^NUGUc5'
		sign = md5(sign_data.encode()).hexdigest()
		data = {
			'i': kw,
			'from': 'AUTO',
			'to': 'AUTO',
			'smartresult': 'dict',
			'client': 'fanyideskweb',
			'salt':salt,
			'sign': sign,# encrypt
			'lts': lts,# timestamp
               
			# Encrypted data
			'bv': 'f0819a82107e6150005e75ef5fddcc3b',
			'doctype': 'json',
			'version': '2.1',
			'keyfrom': 'fanyi.web',
			'action': 'FY_BY_REALTlME',
		}
 
		# Obtain the resource address
		url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
		response = requests.post(url, headers=headers, data=data)

		list_trans = response.text
		result = json.loads(list_trans)
		return result['translateResult'][0][0]['tgt']
	


# Clear Data
def clean_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    
    word_remove = ['i','feel','feeling','and','to','the','that','of']
    for word in word_remove:
        text = re.sub(r'\b'+word+r'\b', '', text, flags=re.I)
    
    text = text.lower()

    return text

# Predict new samples
def predict_sentiment(text, model, vectorizer):
    
    cleaned_text = clean_text(text)
    text_tfidf = vectorizer.transform([cleaned_text])
    
    prediction = model.predict(text_tfidf)
    probabilities = model.predict_proba(text_tfidf)

    # Find the two most likely categories and their probabilities
    top_2_predictions = np.argsort(probabilities)[0, -2:]
    # top_2_probabilities = np.take_along_axis(probabilities, top_2_predictions, axis=1)

    return top_2_predictions


def predict(example_text):
    model_file_path = 'model/GBM_0.94762_model.joblib'
    loaded_model = load(model_file_path)

    with open('data\X_train.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        X_train = [row[0] for row in reader]

    # Load the Te-Idef vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000) # The same vectorizer parameters that are used to process the training data must be the same
    tfidf_vectorizer.fit(X_train)

    # Use models to predict the sentiment of new text
    predicted_sentiment = predict_sentiment(example_text, loaded_model, tfidf_vectorizer)
	
   
    emotion_lablels = ['悲伤', '喜悦', '喜爱', '愤怒', '恐惧', '惊喜']
    Positive = ['悲伤', '愤怒', '恐惧']
    negative = ['喜悦', '喜爱', '惊喜']

    ans = ''
    for i in predicted_sentiment:
        ans += str(emotion_lablels[i])
        ans += ' '
    
    check_ans = ans.split(" ")
    if (check_ans[0] in Positive and check_ans[1] in negative) or (check_ans[1] in Positive and check_ans[0] in negative):
         ans = check_ans[0]

    return ans
     
