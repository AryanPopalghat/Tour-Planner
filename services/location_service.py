class LocationService:
    def get_recommendations(self, city, interests):
        # Mock response for demonstration; ideally, this would fetch from an external API or database
        recommendations = {
            "Rome": [
                {"name": "Colosseum", "suggested_time": "9:00 AM - 10:30 AM", "entry_fee": "$15"},
                {"name": "Roman Forum", "suggested_time": "10:45 AM - 12:00 PM", "entry_fee": "$12"},
                {"name": "Pantheon", "suggested_time": "12:30 PM - 1:15 PM", "entry_fee": "Free"},
                {"name": "Piazza Navona", "suggested_time": "2:30 PM - 3:30 PM", "entry_fee": "Free"},
                {"name": "Trevi Fountain", "suggested_time": "4:00 PM - 4:45 PM", "entry_fee": "Free"},
            ],
            "Paris": [
                {"name": "Eiffel Tower", "suggested_time": "9:00 AM - 10:30 AM", "entry_fee": "$25"},
                {"name": "Louvre Museum", "suggested_time": "11:00 AM - 1:00 PM", "entry_fee": "$15"},
                {"name": "Notre-Dame Cathedral", "suggested_time": "1:30 PM - 2:15 PM", "entry_fee": "Free"},
                {"name": "Montmartre", "suggested_time": "2:30 PM - 4:00 PM", "entry_fee": "Free"},
                {"name": "Champs-Élysées", "suggested_time": "4:30 PM - 6:00 PM", "entry_fee": "Free"},
            ]
        }

        # Filter recommendations based on city and interests
        if city in recommendations:
            return [place for place in recommendations[city] if any(interest in place["name"] for interest in interests)]
        return []
