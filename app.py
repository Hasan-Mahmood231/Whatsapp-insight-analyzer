import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
# --- 1. PAGE CONFIGURATION ---
# Sets the tab title, icon, and expands the layout to use the full screen width
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. THEME & COLOR CSS ---
# We use custom CSS to ensure colors are safe (high contrast) and attractive
st.markdown("""
    <style>
    /* Background of the entire app (Light Grey/WhatsApp background style) */
    .stApp {
        background-color: #f7f9fb;
    }
    
    /* SIDEBAR: Dark Green theme for a professional look */
    [data-testid="stSidebar"] {
        background-color: #075E54 !important;
    }
    
    /* Force Sidebar text to be White so it is readable against Dark Green */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* THE HERO HEADER: Using a solid Dark Green background to prevent color overlap */
    .header-container {
        background-color: #075E54;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        border-bottom: 5px solid #25D366; /* Bright Green accent line */
    }
    
    /* Title Font: Large, bold, and White for maximum visibility */
    .header-title {
        color: #ffffff !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 55px !important;
        font-weight: 800;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Subtext under the title */
    .header-subtitle {
        color: #dcf8c6 !important;
        font-size: 18px;
        margin-top: 10px;
    }

    /* INFO CARD: A clean white box for the introduction text */
    .info-card {
        background-color: #ffffff !important; /* Force background to white */
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        
        /* Correct way to set font color in CSS */
        color: #000000 !important; 
        
        border-left: 8px solid #128C7E;
    }

    /* This ensures the heading inside the card is also black */
    .info-card h3 {
        color: #000000 !important;
        margin-top: 0;
    }

    /* This ensures any paragraph text inside the card is also black */
    .info-card p {
        color: black !important;
    }

    /* BUTTON STYLING: High-contrast Green button with hover effect */
    div.stButton > button {
        background-color: #25D366 !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 18px !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        border: none !important;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background-color: #128C7E !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR CONTENT ---
with st.sidebar:
    # Adding the official logo (or an icon)
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg", width=100)
    st.markdown("## Control Panel")
    st.write("Manage your analysis settings here.")
    
    st.markdown("---") # Divider line
    
    # File Uploader: The main input for the project
    uploaded_file = st.file_uploader("📤 Upload Chat Text File", type="txt")
    
    st.markdown("---")
    # Selection box for user to choose specific analysis
    # user_list = st.selectbox("Select User to Analyze", ["Overall", "User 1", "User 2"])
    
    st.info("💡 Make sure you exported the chat without media for a faster analysis.")

# --- 4. MAIN PAGE CONTENT ---

# The Styled Heading Block (Uses the CSS classes defined above)
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">WhatsApp Chat Analyzer</h1>
        <p class="header-subtitle">Deep Dive into Your Conversation Patterns</p>
    </div>
    """, unsafe_allow_html=True)

# Intro Description - Occupying the main center space
st.markdown("""
    <div class="info-card">
        <h3>👋 Welcome to the Analyzer!</h3>
        <p>This application takes your exported WhatsApp chat history and provides a visual 
        breakdown of your messaging habits. By uploading your file, you can unlock data regarding 
    </div>
    """, unsafe_allow_html=True)

st.write("") # Adding a small space

# --- 5. LOGIC & ACTION BUTTON ---
if uploaded_file is not None:
    # If a file is detected, show a success message
    st.success("✅ Chat file detected and ready for processing!")
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    st.dataframe(df)
    # The Action Button to trigger the backend (Analysis)
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Select user",user_list)
    #button of analysis.
    if st.sidebar.button("Show Analysis"):
        st.balloons() # Visual celebration effect
        num_messages , words,num_media, num_links = helper.fetch_stats(selected_user,df)

        # Placeholder for the data visualizations
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.markdown('<p style="color:#075E54; font-size:24px; font-weight:bold;">Total Messages</p>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="color:#25D366;">{num_messages}</h1>', unsafe_allow_html=True)
        with col2:
            st.markdown('<p style="color:#075E54; font-size:24px; font-weight:bold;">Total Words</p>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="color:#25D366;">{words}</h1>', unsafe_allow_html=True)
        with col3:
            st.markdown('<p style="color:#075E54; font-size:24px; font-weight:bold;">Media Shaird</p>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="color:#25D366;">{num_media}</h1>', unsafe_allow_html=True)
        with col4:
            st.markdown('<p style="color:#075E54; font-size:24px; font-weight:bold;">Number of Links</p>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="color:#25D366;">{num_links}</h1>', unsafe_allow_html=True)
        
        #finding most busy user in group chat only.
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x = helper.fetch_active_user(df)
            
            # Create the figure
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)

            with col1:
                # Check if x is a Series before calling .index or .values
                if isinstance(x, str):
                    st.error(x) # Shows the error message if x is a string
                else:
                    ax.bar(x.index, x.values, color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
        
else:
    # If no file is uploaded, show a helpful prompt
    pass
# --- FOOTER ---