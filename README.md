# MedScope: Smart Imaging System for Ear, Throat, and Skin Diagnostics
MedScope is an AI-powered platform designed for diagnostic imaging, specifically for otoscopy, pharyngoscopy, and dermatoscopy. The system integrates various ML models to analyze images, generate diagnostic reports, and provide recommendations.

Project Structure
1. Backend (Django + DRF)
The backend of the project is built using Django and Django Rest Framework (DRF). It serves as the core of the application, handling image uploads, running ML models, generating PDF reports, and managing user data.

`core/`: Contains main project configurations (settings, URL routing).

`imaging/`: Contains all logic related to medical imaging, including image models, views for image uploads and report generation, and PDF utilities.

`models.py`: Defines the data models for different types of images (Dermatology, Pharyngoscopy, Otoscopy).

`views/`: Includes the views for image upload and report generation.

`pdf_utils.py`: Utility functions for generating PDF reports based on the images and predictions.

`urls.py`: Routes for API endpoints related to image processing and report generation.

## How to Run the Project
Follow the steps below to run the project locally.

Prerequisites
- Python 3.10+ (Ensure you have Python 3.10 or higher installed).

1. Backend Setup (Django)
Clone the repository:

```bash
git clone https://github.com/unfortunatelygeek/medscope_server
```
Create a virtual environment:

```python -m venv venv```

Activate the virtual environment:

On Windows:

```.\venv\Scripts\activate```

On macOS/Linux:

```source venv/bin/activate```

Install the dependencies:

```pip install -r requirements.txt```

Set up environment variables:

Create a .env file in the root directory and add the following:

```
ROBOFLOW_API_KEY=your_roboflow_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Run the migrations to set up the database:

```python manage.py migrate```

Start the Django development server:

```python manage.py runserver```

The backend will now be available at http://localhost:8000.

### API Endpoints

1. POST ```/api/upload/```: Upload an image
Description: Upload an image for diagnostic analysis.

Request Body: Form-data with the image file.

Response: Image metadata and processing status.

2. GET ```/api/report/```: Generate diagnostic report
Description: Generates a PDF report with predictions and recommendations.

Response: PDF file containing the report.

Remember theit's usually ```/api/upload/dermato``` and so on