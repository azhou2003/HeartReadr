# HeartReadr

HeartReadr is a web application designed to process screen captures or video files and perform number recognition, enabling automated extraction and analysis of numeric data from visual media. It is built using Python and Django, with support for modern computer vision libraries.

## Features

- Upload and process video or image files for number recognition.
- Extract frames and generate plots from input media.
- Download results as CSV files.
- Web-based interface for easy interaction.
- Media management for input videos, extracted frames, and output plots.
- Extensible architecture for adding new recognition or analysis services.

## Project Structure

- `HeartReadrSite/` – Django project settings and URLs
- `main/` – Main application logic, models, views, forms, services, and templates
- `media/` – Uploaded and generated media (csvs, frames, input_video, plots)
- `static/` – Static assets (CSS, JS, favicons)
- `requirements.txt` – Python dependencies
- `Procfile`, `runtime.txt` – Deployment configuration

## Tech Stack

- **Backend:** Python 3, Django
- **Frontend:** Django Templates, HTML/CSS/JS (static assets)
- **Computer Vision:** OpenCV, EasyOCR, and PyTorch (see requirements.txt)

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- (Optional) Virtual environment tool (venv)

### Installation

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/azhou2003/HeartReadr.git
   cd HeartReadr
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv HeartReadr-env
   .\HeartReadr-env\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

### Running the Development Server

```powershell
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser to access the application.

## Required Environment Variables

Create a `.env` file in the project root (if not present) and set the following variables as needed:

- `SECRET_KEY` – Django secret key (required for production)
- `DEBUG` – Set to `True` for development, `False` for production
- `ALLOWED_HOSTS` – Comma-separated list of allowed hosts (e.g., `localhost,127.0.0.1`)
- (Add any third-party API keys or service credentials as needed)

## Deployment

- The project is ready for deployment on platforms like Heroku (see `Procfile` and `runtime.txt`).

## Contributing

Contributions are welcome! Please open issues or submit pull requests for new features, bug fixes, or improvements. Feel free to fork the repo!

## License

None