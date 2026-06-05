# Muna Kalati

**Empowering African Children Through Afrocentric Education**

Muna Kalati is a Django-based web application offering Afrocentric storybooks, audiobooks, and animated videos in 39 African languages. The platform aims to empower children to be confident thinkers through culturally relevant educational content.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Key Models](#key-models)
- [Views & URL Routing](#views--url-routing)
- [Admin Interface](#admin-interface)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Muna Kalati is a comprehensive content management and distribution platform designed to:
- Share Afrocentric educational content
- Manage news, press releases, and media
- Post job opportunities
- Engage with audiences through social media integration
- Provide team and review information

---

## Features

### Core Functionality
- **Latest Updates & Blog System**: Create, manage, and display blog articles with categories, summaries, and reading duration estimates
- **Featured News**: Highlight important news articles with automatic recommendation engine
- **Press Releases**: Publish and manage press releases
- **Job Listings**: Post and manage open positions with detailed job descriptions
- **Team Management**: Display team members with social media profiles
- **Social Media Integration**: Embed content from multiple platforms (X, Instagram, Facebook, YouTube, LinkedIn, TikTok)
- **Contact Management**: Capture visitor messages through contact forms
- **Search Functionality**: Advanced search for updates and job postings
- **Intelligent Recommendations**: Uses TF-IDF vectorization and cosine similarity to recommend related content
- **Multi-language Support**: i18n support for internationalization

### Admin Features
- **Jazzmin Admin Dashboard**: Enhanced Django admin interface with custom branding
- **Role-Based Access Control**: Manage permissions for different user types
- **Media Management**: Upload and manage images and media files

---

## Tech Stack

### Backend
- **Django 5.1**: Web framework
- **Python 3.x**: Programming language
- **SQLite3**: Database (development)
- **scikit-learn 1.5.2**: ML algorithms for content recommendations
- **Pillow 10.4.0**: Image processing

### Frontend
- **Django Templates**: Server-side templating
- **HTML/CSS/JavaScript**: Frontend markup and styling

### Additional Libraries
- **django-jazzmin 3.0.0**: Enhanced admin interface
- **requests**: HTTP client library
- **pytz**: Timezone support
- **django-cors** (commented out): For CORS handling if needed

---

## Project Structure

```
muna_kalati/
├── config/                          # Django project configuration
│   ├── settings.py                 # Project settings and configuration
│   ├── urls.py                     # URL routing configuration
│   ├── wsgi.py                     # WSGI application entry point
│   └── asgi.py                     # ASGI application entry point
│
├── muna_kalati/                    # Main Django app
│   ├── models.py                   # Database models
│   ├── views.py                    # View logic and handlers
│   ├── urls.py                     # App-level URL routing
│   ├── forms.py                    # Form definitions
│   ├── admin.py                    # Django admin configuration
│   ├── apps.py                     # App configuration
│   ├── migrations/                 # Database migrations
│   └── templates/                  # HTML templates
│
├── templates/                      # Project-level templates
│   ├── index.html                 # Homepage
│   ├── about_us.html              # About page
│   ├── features.html              # Features page
│   ├── media_and_news.html        # News and media hub
│   ├── latest_update_detail.html  # Blog post detail
│   ├── featured_news_detail.html  # Featured news detail
│   ├── vacancies.html             # Job listings
│   ├── open_position_detail.html  # Job detail
│   ├── press_release_detail.html  # Press release detail
│   ├── search_results.html        # Search results
│   ├── privacy_policy.html        # Privacy policy
│   ├── terms_of_use.html          # Terms of use
│   └── socialmedia_post_list.html # Social media posts
│
├── static/                         # Static files (CSS, JS, images)
├── media/                          # User-uploaded media files
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Murgany/muna_kalati.git
cd muna_kalati
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 5: Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Collect Static Files (Production)
```bash
python manage.py collectstatic
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

Access the application at: `http://127.0.0.1:8000`
Admin dashboard: `http://127.0.0.1:8000/admin`

---

## Configuration

### Django Settings (`config/settings.py`)

Key configurations:
- **TIME_ZONE**: Set to 'Africa/Abidjan'
- **LANGUAGE_CODE**: 'en-us' (with i18n support)
- **INSTALLED_APPS**: Includes jazzmin for enhanced admin
- **MIDDLEWARE**: Security and session handling middleware
- **DATABASES**: SQLite3 for development, update for production
- **STATIC_FILES**: Served from `static/` directory
- **MEDIA_FILES**: User uploads stored in `media/` directory

### Environment Variables
```
SECRET_KEY          # Django secret key (required)
DEBUG               # Debug mode (False in production)
ALLOWED_HOSTS       # Comma-separated list of allowed domains
```

### Jazzmin Admin Customization
The admin interface is customized with:
- Site logo and branding
- Custom top menu with links
- Enhanced sidebar navigation
- Dark mode support
- Custom styling options

---

## Usage

### Managing Content

#### Create a Blog Post
1. Go to Admin Dashboard → muna_kalati → Latest Updates
2. Click "Add Latest Update"
3. Fill in title, content, category, and upload image
4. Optionally add bullet points and summary
5. Save

#### Post a Job Opening
1. Go to Admin Dashboard → muna_kalati → Open Positions
2. Click "Add Open Position"
3. Enter job details, location, and job type
4. Save

#### Create a Press Release
1. Go to Admin Dashboard → muna_kalati → Press Releases
2. Add title and content
3. Save

#### Embed Social Media Content
1. Go to Admin Dashboard → muna_kalati → Social Media Posts
2. Select platform and paste embed code
3. Save

### Frontend Features

#### Search Functionality
- **Blog Search** (`/search/updates/`): Search by title, content, bullet points, or category
- **Job Search** (`/search/jobs/`): Search by job title, description, type, or location

#### Recommendation Engine
- Automatically recommends similar blog posts using TF-IDF vectorization
- Recommends related featured news based on content similarity
- Helps users discover relevant content

---

## Key Models

### Category
```python
category_name: CharField (max 50 chars)
created: DateTimeField
```

### LatestUpdate (Blog Posts)
```python
category: ForeignKey(Category)
title: CharField
image: ImageField
content: TextField
bullet_points: TextField
reading_duration: CharField
summary: TextField
author: ForeignKey(User)
created: DateTimeField
```

### OpenPosition (Job Listings)
```python
job_title: CharField
brief_description: CharField
details: TextField
location: CharField
job_type: CharField
posted_on: DateTimeField
```

### Team Member
```python
name: CharField
title: CharField
bio: TextField
image: ImageField
linkedin_url: URLField
facebook_url: URLField
instagram_url: URLField
x_url: URLField
```

### Review
```python
name: CharField
role: CharField
review_text: TextField
rating: DecimalField (0.5 to 5.0 stars)
```

### SocialMediaPost
Supports: X, Instagram, Facebook, YouTube, LinkedIn, TikTok

### Contact
Stores visitor contact form submissions:
```python
name: CharField
email: EmailField
message: TextField
date: DateTimeField
```

---

## Views & URL Routing

### Main Routes
| Route | View | Description |
|-------|------|-------------|
| `/` | `index` | Homepage |
| `/about/` | `about_us` | About page with team and reviews |
| `/features/` | `features` | Features page |
| `/media-and-news/` | `media_and_news` | News hub |
| `/updates/` | `LatestUpdateListView` | Blog listing |
| `/updates/<id>/` | `latest_update_detail` | Blog detail |
| `/news/<id>/` | `featured_news_detail` | Featured news detail |
| `/jobs/` | `open_position_list` | Job listings |
| `/jobs/<id>/` | `open_position_detail` | Job detail |
| `/press-release/<id>/` | `press_release_detail` | Press release detail |
| `/social-media/` | `SocialMediaPostListView` | Social media posts |
| `/search/updates/` | `updates_search` | Search blog posts |
| `/search/jobs/` | `jobs_search` | Search jobs |
| `/contact/` | `contact_view` | Contact form handler |
| `/privacy/` | `privacy_policy` | Privacy policy |
| `/terms/` | `terms_of_use` | Terms of use |
| `/robots.txt` | `robots_txt` | SEO robots file |
| `/admin/` | Django Admin | Admin dashboard |

---

## Admin Interface

Access the enhanced admin dashboard at `/admin/`:

### Features
- **Jazzmin UI**: Modern, responsive admin interface
- **Custom Branding**: Muna Kalati logo and styling
- **Quick Access**: Top menu with links to main site and admin home
- **Search**: Global search across models
- **Icons**: Custom FontAwesome icons for models
- **Responsive Design**: Works on mobile and desktop

### Manage Models
- Categories
- Latest Updates (Blog Posts)
- Featured News
- Open Positions
- Press Releases
- Social Media Posts
- Team Members
- Reviews
- Contacts
- Users & Permissions

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Write or update tests as needed
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Create a Pull Request

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to classes and complex functions
- Keep functions focused and modular

---

## Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Update `SECRET_KEY` with a secure value
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up environment variables securely
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure a production-grade web server (Gunicorn, uWSGI)
- [ ] Set up a reverse proxy (Nginx, Apache)
- [ ] Enable HTTPS with SSL/TLS certificates
- [ ] Configure static and media file serving
- [ ] Set up database backups
- [ ] Configure error logging and monitoring

### AWS Elastic Beanstalk (Optional)
The project includes AWS EB CLI configuration:
```bash
# Initialize EB environment
eb init -p python-3.x my-django-app --region us-west-2

# Create environment
eb create my-django-env

# Deploy
eb deploy

# Monitor
eb open
```

---

## Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'django'**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**Database migrations failed**
- Run `python manage.py migrate` with the current database state
- Check for conflicting migrations

**Static files not loading**
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` configuration

**Image upload errors**
- Ensure `media/` directory exists and is writable
- Check file permissions

---

## Support & Contact

For issues, questions, or suggestions, please:
1. Check existing GitHub issues
2. Create a new issue with detailed information
3. Contact the development team via the contact form on the website

---

## License

This project is part of Muna Kalati initiative. Please see the LICENSE file for details.

---

## Changelog

### Version 1.0.0 (Latest)
- Initial Django 5.1 setup
- Core content management features
- Admin dashboard with Jazzmin
- Search and recommendation engine
- Social media integration
- Team and review management

---

**Last Updated**: June 5, 2026
**Maintainer**: Murgany ([@Murgany](https://github.com/Murgany))

---

*Muna Kalati - Empowering African Children Through Afrocentric Education*
