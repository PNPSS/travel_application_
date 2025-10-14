# Travel Explorer - AI-Powered Travel Planning Platform

A full-stack web application that provides personalized travel recommendations using machine learning algorithms. Plan your trips with intelligent transport mode suggestions and AI-generated itineraries.

## Features

### 🏠 Homepage
- Hero section with compelling call-to-action
- Auto-rotating carousel showcasing popular destinations
- Bento grid layout with destination highlights
- Search functionality for quick itinerary access

### 🚆 Transport Mode Selection
- Intelligent transport recommendations based on:
  - Distance and travel time preferences
  - Budget constraints
  - Comfort requirements
- Support for Train, Aeroplane, Bus, and Mixed modes
- ML-powered scoring system

### 📅 AI Itinerary Generation
- Personalized day-by-day itineraries
- Location-based activity recommendations
- Similar destination suggestions
- Cost estimates and best time to visit information

### 🤖 Machine Learning Features
- **Content-Based Filtering**: Location recommendations using TF-IDF and cosine similarity
- **Clustering**: K-means clustering for destination grouping
- **Transport Optimization**: Multi-factor scoring for transport mode selection
- **Personalized Itineraries**: Activity sequencing based on location features

## Technology Stack

### Backend
- **Python Flask**: RESTful API development
- **Scikit-learn**: Machine learning algorithms
- **Pandas & NumPy**: Data processing
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Responsive design with modern styling
- **Vanilla JavaScript**: Interactive functionality
- **Responsive Design**: Mobile-first approach

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration
- **Nginx**: Reverse proxy and static file serving
- **Gunicorn**: WSGI server for production

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.9+ (for local development)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd travel-explorer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask application**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

4. **Serve frontend files**
   ```bash
   python -m http.server 8000
   ```
   Open `http://localhost:8000` in your browser

### Production Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Frontend: `http://localhost`
   - API: `http://localhost/api/`

## API Endpoints

### Transport Search
```http
POST /api/search_transport
Content-Type: application/json

{
  "mode": "train",
  "location": "Mumbai",
  "date": "2024-12-25"
}
```

### Itinerary Generation
```http
POST /api/generate_itinerary
Content-Type: application/json

{
  "location": "Delhi",
  "duration": 3
}
```

### Get Locations
```http
GET /api/locations
```

### Health Check
```http
GET /api/health
```

## Machine Learning Models

### 1. Content-Based Recommender
- **TF-IDF Vectorization**: Converts location features into numerical vectors
- **Cosine Similarity**: Measures similarity between locations
- **Use Case**: Finding similar destinations for recommendations

### 2. Transport Mode Optimizer
- **Multi-factor Scoring**: Considers distance, budget, time, and comfort
- **Rule-based Intelligence**: Applies domain knowledge for recommendations
- **Dynamic Weighting**: Adjusts scores based on user preferences

### 3. Itinerary Generator
- **Activity Sequencing**: Intelligent ordering of daily activities
- **Location Feature Analysis**: Tailors activities to destination characteristics
- **Personalization**: Adapts recommendations based on duration and preferences

## Project Structure

```
travel-explorer/
├── app.py                 # Flask application with ML models
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Multi-service orchestration
├── nginx.conf           # Nginx reverse proxy configuration
├── index.html           # Homepage
├── modes.html           # Transport selection page
├── itinerary.html       # Itinerary display page
├── styles.css           # Application styling
├── script.js            # Frontend JavaScript
└── README.md            # This file
```

## Configuration

### Environment Variables
- `FLASK_ENV`: Set to `production` for production deployment
- `FLASK_DEBUG`: Enable/disable debug mode

### Model Configuration
ML models are initialized on application startup with predefined location data. The system can be extended by:

1. Adding more location data to `load_location_data()`
2. Modifying feature weights in recommendation algorithms
3. Implementing additional ML models for enhanced personalization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Enhancements

- [ ] User authentication and profiles
- [ ] Real-time flight/train data integration
- [ ] Social features and trip sharing
- [ ] Advanced ML models (Neural Networks, Collaborative Filtering)
- [ ] Mobile application development
- [ ] Multi-language support
- [ ] Integration with external APIs (booking systems, weather, etc.)