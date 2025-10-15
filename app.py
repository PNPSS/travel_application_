from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pickle
import os
import json
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)

# Load or create ML models
class TravelRecommendationSystem:
    def __init__(self):
        self.location_data = self.load_location_data()
        self.transport_data = self.load_transport_data()
        self.itinerary_model = None
        self.transport_model = None
        self.initialize_models()

    def load_location_data(self):
        """Load location data with features for recommendations"""
        locations = [
            {
                'name': 'Hyderabad',
                'type': 'city',
                'features': ['historical', 'food', 'technology', 'culture', 'shopping'],
                'attractions': ['Charminar', 'Golconda Fort', 'Hussain Sagar', 'Salam Jung Museum'],
                'best_time': 'October-March',
                'avg_cost_per_day': 2000,
                'rating': 4.2
            },
            {
                'name': 'Delhi',
                'type': 'city',
                'features': ['historical', 'political', 'culture', 'food', 'shopping'],
                'attractions': ['Red Fort', 'India Gate', 'Qutub Minar', 'Lotus Temple'],
                'best_time': 'October-March',
                'avg_cost_per_day': 2500,
                'rating': 4.1
            },
            {
                'name': 'Mumbai',
                'type': 'city',
                'features': ['beach', 'bollywood', 'business', 'food', 'nightlife'],
                'attractions': ['Gateway of India', 'Marine Drive', 'Elephanta Caves', 'Chhatrapati Shivaji Terminus'],
                'best_time': 'November-May',
                'avg_cost_per_day': 3000,
                'rating': 4.3
            },
            {
                'name': 'Bangalore',
                'type': 'city',
                'features': ['technology', 'gardens', 'food', 'shopping', 'startup'],
                'attractions': ['Bangalore Palace', 'Cubbon Park', 'Lalbagh Botanical Garden', 'Vidhana Soudha'],
                'best_time': 'October-March',
                'avg_cost_per_day': 2200,
                'rating': 4.0
            },
            {
                'name': 'Chennai',
                'type': 'city',
                'features': ['beach', 'culture', 'food', 'temples', 'classical_music'],
                'attractions': ['Marina Beach', 'Kapaleeshwarar Temple', 'Fort St. George', 'San Thome Basilica'],
                'best_time': 'December-February',
                'avg_cost_per_day': 1800,
                'rating': 3.9
            },
            {
                'name': 'Kolkata',
                'type': 'city',
                'features': ['historical', 'culture', 'food', 'literature', 'festivals'],
                'attractions': ['Victoria Memorial', 'Howrah Bridge', 'St. Paul\'s Cathedral', 'Marble Palace'],
                'best_time': 'October-March',
                'avg_cost_per_day': 1500,
                'rating': 4.0
            },
            {
                'name': 'Pune',
                'type': 'city',
                'features': ['education', 'historical', 'food', 'hill_stations', 'shopping'],
                'attractions': ['Shaniwar Wada', 'Aga Khan Palace', 'Parvati Hill', 'Sinhagad Fort'],
                'best_time': 'October-May',
                'avg_cost_per_day': 1900,
                'rating': 3.8
            }
        ]
        return locations

    def load_transport_data(self):
        """Load transport options data"""
        return {
            'train': {
                'name': 'Train',
                'description': 'Comfortable and scenic journeys across India',
                'avg_speed': 60,  # km/h
                'comfort_rating': 4.0,
                'cost_rating': 3.5,
                'reliability_rating': 4.2,
                'environmental_rating': 4.5
            },
            'aeroplane': {
                'name': 'Aeroplane',
                'description': 'Fast and efficient air travel',
                'avg_speed': 800,  # km/h
                'comfort_rating': 4.5,
                'cost_rating': 2.0,
                'reliability_rating': 4.8,
                'environmental_rating': 2.0
            },
            'bus': {
                'name': 'Bus',
                'description': 'Affordable and flexible road travel',
                'avg_speed': 50,  # km/h
                'comfort_rating': 3.0,
                'cost_rating': 4.5,
                'reliability_rating': 3.5,
                'environmental_rating': 3.5
            },
            'mixed': {
                'name': 'Mixed',
                'description': 'Combine different modes for optimal travel',
                'avg_speed': 0,  # variable
                'comfort_rating': 4.0,
                'cost_rating': 3.0,
                'reliability_rating': 4.0,
                'environmental_rating': 3.5
            }
        }

    def initialize_models(self):
        """Initialize ML models for recommendations"""
        # Create feature vectors for locations
        location_features = []
        for loc in self.location_data:
            features = ' '.join(loc['features'] + [loc['type']])
            location_features.append(features)

        # TF-IDF vectorization for content-based filtering
        self.tfidf_vectorizer = TfidfVectorizer(max_features=100)
        self.location_vectors = self.tfidf_vectorizer.fit_transform(location_features)

        # K-means clustering for location grouping
        self.kmeans = KMeans(n_clusters=3, random_state=42)
        self.location_clusters = self.kmeans.fit_predict(self.location_vectors.toarray())

    def recommend_transport_mode(self, mode_preference, distance, budget, time_constraint):
        """Recommend transport mode based on user preferences"""
        recommendations = []

        for mode_key, mode_data in self.transport_data.items():
            score = 0

            # Mode preference matching
            if mode_preference.lower() == mode_key:
                score += 50

            # Distance suitability
            if distance < 300:  # Short distance
                if mode_key in ['bus', 'train']:
                    score += 30
                elif mode_key == 'aeroplane':
                    score -= 20
            elif distance < 1000:  # Medium distance
                if mode_key in ['train', 'bus', 'aeroplane']:
                    score += 25
            else:  # Long distance
                if mode_key == 'aeroplane':
                    score += 40
                elif mode_key == 'train':
                    score += 20

            # Budget consideration
            if budget == 'low':
                if mode_data['cost_rating'] >= 4.0:
                    score += 30
            elif budget == 'medium':
                if 3.0 <= mode_data['cost_rating'] <= 4.0:
                    score += 25
            else:  # high budget
                score += mode_data['cost_rating'] * 5

            # Time constraint
            if time_constraint == 'fast':
                score += mode_data['avg_speed'] * 0.1
            elif time_constraint == 'comfortable':
                score += mode_data['comfort_rating'] * 10

            recommendations.append({
                'mode': mode_key,
                'name': mode_data['name'],
                'description': mode_data['description'],
                'score': score,
                'estimated_time': f"{distance // mode_data['avg_speed']}h" if mode_data['avg_speed'] > 0 else "Variable",
                'comfort_rating': mode_data['comfort_rating'],
                'cost_rating': mode_data['cost_rating']
            })

        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:3]

    def generate_itinerary(self, location, duration_days):
        """Generate personalized itinerary using ML-based recommendations"""
        # Find the location data
        location_data = None
        for loc in self.location_data:
            if loc['name'].lower() == location.lower():
                location_data = loc
                break

        if not location_data:
            return {"error": "Location not found"}

        # Generate day-wise itinerary
        itinerary = {
            'location': location_data['name'],
            'duration': duration_days,
            'total_estimated_cost': location_data['avg_cost_per_day'] * duration_days,
            'best_time_to_visit': location_data['best_time'],
            'rating': location_data['rating'],
            'days': []
        }

        # Distribute attractions across days
        attractions = location_data['attractions'].copy()
        random.shuffle(attractions)

        # ML-based activity clustering (simplified)
        morning_activities = ['Visit historical sites', 'Explore markets', 'Cultural experiences']
        afternoon_activities = ['Lunch at local restaurants', 'Shopping', 'Relax at parks']
        evening_activities = ['Sunset views', 'Dinner experiences', 'Nightlife']

        for day in range(1, duration_days + 1):
            day_itinerary = {
                'day': day,
                'activities': []
            }

            # Morning activity
            if attractions:
                attraction = attractions.pop()
                day_itinerary['activities'].append(f"Visit {attraction}")
            else:
                day_itinerary['activities'].append(random.choice(morning_activities))

            # Afternoon activity
            day_itinerary['activities'].append(random.choice(afternoon_activities))

            # Evening activity
            day_itinerary['activities'].append(random.choice(evening_activities))

            itinerary['days'].append(day_itinerary)

        return itinerary

    def get_similar_locations(self, location_name, top_n=3):
        """Find similar locations using content-based filtering"""
        # Find the target location
        target_idx = None
        for i, loc in enumerate(self.location_data):
            if loc['name'].lower() == location_name.lower():
                target_idx = i
                break

        if target_idx is None:
            return []

        # Calculate similarities
        target_vector = self.location_vectors[target_idx]
        similarities = cosine_similarity(target_vector, self.location_vectors)[0]

        # Get top similar locations (excluding itself)
        similar_indices = np.argsort(similarities)[::-1][1:top_n+1]

        similar_locations = []
        for idx in similar_indices:
            similar_locations.append({
                'name': self.location_data[idx]['name'],
                'similarity_score': float(similarities[idx]),
                'features': self.location_data[idx]['features'][:3],  # Top 3 features
                'rating': self.location_data[idx]['rating']
            })

        return similar_locations
    
