#!/usr/bin/python3

import json
import tiktoken
import numpy as np
from collections import defaultdict


class EDATextTranscriptions:
	
	data_path = "../database/data_prepared_davinci.jsonl"
	encoding = tiktoken.get_encoding("cl100k_base")
	
	# Load the dataset
	with open(data_path, 'r', encoding='utf-8') as f:
		dataset = [json.loads(line) for line in f]
	
	def load_data(self):
		# Initial dataset stats
		print("Num examples:", len(self.dataset))
		print("First example:")
		for message in self.dataset[0].items():
			print(message)
			
	def error_validate(self):
		
		# Format error checks
		format_errors = defaultdict(int)
		
		for ex in self.dataset:
			if not isinstance(ex, dict):
				format_errors["data_type"] += 1
				continue
			
			for k, v in ex.items():
				if "prompt" == k or "completion" == k:
					continue
				else:
					format_errors["message_missing_key"] += 1
				
				content = ex.get("prompt", None)
				function_call = ex.get("completion", None)
				
				if (not content and not function_call) or not isinstance(content, str):
					format_errors["missing_content"] += 1
		
		if format_errors:
			print("Found errors:")
			for k, v in format_errors.items():
				print(f"{k}: {v}")
		else:
			print("No errors found")
	
	# not exact!
	# simplified from https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
	def num_tokens_from_messages(self, messages, tokens_per_message=3, tokens_per_name=1):
		num_tokens = 0
		for message in messages:
			num_tokens += tokens_per_message
			for key, value in message.items():
				num_tokens += len(self.encoding.encode(value))
				if key == "name":
					num_tokens += tokens_per_name
		num_tokens += 3
		return num_tokens
	
	def num_assistant_tokens_from_messages(self, messages):
		num_tokens = 0
		for message in messages:
			if message["role"] == "assistant":
				num_tokens += len(self.encoding.encode(message["content"]))
		return num_tokens
	
	@staticmethod
	def print_distribution(self, values, name):
		print(f"\n#### Distribution of {name}:")
		print(f"min / max: {min(values)}, {max(values)}")
		print(f"mean / median: {np.mean(values)}, {np.median(values)}")
		print(f"p5 / p95: {np.quantile(values, 0.1)}, {np.quantile(values, 0.9)}")


if __name__ == "__main__":
	tex = EDATextTranscriptions()
	tex.load_data()
	tex.error_validate()
	