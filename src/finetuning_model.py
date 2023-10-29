#!/usr/bin/activate

import openai
# from dotenv import load_dotenv


class FineTuningModel:
	
	def __init__(self, model: str = 'davinci'):
		# load_dotenv()
		self.OPENAI_KEY = "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"
		self.model = model
	
	def load_data_openai(self):
		openai.api_key = self.OPENAI_KEY
		data_train = openai.File.create(
			file=open(f"database/data_prepared_{self.model}.jsonl", "rb"),
			purpose='fine-tune',
			user_provided_filename="training_file_trascription_test"
		)
		return data_train['id']
		
	def fine_tuning_model(self, id_data_fine_tuning):
		openai.api_key = self.OPENAI_KEY
		model = self.model if self.model == 'davinci' else 'gpt-3.5-turbo'
		fine_tuned = openai.FineTuningJob.create(
			training_file=id_data_fine_tuning,
			model=model,
			hyperparameters={"n_epochs": 6}
		)
		print(fine_tuned)
	
	def use_model_finetuned(self, id_model_finetuned: str = None, prompt: str = None) -> str:
		openai.api_key = self.OPENAI_KEY
		id_model_finetuned = openai.FineTuningJob.list(limit=1)['data'][0]['fine_tuned_model'] if id_model_finetuned is None else id_model_finetuned
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
			
	