import pyscreenshot as ImageGrab
import tesserocr
import google
import webbrowser
import urllib
from nltk.corpus import stopwords

line_3_config = [
		(750, 110, 1500, 350),
		(820, 360, 1400, 500),
		(820, 500, 1400, 700),
		(820, 700, 1400, 900),
	]
line_2_config = [
		(750, 120, 1500, 330),
		(820, 330, 1400, 500),
		(820, 480, 1400, 650),
		(820, 630, 1400, 850),
	]
typ_vec = ['q','o','o','o']

isNot = False

esw = set(stopwords.words('english'))

def get_opt(o):
	o_split = o.split('\n')
	mlen = max([len(x) for x in o_split])
	for i in range(len(o_split)):
		if len(o_split[i])==mlen:
			return o_split[i].lower()

def get_query(q):
	global isNot
	q_split = [ s.strip() for s in q.split('\n') if len(s.strip())>2]
	q = ' '.join(q_split).lower()
	if q.count('not')!=0:
		isNot = True
	q = q.replace('not ','')
	return q

def clean_opts(o1,o2,o3):
	o1 = o1.replace('.',' ')
	o2 = o2.replace('.',' ')
	o3 = o3.replace('.',' ')

	o1_s = o1.split()
	o2_s = o2.split()
	o3_s = o3.split()

	common_words = set(o1_s)&set(o2_s)&set(o3_s)

	return 	' '.join([w for w in o1_s if (w not in common_words and len(w)>1)]),\
			' '.join([w for w in o2_s if (w not in common_words and len(w)>1)]),\
			' '.join([w for w in o3_s if (w not in common_words and len(w)>1)]),\

def get_word_wise(desc,oc1,oc2,oc3):
	oc1_s = oc1.split()
	oc2_s = oc2.split()
	oc3_s = oc3.split()

	oc1_c = sum([ desc.count(w) for w in oc1_s if w not in esw])
	oc2_c = sum([ desc.count(w) for w in oc2_s if w not in esw])
	oc3_c = sum([ desc.count(w) for w in oc3_s if w not in esw])

	return (oc1_c,oc2_c,oc3_c)

def get_text(loc,typ):
	im = ImageGrab.grab(bbox=loc)
	im.show()
	txt = tesserocr.image_to_text(im)
	# print(txt)
	# print("="*20)
	if typ=='o':
		txt = get_opt(txt)
	else:
		txt = get_query(txt)
	return txt

def search_and_print(query,o1,o2,o3,num_pages):
	search_results = google.search(query, num_pages)

	desc = ' '.join([res.description.lower() for res in search_results])
	desc += (' '+' '.join([res.name.lower() for res in search_results]))
	# print(search_results[0].name)

	oc1,oc2,oc3 = clean_opts(o1,o2,o3)
	print(query)
	print(oc1,oc2,oc3,sep="|")

	print(desc.count(oc1),desc.count(oc2),desc.count(oc3))
	oc1_c,oc2_c,oc3_c = desc.count(o1),desc.count(o2),desc.count(o3)
	print(oc1_c,oc2_c,oc3_c)
	print(*get_word_wise(desc,oc1,oc2,oc3))

	if isNot:
		print("NOT ### NOT ### NOT")

	if num_pages==1 and sum([oc1_c,oc2_c,oc3_c])==0:
		search_and_print(query,o1,o2,o3,2)


def doit(num_lines):
	global isNot
	isNot = False

	if num_lines=='2':
		query,o1,o2,o3 = map(get_text,line_2_config,typ_vec)
	else:
		query,o1,o2,o3 = map(get_text,line_3_config,typ_vec)

	# query = "to whom is the president of not india supposed to submit his resignation letter?"
	# o1 = "chief justice"
	# o2 = "vice-president"
	# o3 = "prime minister"

	webbrowser.get().open("https://www.google.co.in/search?"+urllib.parse.urlencode({'q':query}), autoraise=False)

	search_and_print(query,o1,o2,o3,1)

	if ('-' in o1) or ('-' in o2) or ('-' in o3):
		o1 = o1.replace('-',' ')
		o2 = o2.replace('-',' ')
		o3 = o3.replace('-',' ')

		search_and_print(query,o1,o2,o3,1)

while True:
	doit(input("..."))

# doit('2')

	
