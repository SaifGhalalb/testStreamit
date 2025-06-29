# Please ensure Streamlit is installed using:
# pip install streamlit

import streamlit as st
import pandas as pd

st.set_page_config(page_title='Umrah Travel Agency', layout='wide')

# Sidebar navigation
st.sidebar.title('Navigation')
menu = st.sidebar.radio('', [
    'Home', 'Packages', 'Book Package', 'My Bookings', 'User Profile', 'Admin Panel', 'Contact Support'
])

# Dummy data for packages
packages = pd.DataFrame({
    'Package Name': ['Economy Package', 'Deluxe Package', 'Premium Package'],
    'Price (USD)': [1200, 2000, 3500],
    'Hotel': ['Makkah Hotel 3-star', 'Makkah Hotel 4-star', 'Makkah Hotel 5-star'],
    'Duration (days)': [7, 10, 14],
    'Transport': ['Bus', 'Private Car', 'Luxury Car'],
    'Meals Included': ['Breakfast', 'Breakfast & Dinner', 'All meals']
})

if menu == 'Home':
    st.title('Umrah Travel Agency')
    st.image('https://example.com/banner.jpg', use_column_width=True)
    st.markdown("""
        Welcome to **Umrah Travel Agency**, your trusted partner for a comfortable and spiritually enriching Umrah journey.

        ### Explore our services:
        - Comprehensive travel packages
        - Hassle-free bookings
        - Dedicated customer support
    """)

elif menu == 'Packages':
    st.title('Available Umrah Packages')
    st.table(packages)

elif menu == 'Book Package':
    st.title('Book Your Umrah Package')

    col1, col2 = st.columns(2)

    with col1:
        package_selected = st.selectbox('Select Package', packages['Package Name'])
        traveler_name = st.text_input('Full Name')
        passport_number = st.text_input('Passport Number')
        nationality = st.text_input('Nationality')
        travel_date = st.date_input('Preferred Travel Date')

    with col2:
        email = st.text_input('Email')
        phone = st.text_input('Phone Number')
        uploaded_files = st.file_uploader('Upload Documents (Passport, Visa, Vaccination)', accept_multiple_files=True)
        payment_method = st.selectbox('Payment Method', ['Credit Card', 'Debit Card', 'Bank Transfer'])

    if st.button('Confirm Booking'):
        st.success(f'Booking confirmed for {traveler_name} ({package_selected}) on {travel_date}')

elif menu == 'My Bookings':
    st.title('My Bookings')
    st.info('Your bookings will be displayed here once connected to a database.')

elif menu == 'User Profile':
    st.title('User Profile')
    name = st.text_input('Name', 'John Doe')
    passport_num = st.text_input('Passport Number', 'A12345678')
    nationality = st.text_input('Nationality', 'Country')
    phone_number = st.text_input('Phone Number', '+1234567890')
    email_address = st.text_input('Email', 'john.doe@example.com')

    if st.button('Update Profile'):
        st.success('Profile updated successfully!')

elif menu == 'Admin Panel':
    st.title('Admin Panel')

    admin_menu = st.sidebar.selectbox('Admin Menu', ['Manage Packages', 'View Reports', 'User Management'])

    if admin_menu == 'Manage Packages':
        st.subheader('Package Management')
        st.write('Add, update, or remove packages here.')

    elif admin_menu == 'View Reports':
        st.subheader('Reports & Analytics')
        st.write('View booking reports, analytics, and user activities.')

    elif admin_menu == 'User Management':
        st.subheader('Manage Users')
        st.write('Create, update, or deactivate user accounts.')

elif menu == 'Contact Support':
    st.title('Contact Customer Support')
    issue = st.text_area('Describe Your Issue')
    contact_email = st.text_input('Your Email')
    if st.button('Submit Issue'):
        st.success('Issue submitted! Our support team will contact you shortly.')
