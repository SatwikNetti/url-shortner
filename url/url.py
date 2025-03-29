import streamlit as st
import pyshorteners
import re

# Set up the title and description for the app
st.title("URL Shortener")
st.markdown("Enter a URL to shorten it. You can also see a history of previously shortened links.")

# Input for URL
url_input = st.text_input("Enter the URL you want to shorten:", "")

# Create a dictionary to store the shortened URLs
if 'history' not in st.session_state:
    st.session_state.history = []

# Function to validate URL format
def is_valid_url(url):
    # Simple regex to validate URL format
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

# Function to shorten the URL using Is.gd service
def shorten_url(url):
    try:
        if not is_valid_url(url):
            st.error("Invalid URL. Please enter a valid URL starting with 'http://' or 'https://'.")
            return None
        
        s = pyshorteners.Shortener()
        return s.isgd.short(url)
    
    except Exception as e:
        st.error(f"An error occurred while shortening the URL: {e}")
        return None

# Handle shortening process
if url_input:
    if st.button("Shorten URL"):
        shortened_url = shorten_url(url_input)
        if shortened_url:
            st.success(f"Shortened URL: {shortened_url}")
            # Save the URL in history
            st.session_state.history.append(shortened_url)

# Display previous shortened URLs
if st.session_state.history:
    st.subheader("Shortened URL History")
    for index, shortened in enumerate(st.session_state.history):
        st.write(f"{index + 1}. {shortened}")
