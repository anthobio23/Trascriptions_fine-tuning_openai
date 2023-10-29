#!/usr/bin/python3

import re
from unidecode import unidecode
import json


def match_parrafo(msg: str):
	
	msg = msg.replace('á', 'a').\
		replace('é', 'e').\
		replace('í', 'i').\
		replace('ó', 'o').\
		replace('ú', 'u').\
		replace('ñ', 'ni').\
		replace('ü', 'u')
	msg = msg.replace('\n', ' ')
	msg = re.sub(r'[¿?"\'&@!¡]', '', msg)
	text = msg.split('Trascripcion ')
	#rc = re.compile(r"trascripcion \d:\.", flags=re.IGNORECASE)
	#text = msg.split(r"trascrip\w* \d:")
	return text


if __name__ == '__main__':
	with open('../database/Trascripciones.txt', 'r') as target:
		data = target.read()
	
	data = match_parrafo(data)
	
	with open('../database/fine_tuned_data.jsonl', 'w') as target:
		for n, i in enumerate(data):
			json_line = json.dumps(
				{
					"prompt": f"genera texto con la misma gramatica, tono de redaccion y estilo para esta transcripcion {n}",
					"completion": f"{i}"
				}
			)
			target.write(json_line + '\n')
		