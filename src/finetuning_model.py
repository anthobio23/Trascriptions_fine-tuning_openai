#!/usr/bin/activate

import time

from conf import openai


class FineTuningModel:
	
	def __init__(self, model: str = 'davinci'):
		self.model = model
	
	def load_data_openai(self):
		data_train = openai.File.create(
			file=open(f"database/data_prepared_{self.model}.jsonl", "rb"),
			purpose='fine-tune',
			user_provided_filename="training_file_trascription_test"
		)
		return data_train['id']
		
	def fine_tuning_model(self, id_data_fine_tuning):
		model = self.model if self.model == 'davinci' else 'gpt-3.5-turbo'
		fine_tuned = openai.FineTuningJob.create(
			training_file=id_data_fine_tuning,
			model=model,
			hyperparameters={"n_epochs": 6}
		)
		
		while True:
			if fine_tuned['status'] != 'running':
				print(openai.FineTuningJob.list(limit=1))
				time.sleep(20)
			else:
				break
		print(f"Estado de fine-tuning: {fine_tuned['status']}")
	
	def use_model_finetuned(self, id_model_finetuned: str = None, prompt: str = None) -> str:
		id_model_finetuned = openai.FineTuningJob.list(limit=1)['data'][0]['fine_tuned_model'] if id_model_finetuned is None else id_model_finetuned
		print(f"model ajusto a usar: {id_model_finetuned}") # ft:gpt-3.5-turbo-0613:personal::8GBpGZOg
		if self.model == 'gpt':
			completion = openai.ChatCompletion.create(
				model=id_model_finetuned,
				messages=[
					{
						"role": "system",
						"content": """
							Eres un asistente que ayuda a generar texto de minimo 2500
							palabras de forma creativa y relacionado con la zoologia
							"""
					},
					{
						"role": "user",
						"content": prompt
					}
				],
				max_tokens=2800
			)
			message = completion.choices[0].message
			return message['content']
		elif self.model == 'davinci':
			completion = openai.Completion.create(
				model=id_model_finetuned,
				prompt=prompt,
				max_tokens=1000
			)
			return completion.choices[0].text
			
	
