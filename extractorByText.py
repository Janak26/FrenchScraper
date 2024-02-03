import requests
from bs4 import BeautifulSoup
import pandas as pd


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
			print('sentence1 ', sentenceOne)
			if pref == "ils":
				sentenceTwo = sentenceOne.strip()
			else:
				sentenceTwo = (sentenceOne.split(suff)[0]).strip()
			if pref == "j'":
				verber = pref + sentenceTwo
			else:
				verber = pref + " " + sentenceTwo
			print('sentence2 ', sentenceTwo)
			print(verber)
			print('---')
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
	URL = "https://leconjugueur.lefigaro.fr/french/verb/aller.html"
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	conjugations = soup.find_all("div", class_="conjugBloc")
	return conjugations



def verbParser(frenchVerb):

	verbDict = {}

	present_count = 0

	plusperfect_count = 0

	imperfect_count = 0

	conjugations = hitSoup(frenchVerb)

	for tense in conjugations:

		tense_text = tense.text.lower()

		if tense_text.startswith("presentj"):
			tense_text = tense_text.replace("present", "")
			if present_count == 0:
				processed_tense = splitter(tense_text)
				verbDict["present"] = processed_tense
				present_count = present_count + 1

			elif present_count == 1:
				processed_tense = splitter(tense_text)
				verbDict["conditionnel present"] = processed_tense
				present_count = present_count + 1


		elif tense_text.startswith("present perfect"):
			tense_text = tense_text.replace("present perfect", "")
			processed_tense = splitter(tense_text)
			verbDict["passe compose"] = processed_tense
			
		elif tense_text.startswith("imperfect"):
			tense_text = tense_text.replace("imperfect", "")
			if imperfect_count == 0:
				processed_tense = splitter(tense_text)
				verbDict["imparfait"] = processed_tense
			imperfect_count = imperfect_count + 1


		elif tense_text.startswith("pluperfect"):
			tense_text = tense_text.replace("pluperfect", "")
			if plusperfect_count == 0:
				processed_tense = splitter(tense_text)
				verbDict["plus-que-parfait (past perfect)"] = processed_tense
			plusperfect_count = plusperfect_count + 1

		elif tense_text.startswith("future"):
			tense_text = tense_text.replace("future", "")
			processed_tense = splitter(tense_text)
			verbDict["futur simple"] = processed_tense

		elif tense_text.startswith("first past"):
			tense_text = tense_text.replace("first_past", "")
			processed_tense = splitter(tense_text)
			verbDict["conditionnel passe"] = processed_tense


	df = pd.DataFrame(verbDict)
	# print(df)
	df.to_excel(dataPath +  frenchVerb + '.xlsx', index=False)




if __name__ == "__main__":
	verbParser('aller')
	# sent = "futurej'iraitu irasil iranous ironsvous irezils iront"
	# print(sent)
	# splitter(sent)