#!/usr/bin/activate
import os.path
import random
from src.finetuning_model import FineTuningModel


class ProcessModelText(object):
	
	def __init__(self, model: str = 'davinci'):
		self.model = model
		self.tuning_model = FineTuningModel(model=model)
		
		with open('templates/prompt_template.txt', 'r') as target:
			template = target.read()
			self.template = template.replace('\n', '')
			
		self.get_prompt()
		
	def use_model(self, prompt: str, id_model_finetuned: str = None):
		response = self.tuning_model.use_model_finetuned(
				id_model_finetuned=id_model_finetuned,
				prompt=prompt
			)
		return response
	
	def load_data_to_openai(self):
		try:
			id_data_fine_tuning = self.tuning_model.load_data_openai()
			self.tuning_model.fine_tuning_model(id_data_fine_tuning)
		except Exception as e:
			raise e
		else:
			print("data carga y modelo ajustado...")
	
	@staticmethod
	def output_parser(msg: str):
		output_index_path = "outputs/text_generator"
		if not os.path.exists(output_index_path):
			os.makedirs(output_index_path, exist_ok=True)
		with open(f'{output_index_path}/text_generator_{random.randint(0, 10)}.txt', 'w') as target:
			target.write(msg)
	
	def get_prompt(self):
		print("Escribe 'exit' para salir del programa")
		train = str(input('Deseas entrenar un modelo? Y/n: '))
		if train in ['Y', 'y']:
			id_fine_tuning = self.load_data_to_openai()
		print("Bienvenido al asistente generador de guion, en que puedo ayudarte: ")
		train = input("quieres leer un archivo para usarlo commo prompt? Y/n: ")
		if train in ["Y", "y"]:
			answer = self.use_model(self.template)
			print("\n-----------------------------------\n")
			print(answer)
			print("\n-----------------------------------\n")
			print(f"Cantidad de palabras: {len(answer.split())}\n")
		while True:
			prompt = input('?> ')
			if prompt.lower() == 'exit':
				print('Gracias por usar al asistente, espero haberte ayudado. \nExiting...')
				break
			try:
				try:
					assert 'id_fine_tuning' in locals()
				except AssertionError:
					id_fine_tuning = None
				answer = self.use_model(prompt, id_model_finetuned=id_fine_tuning)
				print("\n-----------------------------------\n")
				print(answer)
				print("\n-----------------------------------\n")
				print(f"Cantidad de palabras: {len(answer.split())}\n")
				res_ex = input('Deseas tener un archivo exportable del texto generado? Y/n: ')
				if res_ex is None or res_ex in ['y', 'Y']:
					self.output_parser(answer)
				elif res_ex == 'n':
					continue
			except Exception as e:
				raise e
			print("Alguna otra pregunta? ")
				

if __name__ == '__main__':
	ProcessModelText(model='gpt')
	