@app.route('/')
def home():
    return "Hello! Your Flask app is working 🚀"

if __name__ == '__main__':
    app.run()

# Initialize the recommendation system
recommendation_system = TravelRecommendationSystem()

@app.route('/api/search_transport', methods=['POST'])
def search_transport():
    """API endpoint for transport mode search"""
    try:
        data = request.get_json()

        mode = data.get('mode', 'mixed')
        location = data.get('location', '')
        date = data.get('date', '')

        # Estimate distance (simplified - in real app, use actual distance calculation)
        distance = random.randint(200, 1500)  # Random distance for demo

        # Determine budget and time constraints based on mode preference
        budget = 'medium'
        time_constraint = 'balanced'

        if mode == 'bus':
            budget = 'low'
        elif mode == 'aeroplane':
            time_constraint = 'fast'
        elif mode == 'train':
            time_constraint = 'comfortable'

        recommendations = recommendation_system.recommend_transport_mode(
            mode, distance, budget, time_constraint
        )

        # Add mock pricing and availability
        for rec in recommendations:
            rec['estimated_cost'] = random.randint(500, 5000)
            rec['availability'] = random.choice(['Available', 'Limited', 'High Demand'])

        return jsonify({
            'success': True,
            'location': location,
            'date': date,
            'distance_km': distance,
            'recommendations': recommendations
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate_itinerary', methods=['POST'])
def generate_itinerary():
    """API endpoint for itinerary generation"""
    try:
        data = request.get_json()

        location = data.get('location', '')
        duration = int(data.get('duration', 3))

        if not location:
            return jsonify({
                'success': False,
                'error': 'Location is required'
            }), 400

        if duration < 1 or duration > 30:
            return jsonify({
                'success': False,
                'error': 'Duration must be between 1 and 30 days'
            }), 400

        itinerary = recommendation_system.generate_itinerary(location, duration)

        # Add similar locations recommendation
        similar_locations = recommendation_system.get_similar_locations(location)

        return jsonify({
            'success': True,
            'itinerary': itinerary,
            'similar_locations': similar_locations
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Get all available locations"""
    locations = []
    for loc in recommendation_system.location_data:
        locations.append({
            'name': loc['name'],
            'type': loc['type'],
            'features': loc['features'],
            'rating': loc['rating'],
            'best_time': loc['best_time']
        })

    return jsonify({
        'success': True,
        'locations': locations
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)