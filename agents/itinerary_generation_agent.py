from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class ItineraryGenerationAgent:
    def __init__(self, model_name="sshleifer/distilbart-cnn-6-6", device="cpu"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        self.device = device

    def generate_itinerary(self, city, interests, start_time, end_time, budget, suggested_places):
        place_list = "; ".join(suggested_places)
        prompt = (
            f"Create a detailed itinerary for a day trip in {city} from {start_time} to {end_time} with a budget of ${budget}. "
            f"Include the following stops based on the interests in {', '.join(interests)}: {place_list}. "
            "For each stop, provide the following details: Name, Time, Entry Fee, Transportation, and Status."
        )
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(inputs.input_ids, max_length=500)
        itinerary_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        itinerary = []
        for line in itinerary_text.split('\n'):
            if "Stop" in line or "Name" in line:
                stop = {
                    "name": line.split(":", 1)[1].strip() if ":" in line else "Unknown Place",
                    "time": "TBD",
                    "entry_fee": "$0",
                    "transportation": "Walk",
                    "status": "Open"
                }
                itinerary.append(stop)
            elif "Time" in line:
                itinerary[-1]["time"] = line.split(":", 1)[1].strip()
            elif "Entry Fee" in line:
                itinerary[-1]["entry_fee"] = line.split(":", 1)[1].strip()
            elif "Transportation" in line:
                itinerary[-1]["transportation"] = line.split(":", 1)[1].strip()
            elif "Status" in line:
                itinerary[-1]["status"] = line.split(":", 1)[1].strip()

        return itinerary
