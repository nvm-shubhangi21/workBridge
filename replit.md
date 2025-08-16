# NaukriSathi - Domestic Worker Platform

## Overview

NaukriSathi is a Streamlit-based web application designed to connect domestic workers with employers. The platform provides a comprehensive solution for worker registration, job posting, salary tracking, and worker discovery. Built with simplicity and accessibility in mind, the application features a clean, modern interface with a soft blue theme that ensures ease of use for both workers and employers.

## Recent Changes

### August 15, 2025 - Major Feature Enhancement
- **AI Bio Generator**: Implemented smart template-based bio generation for worker profiles
- **QR Code Generation**: Added QR code creation for worker contact sharing
- **Smart Job Matching**: Developed algorithm to match top 3 workers to job postings
- **Dashboard Redesign**: Modernized home page with card-based layout matching professional UI
- **Search Functionality**: Added real-time search for workers and jobs from home page
- **Hot Topics Section**: Added dynamic statistics display (worker count, job count)
- **Enhanced UI**: Implemented gradient cards, hover effects, and mobile-responsive design

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for rapid web application development
- **UI Design**: Custom CSS implementation with soft blue theme (#4A90E2) for professional appearance
- **Responsive Design**: Mobile-friendly layout with flexible button sizing and padding
- **Navigation**: Multi-page application structure with centralized navigation from home page

### Backend Architecture
- **Application Structure**: Single-file Python application (app.py) following Streamlit's page-based architecture
- **Data Processing**: Pandas integration for data manipulation and display
- **State Management**: Streamlit's built-in session state for user interactions

### Data Storage
- **Database**: SQLite for lightweight, serverless data persistence
- **Schema Design**: Three main tables:
  - `workers`: Stores worker profiles (name, skills, location, contact, rating, bio, qr_code)
  - `jobs`: Manages job postings (title, required skills, location, salary, contact)
  - `salary`: Tracks payment records (worker name, month, amount, status)

### Core Features
1. **Worker Registration System**: Form-based registration with skill tagging, rating system, AI bio generation, and QR code creation
2. **Job Posting Platform**: Employer interface for posting job opportunities with instant smart matching
3. **Salary Tracking**: Monthly payment management with status tracking
4. **Worker Discovery**: Search functionality by skills and location with AI-generated bios and QR codes
5. **Smart Job Matching**: AI-powered algorithm to match workers to job postings with percentage scores
6. **Dashboard Interface**: Modern card-based home page with search functionality and statistics

### Design Patterns
- **Component-based CSS**: Modular styling with reusable classes for consistent UI elements
- **Form-driven Interactions**: Streamlit forms for data collection and validation
- **Database Abstraction**: Direct SQLite integration with pandas for data operations

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework for Python
- **SQLite3**: Built-in Python database interface
- **Pandas**: Data manipulation and analysis library
- **QRCode**: QR code generation library for worker profiles
- **Pillow (PIL)**: Image processing for QR code handling
- **datetime**: Python standard library for date/time handling
- **os**: Python standard library for operating system interface
- **base64**: Encoding/decoding for QR code storage
- **io**: Input/output operations for image processing

### Development Dependencies
- AI bio generation using local template-based system (no external API required)
- Self-contained application with local database storage
- Browser-based execution with no desktop dependencies
- QR code generation handled locally

### Database Requirements
- SQLite database file creation and management
- No external database server required
- Local file-based storage suitable for small to medium-scale deployments