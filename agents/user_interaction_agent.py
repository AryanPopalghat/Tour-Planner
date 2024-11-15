from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class UserInteractionAgent:
    def __init__(self, model_name="facebook/blenderbot-400M-distill", device="cpu"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        self.device = device

    def suggest_places(self, city, interests):
        prompt = (
            f"Suggest popular locations in {city} based on interests: {', '.join(interests)}. "
            "List each place with a name and any relevant details."
        )
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(inputs.input_ids, max_length=300)
        response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        places = []
        for line in response_text.split('\n'):
            if line.strip():
                places.append(line.strip())
        
        return places
