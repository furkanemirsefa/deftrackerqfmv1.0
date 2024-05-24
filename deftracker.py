import pandas as pd
import streamlit as st

# Function to load the Excel file
@st.cache_data
def load_data(file):
    try:
        data = pd.read_excel(file)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Function to search the data
def search_data(entries, data):
    if 'Event ID' not in data.columns:
        st.error("The column 'Event ID' does not exist in the data.")
        return pd.DataFrame()  # Return an empty DataFrame if the column doesn't exist

    # Ensure 'id' is of string type for comparison
    data['Event ID'] = data['Event ID'].astype(str).str.strip()
    entries = [entry.strip() for entry in entries]

    results = data[data['Event ID'].isin(entries)]
    return results

# Streamlit app
st.title('Quick Look Application')

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=['xlsx'])

if uploaded_file:
    data = load_data(uploaded_file)
    if not data.empty:
        st.write("Data loaded successfully.")
        st.write("Columns in the dataset:", data.columns.tolist())

        st.write('Paste your entries below (one per line):')
        user_input = st.text_area('Entries', '')

        if st.button('Search'):
            if user_input.strip() == '':
                st.warning('Please enter at least one entry.')
            else:
                entries = user_input.split('\n')
                entries = [entry.strip() for entry in entries if entry.strip()]
                
                if not entries:
                    st.warning('Please enter valid entries.')
                else:
                    results = search_data(entries, data)
                    if results.empty:
                        st.info('No results found.')
                    else:
                        # Select only the specified columns to display
                        columns_to_display = ['Event ID', 'Site', 'Workflow Status', 'External Reference']
                        results = results[columns_to_display]
                        
                        st.write('Results:')
                        st.dataframe(results)

# Message when no file is uploaded
else:
    st.info('Please upload an Excel file to proceed.')
