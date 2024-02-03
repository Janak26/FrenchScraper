import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


dataPath = "D:/Projects/FrenchCollector/data/"

prefixes = ["j'ai", "j'", "je", "tu", "il", "nous", "vous", "ils"]
suffixes = ["tu", "tu", "tu", "il", "nous", "vous", "ils", ""]

IMprefixes = ["tu", "nous", "vous"]
IMsuffixes = ["nous", "vous", ""]


def decide_imperatif(sentence):
	split_Sentence = sentence.split(' ')
	if len(split_Sentence) < 5:
		return True
	else:
		return False



def splitter(sentence):
	verbs_list = []
	for pref, suff in zip(prefixes, suffixes):
		if pref in sentence:
			sentenceOne = (sentence.split(pref)[1]).strip()
			# print(sentenceOne)
			if pref == "ils":
				sentenceTwo = sentenceOne.strip()
			else:
				sentenceTwo = (sentenceOne.split(suff)[0]).strip()
			if pref == "j'":
				verber = pref + sentenceTwo
			else:
				verber = pref + " " + sentenceTwo
			verbs_list.append(verber)
	verbs_list = list(dict.fromkeys(verbs_list))
	return verbs_list


def imperatif_splitter(IMsentence):
	IM_verbs_list = []
	for IMpref, IMsuff in zip(IMprefixes, IMsuffixes):
		if IMpref in IMsentence:
			IMsentenceOne = (IMsentence.split(IMpref)[1]).strip()
			# print(IMsentenceOne)
			if IMpref == "vous":
				IMsentenceTwo = IMsentenceOne.strip()
			else:
				IMsentenceTwo = (IMsentenceOne.split(IMsuff)[0]).strip()
			if IMpref == "tu":
				IMverber = IMpref + IMsentenceTwo
			else:
				IMverber = IMpref + " " + IMsentenceTwo
			IM_verbs_list.append(IMverber)
	IM_verbs_list = list(dict.fromkeys(IM_verbs_list))
	IM_verbs_list = [None, IM_verbs_list[0], None, IM_verbs_list[1], IM_verbs_list[2], None]
	return IM_verbs_list



def hitSoup(frenchVerb):
	URL = "https://leconjugueur.lefigaro.fr/french/verb/" + frenchVerb + ".html"
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	conjugations = soup.find_all("div", class_="conjugBloc")
	return conjugations




def verbParser(conjugations):
	verbDict = {}
	for tense in conjugations:

		try:
			tense_id = tense.div.attrs['id']
		except:
			tense_id = None

		if tense_id is not None:
			
			tense_text = tense.text.lower()

			if tense_id == "temps0":
				tense_text = tense_text.replace("present", "")
				processed_tense = splitter(tense_text)
				verbDict["present"] = processed_tense

			elif tense_id == "temps100":
				tense_text = tense_text.replace("present perfect", "")
				processed_tense = splitter(tense_text)
				verbDict["passe compose"] = processed_tense

			elif tense_id == "temps6":
				tense_text = tense_text.replace("imperfect", "")
				processed_tense = splitter(tense_text)
				verbDict["imparfait"] = processed_tense

			elif tense_id == "temps106":
				tense_text = tense_text.replace("pluperfect", "")
				processed_tense = splitter(tense_text)
				verbDict["plus-que-parfait (past perfect)"] = processed_tense

			elif tense_id == "temps18":
				tense_text = tense_text.replace("future", "")
				processed_tense = splitter(tense_text)
				verbDict["future simple"] = processed_tense

			elif tense_id == "temps36":
				processed_tense = splitter(tense_text)
				processed_tense = splitter(tense_text)
				verbDict["conditionnel présent"] = processed_tense

			elif tense_id == "temps136":
				tense_text = tense_text.replace("first_past", "")
				processed_tense = splitter(tense_text)
				verbDict["conditionnel passe"] = processed_tense

	df = pd.DataFrame(verbDict)
	return df



def verbDownloader(frenchVerb):
	conjugations = hitSoup(frenchVerb)

	try:
		df = verbParser(conjugations)
		df.to_excel(dataPath +  frenchVerb + '.xlsx', index=False)
	except:
		print('Could not finish ', frenchVerb)


if __name__ == "__main__":
	downloaded = os.listdir(dataPath)
	downloaded = [x.replace('.xlsx', '') for x in downloaded]

	frame = pd.read_excel('verbsList.xlsx')
	frame.dropna(subset=['french'], axis=0, inplace=True)
	DFverbs = list(frame['french'].unique())
	for dfVerb in DFverbs:
		if dfVerb not in downloaded:
			print(dfVerb)
			verbDownloader(dfVerb)
			time.sleep(10)