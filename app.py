import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
import qrcode
from PIL import Image
import io
import base64
import random
import re

# Custom CSS for soft blue theme and mobile-friendly design
def load_custom_css():
    st.markdown("""
    <style>
    .main {
        padding: 2rem 1rem;
    }
    
    .stApp {
        background-color: #F8FAFE;
    }
    
    .main-header {
        text-align: center;
        color: #4A90E2;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(74, 144, 226, 0.1);
    }
    
    .welcome-text {
        text-align: center;
        font-size: 1.2rem;
        color: #5A6C7D;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .nav-button {
        background: white;
        color: #2C3E50;
        padding: 1.5rem;
        border: 1px solid #F0F0F0;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 600;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        width: 100%;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    
    .nav-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 20px rgba(74, 144, 226, 0.2);
        border-color: #4A90E2;
        color: #4A90E2;
    }
    
    .stButton > button {
        background: white !important;
        color: #2C3E50 !important;
        border: 1px solid #F0F0F0 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 1.5rem !important;
        height: 120px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 4px 20px rgba(74, 144, 226, 0.2) !important;
        border-color: #4A90E2 !important;
        color: #4A90E2 !important;
    }
    
    .section-header {
        color: #4A90E2;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #E8F4FD;
        padding-bottom: 0.5rem;
    }
    
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #E8F4FD;
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #E8F4FD;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #E8F4FD;
    }
    
    .success-message {
        background: #D4F6DD;
        color: #2D5A3D;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #FFE6E6;
        color: #C62828;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #F44336;
        margin: 1rem 0;
    }
    
    .ai-bio-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .match-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(17, 153, 142, 0.3);
    }
    
    .qr-container {
        text-align: center;
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px dashed #4A90E2;
        margin: 1rem 0;
    }
    
    .wow-feature {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
    }
    
    .feature-highlight {
        background: #FFF8E1;
        border: 2px solid #FFB74D;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #E65100;
    }
    
    .search-container {
        background: white;
        border-radius: 25px;
        padding: 0.5rem 1rem;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #E0E0E0;
    }
    
    .dashboard-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid #F0F0F0;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 20px rgba(74, 144, 226, 0.2);
        border-color: #4A90E2;
    }
    
    .card-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        color: #4A90E2;
    }
    
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: #2C3E50;
        margin: 0;
    }
    
    .hot-topics-section {
        margin-top: 3rem;
    }
    
    .hot-topic-item {
        background: white;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #4A90E2;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s ease;
    }
    
    .hot-topic-item:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        transform: translateX(5px);
    }
    
    .topic-title {
        font-weight: 500;
        color: #2C3E50;
        margin: 0;
    }
    
    .topic-icon {
        color: #4A90E2;
        font-size: 1.2rem;
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .welcome-text {
            font-size: 1rem;
        }
        
        .form-container {
            padding: 1.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize database
def init_db():
    conn = sqlite3.connect('naukrisathi.db')
    cursor = conn.cursor()
    
    # Create workers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            skills TEXT NOT NULL,
            location TEXT NOT NULL,
            contact TEXT NOT NULL,
            rating INTEGER NOT NULL,
            bio TEXT,
            qr_code TEXT,
            profile_picture TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT NOT NULL,
            required_skills TEXT NOT NULL,
            location TEXT NOT NULL,
            offered_salary TEXT NOT NULL,
            contact TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create salary table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS salary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_name TEXT NOT NULL,
            month TEXT NOT NULL,
            salary_amount REAL NOT NULL,
            payment_status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create requests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employer_name TEXT NOT NULL,
            employer_contact TEXT NOT NULL,
            worker_id INTEGER NOT NULL,
            job_title TEXT NOT NULL,
            message TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (worker_id) REFERENCES workers (id)
        )
    ''')
    
    # Create availability table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS availability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            is_available BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (worker_id) REFERENCES workers (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Database operations
def add_worker(name, skills, location, contact, rating, bio=None, qr_code=None, profile_picture=None):
    conn = sqlite3.connect('naukrisathi.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO workers (name, skills, location, contact, rating, bio, qr_code, profile_picture)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, skills, location, contact, rating, bio, qr_code, profile_picture))
    conn.commit()
    conn.close()

def add_job(job_title, required_skills, location, offered_salary, contact):
    conn = sqlite3.connect('naukrisathi.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO jobs (job_title, required_skills, location, offered_salary, contact)
        VALUES (?, ?, ?, ?, ?)
    ''', (job_title, required_skills, location, offered_salary, contact))
    conn.commit()
    conn.close()

def add_salary_record(worker_name, month, salary_amount, payment_status):
    conn = sqlite3.connect('naukrisathi.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO salary (worker_name, month, salary_amount, payment_status)
        VALUES (?, ?, ?, ?)
    ''', (worker_name, month, salary_amount, payment_status))
    conn.commit()
    conn.close()

def get_workers():
    conn = sqlite3.connect('naukrisathi.db')
    df = pd.read_sql_query("SELECT * FROM workers", conn)
    conn.close()
    return df

def get_worker_names():
    conn = sqlite3.connect('naukrisathi.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM workers")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names

def search_workers(skill_filter="", location_filter=""):
    conn = sqlite3.connect('naukrisathi.db')
    query = "SELECT * FROM workers WHERE 1=1"
    params = []
    
    if skill_filter:
        query += " AND skills LIKE ?"
        params.append(f"%{skill_filter}%")
    
    if location_filter:
        query += " AND location LIKE ?"
        params.append(f"%{location_filter}%")
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_jobs():
    conn = sqlite3.connect('naukrisathi.db')
    df = pd.read_sql_query("SELECT * FROM jobs ORDER BY created_at DESC", conn)
    conn.close()
    return df

def get_worker_by_id(worker_id):
    conn = sqlite3.connect('naukrisathi.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workers WHERE id = ?", (worker_id,))
    worker = cursor.fetchone()
    conn.close()
    return worker

# AI Bio Generator (Smart Template System)
def generate_worker_bio(name, skills, location, rating):
    """Generate professional bio using smart templates"""
    skills_list = [skill.strip().title() for skill in skills.split(',')]
    
    # Bio templates based on skills
    templates = {
        'cooking': f"Meet {name}, a skilled culinary professional specializing in {', '.join(skills_list[:3])}. Based in {location}, {name} brings {rating} years of experience creating delicious, nutritious meals for families.",
        'cleaning': f"{name} is a meticulous and reliable cleaning professional from {location}. With expertise in {', '.join(skills_list[:3])}, {name} ensures every space is spotless and organized to perfection.",
        'childcare': f"Introducing {name}, a caring and experienced childcare provider located in {location}. Specializing in {', '.join(skills_list[:3])}, {name} creates safe, nurturing environments for children to learn and grow.",
        'eldercare': f"{name} is a compassionate eldercare specialist from {location}. With skills in {', '.join(skills_list[:3])}, {name} provides dignified, professional care for seniors and their families."
    }
    
    # Determine primary skill category
    skills_lower = skills.lower()
    if any(word in skills_lower for word in ['cook', 'kitchen', 'meal', 'food']):
        bio = templates['cooking']
    elif any(word in skills_lower for word in ['clean', 'housekeep', 'laundry', 'organize']):
        bio = templates['cleaning']
    elif any(word in skills_lower for word in ['child', 'baby', 'nanny', 'kid']):
        bio = templates['childcare']
    elif any(word in skills_lower for word in ['elder', 'senior', 'care']):
        bio = templates['eldercare']
    else:
        bio = f"{name} is a dedicated domestic professional from {location} with expertise in {', '.join(skills_list[:3])}. With a {rating}-star rating, {name} brings reliability and excellence to every task."
    
    # Add rating-based enhancement
    if rating >= 4:
        bio += f" Known for exceptional service quality and attention to detail."
    elif rating >= 3:
        bio += f" Committed to providing reliable and professional service."
    
    return bio

# QR Code Generator
def generate_qr_code(worker_data):
    """Generate QR code for worker profile"""
    # Create profile text
    profile_text = f"""NaukriSathi Worker Profile
Name: {worker_data['name']}
Skills: {worker_data['skills']}
Location: {worker_data['location']}
Contact: {worker_data['contact']}
Rating: {worker_data['rating']}/5 stars"""
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(profile_text)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for storage
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return qr_base64

# Smart Job Matching Algorithm
def find_best_workers_for_job(job_skills, job_location, top_n=3):
    """Find top matching workers for a job"""
    workers_df = get_workers()
    
    if workers_df.empty:
        return pd.DataFrame()
    
    # Calculate match scores
    match_scores = []
    
    for idx, worker in workers_df.iterrows():
        score = 0
        
        # Skill matching (70% weight)
        job_skills_list = [skill.strip().lower() for skill in job_skills.split(',')]
        worker_skills_list = [skill.strip().lower() for skill in str(worker['skills']).split(',')]
        
        skill_matches = len(set(job_skills_list) & set(worker_skills_list))
        skill_score = (skill_matches / max(len(job_skills_list), 1)) * 70
        
        # Location matching (20% weight)
        worker_location = str(worker['location']).lower()
        job_location_lower = job_location.lower()
        location_score = 20 if job_location_lower in worker_location or worker_location in job_location_lower else 0
        
        # Rating bonus (10% weight)
        rating_score = (worker['rating'] / 5) * 10
        
        total_score = skill_score + location_score + rating_score
        match_scores.append(total_score)
    
    # Add match scores to dataframe
    workers_df['match_score'] = match_scores
    
    # Sort by match score and return top N
    best_matches = workers_df.nlargest(top_n, 'match_score')
    
    return best_matches

# New functions for enhanced features
def add_request(employer_name, employer_contact, worker_id, job_title, message):
    conn = sqlite3.connect('naukrisathi.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (employer_name, employer_contact, worker_id, job_title, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (employer_name, employer_contact, worker_id, job_title, message))
    conn.commit()
    conn.close()

def get_worker_requests(worker_id):
    conn = sqlite3.connect('naukrisathi.db')
    df = pd.read_sql_query("SELECT * FROM requests WHERE worker_id = ? ORDER BY created_at DESC", conn, params=[worker_id])
    conn.close()
    return df

def update_request_status(request_id, status):
    conn = sqlite3.connect('naukrisathi.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE requests SET status = ? WHERE id = ?", (status, request_id))
    conn.commit()
    conn.close()

def add_availability(worker_id, date, time_slot, is_available=True):
    conn = sqlite3.connect('naukrisathi.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO availability (worker_id, date, time_slot, is_available)
        VALUES (?, ?, ?, ?)
    ''', (worker_id, date, time_slot, is_available))
    conn.commit()
    conn.close()

def get_worker_availability(worker_id):
    conn = sqlite3.connect('naukrisathi.db')
    df = pd.read_sql_query("SELECT * FROM availability WHERE worker_id = ? ORDER BY date, time_slot", conn, params=[worker_id])
    conn.close()
    return df

def save_profile_picture(uploaded_file):
    """Save uploaded profile picture and return base64 string"""
    if uploaded_file is not None:
        try:
            # Read the file and convert to base64
            image = Image.open(uploaded_file)
            # Resize image to reasonable size (300x300)
            image = image.resize((300, 300), Image.Resampling.LANCZOS)
            
            # Convert to base64
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            return img_base64
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            return None
    return None

# Navigation functions
def show_home():
    # Top search bar with functionality
    search_query = st.text_input("Search", placeholder="Search for jobs or workers", key="home_search", label_visibility="collapsed")
    
    # If search query exists, show search results
    if search_query:
        st.markdown(f"### 🔍 Search Results for: '{search_query}'")
        
        # Search workers
        workers_results = search_workers(search_query, search_query)
        if not workers_results.empty:
            st.markdown("**👥 Matching Workers:**")
            for _, worker in workers_results.head(3).iterrows():
                st.markdown(f"- **{worker['name']}** | {worker['skills']} | {worker['location']}")
        
        # Search in job titles and skills
        jobs_df = get_jobs()
        if not jobs_df.empty:
            job_matches = jobs_df[jobs_df['job_title'].str.contains(search_query, case=False, na=False) | 
                                 jobs_df['required_skills'].str.contains(search_query, case=False, na=False)]
            if not job_matches.empty:
                st.markdown("**💼 Matching Jobs:**")
                for _, job in job_matches.head(3).iterrows():
                    st.markdown(f"- **{job['job_title']}** | {job['required_skills']} | {job['location']}")
        
        st.markdown("---")
        if st.button("❌ Clear Search"):
            st.session_state.home_search = ""
            st.rerun()
        return
    
    # Title
    st.markdown('<h1 class="main-header">NaukriSathi</h1>', unsafe_allow_html=True)
    
    # Dashboard cards in grid layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Worker Registration Card
        if st.button("👤 Worker Registration", key="nav_worker_reg", help="Register new workers"):
            st.session_state.page = "worker_registration"
            st.rerun()
        st.markdown('''
        <div style="margin-bottom: 1rem;"></div>
        ''', unsafe_allow_html=True)
        
        # Salary Tracker Card
        if st.button("💰 Salary Tracker", key="nav_salary", help="Track worker payments"):
            st.session_state.page = "salary_tracker"
            st.rerun()
        st.markdown('''
        <div style="margin-bottom: 1rem;"></div>
        ''', unsafe_allow_html=True)
        
        # Reports Card
        if st.button("📊 Reports", key="nav_reports", help="View platform statistics and reports"):
            st.session_state.page = "reports"
            st.rerun()
    
    with col2:
        # Job Posting Card
        if st.button("📝 Job Posting", key="nav_job_post", help="Post new job opportunities"):
            st.session_state.page = "job_posting"
            st.rerun()
        st.markdown('''
        <div style="margin-bottom: 1rem;"></div>
        ''', unsafe_allow_html=True)
        
        # View Workers Card
        if st.button("👥 View Workers", key="nav_view_workers", help="Browse worker profiles"):
            st.session_state.page = "view_workers"
            st.rerun()
        st.markdown('''
        <div style="margin-bottom: 1rem;"></div>
        ''', unsafe_allow_html=True)
        
        # Worker Dashboard Card
        if st.button("📋 Worker Dashboard", key="nav_worker_dashboard", help="Worker profile management"):
            st.session_state.page = "worker_dashboard"
            st.rerun()
        st.markdown('''
        <div style="margin-bottom: 1rem;"></div>
        ''', unsafe_allow_html=True)
        
        # Notifications Card
        if st.button("🔔 Notifications", key="nav_notifications", help="View recent activities and alerts"):
            st.session_state.page = "notifications"
            st.rerun()
    
    # Smart Matching button (full width)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎯 Smart Job Matching", key="nav_smart_match", help="AI-powered job matching", use_container_width=True):
        st.session_state.page = "smart_matching"
        st.rerun()
    
    # Hot Topics Section
    st.markdown('''
    <div class="hot-topics-section">
        <h3 style="color: #2C3E50; margin-bottom: 1rem;">Hot Topics</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Hot topic items
    workers_count = len(get_workers()) if not get_workers().empty else 0
    jobs_count = len(get_jobs()) if not get_jobs().empty else 0
    
    st.markdown(f'''
    <div class="hot-topic-item">
        <div class="topic-title">New Worker Registration Process (👤 {workers_count} workers)</div>
        <div class="topic-icon">🔗</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="hot-topic-item">
        <div class="topic-title">Job Market Trends (💼 {jobs_count} active jobs)</div>
        <div class="topic-icon">🔗</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="hot-topic-item">
        <div class="topic-title">AI-Powered Salary Insights & Matching</div>
        <div class="topic-icon">🔗</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Feature highlight at bottom
    st.markdown('''
    <div class="feature-highlight" style="margin-top: 2rem;">
        <strong>✨ Platform Features:</strong><br>
        🤖 AI Bio Generator • 🎯 Smart Job Matching • 📱 QR Code Profiles • 💰 Payment Tracking
    </div>
    ''', unsafe_allow_html=True)

def show_worker_registration():
    st.markdown('<h2 class="section-header">👤 Worker Registration</h2>', unsafe_allow_html=True)
    st.markdown('**Register your profile and get an AI-generated professional bio + QR code instantly!**')
    
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("worker_form"):
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            skills = st.text_input("Skills *", placeholder="e.g., Cooking, Cleaning, Baby Care, Elder Care")
            location = st.text_input("Location *", placeholder="Enter your city/area")
            contact = st.text_input("Contact Number *", placeholder="Enter your phone number")
            rating = st.slider("Experience Rating", 1, 5, 3, help="Rate your experience level (1-5 stars)")
            
            # Profile picture upload
            st.markdown("**Profile Picture**")
            uploaded_file = st.file_uploader("Upload your photo (optional)", type=['png', 'jpg', 'jpeg'], help="Add a professional photo to your profile")
            
            submitted = st.form_submit_button("Register Worker", use_container_width=True)
            
            if submitted:
                if name and skills and location and contact:
                    try:
                        # Generate AI bio
                        ai_bio = generate_worker_bio(name, skills, location, rating)
                        
                        # Save profile picture if uploaded
                        profile_picture = save_profile_picture(uploaded_file)
                        
                        # Generate QR code
                        worker_data = {'name': name, 'skills': skills, 'location': location, 'contact': contact, 'rating': rating}
                        qr_code = generate_qr_code(worker_data)
                        
                        # Save worker with bio, QR code, and profile picture
                        add_worker(name, skills, location, contact, rating, ai_bio, qr_code, profile_picture)
                        
                        st.success(f"✅ Worker {name} registered successfully!")
                        st.balloons()
                        
                        # Show AI-generated bio
                        st.markdown(f'''
                        <div class="ai-bio-container">
                            <h4>🤖 AI-Generated Professional Bio:</h4>
                            <p style="font-size: 1.1rem; line-height: 1.6;">{ai_bio}</p>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        # Show QR code
                        st.markdown('''
                        <div class="qr-container">
                            <h4>📱 Your QR Code Profile</h4>
                            <p>Employers can scan this to instantly view your contact details!</p>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        # Display QR code
                        qr_image = Image.open(io.BytesIO(base64.b64decode(qr_code)))
                        col1, col2, col3 = st.columns([1, 1, 1])
                        with col2:
                            st.image(qr_image, width=200)
                        
                    except Exception as e:
                        st.error(f"❌ Error registering worker: {str(e)}")
                else:
                    st.error("❌ Please fill in all required fields marked with *")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def show_job_posting():
    st.markdown('<h2 class="section-header">📝 Job Posting</h2>', unsafe_allow_html=True)
    st.markdown('**Post your job and instantly see the top 3 matching workers!**')
    
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        with st.form("job_form"):
            job_title = st.text_input("Job Title *", placeholder="e.g., House Maid, Cook, Nanny")
            required_skills = st.text_input("Required Skills *", placeholder="e.g., Cooking, Cleaning, Child Care")
            location = st.text_input("Job Location *", placeholder="Enter city/area where work is needed")
            offered_salary = st.text_input("Offered Salary *", placeholder="e.g., ₹15,000/month or ₹500/day")
            contact = st.text_input("Contact Information *", placeholder="Your phone number or email")
            
            submitted = st.form_submit_button("Post Job", use_container_width=True)
            
            if submitted:
                if job_title and required_skills and location and offered_salary and contact:
                    try:
                        add_job(job_title, required_skills, location, offered_salary, contact)
                        st.success(f"✅ Job '{job_title}' posted successfully!")
                        st.balloons()
                        
                        # Show smart matching results
                        st.markdown('''
                        <div class="wow-feature">
                            🎯 Smart Matching: Finding your perfect workers...
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        best_workers = find_best_workers_for_job(required_skills, location)
                        
                        if not best_workers.empty:
                            st.markdown("### 🌟 Top 3 Matching Workers for Your Job:")
                            for idx, worker in best_workers.iterrows():
                                match_percentage = min(100, int(worker['match_score']))
                                st.markdown(f'''
                                <div class="match-card">
                                    <strong>👤 {worker['name']}</strong> - {match_percentage}% Match<br>
                                    🛠️ Skills: {worker['skills']}<br>
                                    📍 Location: {worker['location']}<br>
                                    📞 Contact: {worker['contact']}<br>
                                    ⭐ Rating: {worker['rating']}/5
                                </div>
                                ''', unsafe_allow_html=True)
                        else:
                            st.info("🔍 No workers registered yet. Encourage workers to join the platform!")
                            
                    except Exception as e:
                        st.error(f"❌ Error posting job: {str(e)}")
                else:
                    st.error("❌ Please fill in all required fields marked with *")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def show_salary_tracker():
    st.markdown('<h2 class="section-header">💰 Salary Tracker</h2>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        worker_names = get_worker_names()
        
        if not worker_names:
            st.warning("⚠️ No workers registered yet. Please register workers first.")
            if st.button("👤 Go to Worker Registration"):
                st.session_state.page = "worker_registration"
                st.rerun()
        else:
            with st.form("salary_form"):
                worker_name = st.selectbox("Select Worker *", worker_names)
                
                months = ["January", "February", "March", "April", "May", "June",
                         "July", "August", "September", "October", "November", "December"]
                month = st.selectbox("Month *", months)
                
                salary_amount = st.number_input("Salary Amount (₹) *", min_value=0.0, step=100.0, format="%.2f")
                payment_status = st.selectbox("Payment Status *", ["Paid", "Unpaid"])
                
                submitted = st.form_submit_button("Save Salary Record", use_container_width=True)
                
                if submitted:
                    if worker_name and month and salary_amount > 0:
                        try:
                            add_salary_record(worker_name, month, salary_amount, payment_status)
                            st.success(f"✅ Salary record for {worker_name} in {month} saved successfully!")
                            st.balloons()
                        except Exception as e:
                            st.error(f"❌ Error saving salary record: {str(e)}")
                    else:
                        st.error("❌ Please fill in all required fields with valid values")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def show_view_workers():
    st.markdown('<h2 class="section-header">👥 View Workers</h2>', unsafe_allow_html=True)
    st.markdown('**Browse worker profiles with AI-generated bios and QR codes!**')
    
    # Search filters
    col1, col2 = st.columns(2)
    with col1:
        skill_filter = st.text_input("🔍 Search by Skill", placeholder="e.g., Cooking, Cleaning")
    with col2:
        location_filter = st.text_input("📍 Search by Location", placeholder="e.g., Mumbai, Delhi")
    
    # Get workers data
    if skill_filter or location_filter:
        workers_df = search_workers(skill_filter, location_filter)
    else:
        workers_df = get_workers()
    
    if workers_df.empty:
        st.info("📋 No workers found matching your search criteria.")
        if st.button("👤 Register First Worker"):
            st.session_state.page = "worker_registration"
            st.rerun()
    else:
        st.markdown(f"**Found {len(workers_df)} worker(s):**")
        
        # Display workers in cards
        for idx, worker in workers_df.iterrows():
            with st.container():
                st.markdown("""
                <div style="background: white; padding: 1.5rem; margin: 1rem 0; 
                           border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                           border-left: 4px solid #4A90E2;">
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
                
                with col1:
                    # Show profile picture if available
                    try:
                        if 'profile_picture' in worker and pd.notna(worker['profile_picture']) and worker['profile_picture']:
                            img_data = base64.b64decode(worker['profile_picture'])
                            st.image(Image.open(io.BytesIO(img_data)), width=80, caption="")
                        else:
                            st.markdown("<div style='text-align:center; font-size:3rem;'>👤</div>", unsafe_allow_html=True)
                    except:
                        st.markdown("<div style='text-align:center; font-size:3rem;'>👤</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**{worker['name']}**")
                    st.markdown(f"📍 {worker['location']}")
                    # Add request button for employers
                    if st.button(f"📝 Send Request", key=f"req_{worker['id']}"):
                        st.session_state[f'show_request_form_{worker["id"]}'] = True
                        st.rerun()
                
                with col3:
                    st.markdown(f"🛠️ **Skills:** {worker['skills']}")
                    st.markdown(f"📞 **Contact:** {worker['contact']}")
                
                with col4:
                    rating_stars = "⭐" * worker['rating']
                    st.markdown(f"**Rating:**")
                    st.markdown(f"{rating_stars} ({worker['rating']}/5)")
                
                # Show request form if button was clicked
                if st.session_state.get(f'show_request_form_{worker["id"]}', False):
                    with st.form(f"request_form_{worker['id']}"):
                        st.markdown(f"**Send Request to {worker['name']}**")
                        employer_name = st.text_input("Your Name *")
                        employer_contact = st.text_input("Your Contact *")
                        job_title = st.text_input("Job Title *")
                        message = st.text_area("Message (optional)", placeholder="Describe your requirements...")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.form_submit_button("Send Request"):
                                if employer_name and employer_contact and job_title:
                                    add_request(employer_name, employer_contact, worker['id'], job_title, message)
                                    st.success(f"✅ Request sent to {worker['name']}!")
                                    st.session_state[f'show_request_form_{worker["id"]}'] = False
                                    st.rerun()
                                else:
                                    st.error("Please fill in all required fields")
                        with col_b:
                            if st.form_submit_button("Cancel"):
                                st.session_state[f'show_request_form_{worker["id"]}'] = False
                                st.rerun()
                
                # Show AI bio if available
                try:
                    if hasattr(worker, 'bio') and pd.notna(worker.bio) and str(worker.bio).strip():
                        st.markdown(f'''
                        <div style="background: #F0F8FF; padding: 0.8rem; border-radius: 6px; margin-top: 0.5rem;">
                            <strong>🤖 Professional Bio:</strong><br>
                            <em>{worker.bio}</em>
                        </div>
                        ''', unsafe_allow_html=True)
                except:
                    pass
                
                # Show QR code button
                try:
                    if hasattr(worker, 'qr_code') and pd.notna(worker.qr_code) and str(worker.qr_code).strip():
                        if st.button(f"📱 View QR Code", key=f"qr_{worker.id}"):
                            try:
                                qr_image = Image.open(io.BytesIO(base64.b64decode(str(worker.qr_code))))
                                st.image(qr_image, width=150, caption=f"QR Code for {worker['name']}")
                            except Exception as e:
                                st.error(f"Error loading QR code: {str(e)}")
                except:
                    pass
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def show_smart_matching():
    st.markdown('<h2 class="section-header">🎯 Smart Job Matching</h2>', unsafe_allow_html=True)
    st.markdown('**See how our AI matches workers to available jobs!**')
    
    jobs_df = get_jobs()
    workers_df = get_workers()
    
    if jobs_df.empty:
        st.warning("⚠️ No jobs posted yet. Post some jobs first!")
        if st.button("📝 Post a Job"):
            st.session_state.page = "job_posting"
            st.rerun()
        return
    
    if workers_df.empty:
        st.warning("⚠️ No workers registered yet. Register workers first!")
        if st.button("👤 Register Worker"):
            st.session_state.page = "worker_registration"
            st.rerun()
        return
    
    st.markdown(f"**Available Jobs: {len(jobs_df)} | Registered Workers: {len(workers_df)}**")
    
    # Show job matching results
    for idx, job in jobs_df.iterrows():
        st.markdown(f"### 📋 {job['job_title']}")
        st.markdown(f"**Required Skills:** {job['required_skills']} | **Location:** {job['location']} | **Salary:** {job['offered_salary']}")
        
        # Find best matches for this job
        best_workers = find_best_workers_for_job(job['required_skills'], job['location'])
        
        if not best_workers.empty:
            st.markdown("**🌟 Top Matching Workers:**")
            
            col1, col2, col3 = st.columns(3)
            
            for i, (_, worker) in enumerate(best_workers.iterrows()):
                match_percentage = min(100, int(worker['match_score']))
                
                with [col1, col2, col3][i % 3]:
                    st.markdown(f'''
                    <div class="match-card">
                        <strong>👤 {worker['name']}</strong><br>
                        🎯 {match_percentage}% Match<br>
                        🛠️ {worker['skills']}<br>
                        📍 {worker['location']}<br>
                        ⭐ {worker['rating']}/5<br>
                        📞 {worker['contact']}
                    </div>
                    ''', unsafe_allow_html=True)
        else:
            st.info("🔍 No suitable workers found for this job.")
        
        st.markdown("---")
    
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def show_reports():
    st.markdown('<h2 class="section-header">📊 Platform Reports</h2>', unsafe_allow_html=True)
    st.markdown('**Comprehensive analytics and insights for the NaukriSathi platform**')
    
    # Get data for reports
    workers_df = get_workers()
    jobs_df = get_jobs()
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Workers", len(workers_df))
    with col2:
        st.metric("Active Jobs", len(jobs_df))
    with col3:
        avg_rating = workers_df['rating'].mean() if not workers_df.empty else 0
        st.metric("Avg Worker Rating", f"{avg_rating:.1f}/5")
    with col4:
        # Get unique skills count
        if not workers_df.empty:
            all_skills = []
            for skills in workers_df['skills']:
                all_skills.extend([s.strip() for s in str(skills).split(',')])
            unique_skills = len(set(all_skills))
        else:
            unique_skills = 0
        st.metric("Skill Categories", unique_skills)
    
    st.markdown("---")
    
    # Charts and detailed analytics
    if not workers_df.empty:
        st.markdown("### 📈 Worker Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Rating distribution
            rating_counts = workers_df['rating'].value_counts().sort_index()
            st.markdown("**Rating Distribution:**")
            for rating, count in rating_counts.items():
                stars = "⭐" * rating
                st.markdown(f"{stars} ({rating}/5): {count} workers")
        
        with col2:
            # Top locations
            location_counts = workers_df['location'].value_counts().head(5)
            st.markdown("**Top Locations:**")
            for location, count in location_counts.items():
                st.markdown(f"📍 {location}: {count} workers")
        
        # Skills analysis
        st.markdown("### 🛠️ Skills Analysis")
        skill_counts = {}
        for skills in workers_df['skills']:
            for skill in str(skills).split(','):
                skill = skill.strip().title()
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Top 10 skills
        top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        for skill, count in top_skills:
            progress = count / len(workers_df)
            st.progress(progress, text=f"{skill}: {count} workers")
    
    if not jobs_df.empty:
        st.markdown("### 💼 Job Market Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Job locations
            job_location_counts = jobs_df['location'].value_counts().head(5)
            st.markdown("**Job Hotspots:**")
            for location, count in job_location_counts.items():
                st.markdown(f"📍 {location}: {count} jobs")
        
        with col2:
            # Recent jobs
            st.markdown("**Recent Job Postings:**")
            for _, job in jobs_df.head(5).iterrows():
                st.markdown(f"• {job['job_title']} in {job['location']}")
    
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def show_notifications():
    st.markdown('<h2 class="section-header">🔔 Notifications</h2>', unsafe_allow_html=True)
    st.markdown('**Stay updated with recent platform activities and alerts**')
    
    # Generate dynamic notifications based on actual data
    workers_df = get_workers()
    jobs_df = get_jobs()
    
    notifications = []
    
    # Recent worker registrations
    if not workers_df.empty:
        recent_workers = workers_df.tail(3)
        for _, worker in recent_workers.iterrows():
            notifications.append({
                'icon': '👤',
                'title': 'New Worker Registration',
                'message': f"{worker['name']} joined as a {worker['skills'].split(',')[0].strip()} specialist in {worker['location']}",
                'type': 'success',
                'time': 'Recently'
            })
    
    # Recent job postings
    if not jobs_df.empty:
        recent_jobs = jobs_df.tail(2)
        for _, job in recent_jobs.iterrows():
            notifications.append({
                'icon': '💼',
                'title': 'New Job Posted',
                'message': f"'{job['job_title']}' position available in {job['location']} - {job['offered_salary']}",
                'type': 'info',
                'time': 'Recently'
            })
    
    # Platform insights
    if len(workers_df) > 0 and len(jobs_df) > 0:
        notifications.append({
            'icon': '🎯',
            'title': 'Smart Matching Available',
            'message': f"AI found potential matches between {len(jobs_df)} jobs and {len(workers_df)} workers. Check Smart Job Matching!",
            'type': 'highlight',
            'time': 'Now'
        })
    
    # System notifications
    notifications.extend([
        {
            'icon': '✨',
            'title': 'New Feature Alert',
            'message': 'AI Bio Generator and QR Code profiles are now live! Enhanced worker registration experience.',
            'type': 'feature',
            'time': 'Today'
        },
        {
            'icon': '📊',
            'title': 'Platform Growth',
            'message': f"Platform growing! {len(workers_df)} workers and {len(jobs_df)} jobs now available.",
            'type': 'stats',
            'time': 'Today'
        }
    ])
    
    # Display notifications
    for notif in notifications:
        # Set colors based on notification type
        if notif['type'] == 'success':
            bg_color = '#D4F6DD'
            border_color = '#4CAF50'
        elif notif['type'] == 'info':
            bg_color = '#E3F2FD'
            border_color = '#2196F3'
        elif notif['type'] == 'highlight':
            bg_color = '#FFF3E0'
            border_color = '#FF9800'
        elif notif['type'] == 'feature':
            bg_color = '#F3E5F5'
            border_color = '#9C27B0'
        else:
            bg_color = '#F5F5F5'
            border_color = '#757575'
        
        st.markdown(f'''
        <div style="
            background: {bg_color};
            border-left: 4px solid {border_color};
            border-radius: 8px;
            padding: 1rem;
            margin: 0.8rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem; margin-right: 0.8rem;">{notif['icon']}</span>
                <strong style="color: #2C3E50;">{notif['title']}</strong>
                <span style="margin-left: auto; color: #666; font-size: 0.9rem;">{notif['time']}</span>
            </div>
            <div style="color: #444; line-height: 1.4;">{notif['message']}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("### 💬 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👤 View All Workers"):
            st.session_state.page = "view_workers"
            st.rerun()
    
    with col2:
        if st.button("💼 Check Jobs"):
            st.session_state.page = "job_posting"
            st.rerun()
    
    with col3:
        if st.button("🎯 Smart Matching"):
            st.session_state.page = "smart_matching"
            st.rerun()
    
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def show_worker_dashboard():
    st.markdown('<h2 class="section-header">📋 Worker Dashboard</h2>', unsafe_allow_html=True)
    st.markdown('**Manage your profile, requests, and availability**')
    
    # Worker selection
    workers_df = get_workers()
    if workers_df.empty:
        st.warning("⚠️ No workers registered yet. Please register first!")
        if st.button("👤 Go to Worker Registration"):
            st.session_state.page = "worker_registration"
            st.rerun()
        return
    
    worker_names = workers_df['name'].tolist()
    selected_worker_name = st.selectbox("Select Your Profile", worker_names)
    
    # Get selected worker details
    selected_worker = workers_df[workers_df['name'] == selected_worker_name].iloc[0]
    worker_id = selected_worker['id']
    
    # Dashboard tabs
    tab1, tab2, tab3 = st.tabs(["📬 Employer Requests", "📅 Availability Calendar", "👤 Profile Settings"])
    
    with tab1:
        st.markdown("### 📬 Employer Requests")
        
        # Get and display requests
        requests_df = get_worker_requests(worker_id)
        
        if requests_df.empty:
            st.info("📭 No requests yet. Employers will send you job requests here!")
        else:
            st.markdown(f"**You have {len(requests_df)} request(s)**")
            
            for _, request in requests_df.iterrows():
                # Color coding for status
                if request['status'] == 'pending':
                    bg_color = '#FFF3E0'
                    border_color = '#FF9800'
                elif request['status'] == 'accepted':
                    bg_color = '#E8F5E8'
                    border_color = '#4CAF50'
                else:
                    bg_color = '#FFEBEE'
                    border_color = '#F44336'
                
                st.markdown(f'''
                <div style="background: {bg_color}; border-left: 4px solid {border_color}; 
                           padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: #2C3E50;">📝 {request['job_title']}</h4>
                        <span style="background: {border_color}; color: white; padding: 0.3rem 0.8rem; 
                                   border-radius: 15px; font-size: 0.8rem; font-weight: bold;">
                            {request['status'].upper()}
                        </span>
                    </div>
                    <p><strong>👤 Employer:</strong> {request['employer_name']}</p>
                    <p><strong>📞 Contact:</strong> {request['employer_contact']}</p>
                    {f"<p><strong>💬 Message:</strong> {request['message']}</p>" if request['message'] else ""}
                    <p><strong>📅 Received:</strong> {request['created_at']}</p>
                </div>
                ''', unsafe_allow_html=True)
                
                if request['status'] == 'pending':
                    col_a, col_b, col_c = st.columns([1, 1, 4])
                    with col_a:
                        if st.button("✅ Accept", key=f"accept_{request['id']}"):
                            update_request_status(request['id'], 'accepted')
                            st.success("Request accepted!")
                            st.rerun()
                    with col_b:
                        if st.button("❌ Decline", key=f"decline_{request['id']}"):
                            update_request_status(request['id'], 'declined')
                            st.success("Request declined!")
                            st.rerun()
    
    with tab2:
        st.markdown("### 📅 Availability Calendar")
        st.markdown("Set your available days and time slots for employers to see")
        
        # Date and time selection
        col1, col2 = st.columns(2)
        
        with col1:
            selected_date = st.date_input("Select Date")
        with col2:
            time_slots = [
                "Morning (6AM-12PM)", "Afternoon (12PM-6PM)", 
                "Evening (6PM-10PM)", "Full Day", "Custom Hours"
            ]
            selected_time = st.selectbox("Time Slot", time_slots)
        
        if st.button("✅ Set as Available"):
            add_availability(worker_id, str(selected_date), selected_time, True)
            st.success(f"✅ Marked as available on {selected_date} for {selected_time}")
            st.rerun()
        
        # Show current availability
        availability_df = get_worker_availability(worker_id)
        
        if not availability_df.empty:
            st.markdown("### 📋 Your Current Availability")
            
            for _, avail in availability_df.iterrows():
                status_icon = "✅" if avail['is_available'] else "❌"
                st.markdown(f"**{status_icon} {avail['date']}** - {avail['time_slot']}")
        else:
            st.info("📅 No availability set yet. Add your available slots above!")
    
    with tab3:
        st.markdown("### 👤 Profile Settings")
        st.markdown("View and manage your profile information")
        
        # Show current profile
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Show profile picture
            try:
                if pd.notna(selected_worker.get('profile_picture')) and selected_worker['profile_picture']:
                    img_data = base64.b64decode(selected_worker['profile_picture'])
                    st.image(Image.open(io.BytesIO(img_data)), width=150, caption="Your Profile Picture")
                else:
                    st.markdown("<div style='text-align:center; font-size:5rem;'>👤</div>", unsafe_allow_html=True)
            except:
                st.markdown("<div style='text-align:center; font-size:5rem;'>👤</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**Name:** {selected_worker['name']}")
            st.markdown(f"**Skills:** {selected_worker['skills']}")
            st.markdown(f"**Location:** {selected_worker['location']}")
            st.markdown(f"**Contact:** {selected_worker['contact']}")
            st.markdown(f"**Rating:** {'⭐' * selected_worker['rating']} ({selected_worker['rating']}/5)")
            
            # Show AI bio if available
            if pd.notna(selected_worker.get('bio')):
                st.markdown(f"**🤖 Professional Bio:**")
                st.markdown(f"*{selected_worker['bio']}*")
            
            # Show QR code if available
            if pd.notna(selected_worker.get('qr_code')):
                if st.button("📱 Show My QR Code"):
                    try:
                        qr_image = Image.open(io.BytesIO(base64.b64decode(selected_worker['qr_code'])))
                        st.image(qr_image, width=200, caption="Share this QR code with employers!")
                    except Exception as e:
                        st.error(f"Error loading QR code: {str(e)}")
    
    if st.button("🏠 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# Main application
def main():
    st.set_page_config(
        page_title="NaukriSathi - Domestic Worker Platform",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize database
    init_db()
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    
    # Navigation
    if st.session_state.page == "home":
        show_home()
    elif st.session_state.page == "worker_registration":
        show_worker_registration()
    elif st.session_state.page == "job_posting":
        show_job_posting()
    elif st.session_state.page == "salary_tracker":
        show_salary_tracker()
    elif st.session_state.page == "view_workers":
        show_view_workers()
    elif st.session_state.page == "smart_matching":
        show_smart_matching()
    elif st.session_state.page == "reports":
        show_reports()
    elif st.session_state.page == "notifications":
        show_notifications()
    elif st.session_state.page == "worker_dashboard":
        show_worker_dashboard()

if __name__ == "__main__":
    main()
