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
	# text = msg.split('Trascripcion ')
	
	return msg


def text_to_json(text: str):
	
	text = match_parrafo(text)
	
	with open('../database/fine_tuned_data.jsonl', 'w') as file:
		for n, i in enumerate(text):
			# data para modelo davinci
			json_line = json.dumps(
				{
					"prompt": f"genera texto con la misma gramatica, tono de redaccion y estilo para esta transcripcion {n}",
					"completion": f"{i}"
				}
			)
			file.write(json_line + '\n')


if __name__ == '__main__':
	# data de texto en crudo
	with open('../database/Trascripciones.txt', 'r') as target:
		data = target.read()
	text_to_json(text=data)
	