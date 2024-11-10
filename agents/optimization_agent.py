class OptimizationAgent:
    def optimize_route(self, itinerary, budget):
        optimized_itinerary = []

        for stop in itinerary:
            entry_fee = stop.get("entry_fee", "0").replace("$", "")
            try:
                entry_fee_value = int(entry_fee)  # Convert to integer if possible
            except ValueError:
                # Handle cases where entry_fee is not a number
                entry_fee_value = 0  # Default to 0 or some other handling

            # Example budget-based logic
            if entry_fee_value > budget / len(itinerary):
                stop["transportation"] = "Walk"  # Adjust transportation to reduce cost
            
            optimized_itinerary.append(stop)
        
        return optimized_itinerary
