import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# Assume df is your DataFrame
df = pd.read_csv("Analysis_Ready_DS_jobs.csv")
import streamlit as st

# Google Analytics tracking
import streamlit as st
import streamlit.components.v1 as components
import streamlit as st
import streamlit.components.v1 as components

CLARITY_CODE = """
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "wi8hkmd1gs");
</script>
"""

components.html(CLARITY_CODE, height=0)




####
import streamlit as st
import firebase_admin
from firebase_admin import credentials

if not firebase_admin._apps:

    cred = credentials.Certificate(
        st.secrets["firebase"]["service_account"]
    )

    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://YOUR_PROJECT.firebaseio.com/"
    })




import streamlit as st
components.html("""
<div style="text-align:center;">

<script>
function changeText(){
    document.getElementById("text").innerHTML = "🔥 JavaScript is working!";
}
</script>
""", height=0)





# Set wide layout before anything else
st.set_page_config(
    page_title="Job Data Explorer",
    layout="wide"
)


import streamlit as st

st.set_page_config(page_title="Dragon Background", layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    position: relative;
    z-index: 2;
}

.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #ff512f);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.dragon {
    position: fixed;
    top: 10%;
    left: -300px;
    width: 250px;
    height: 250px;
    z-index: 1;
    animation: flyDragon 18s linear infinite;
    opacity: 0.85;
}

@keyframes flyDragon {
    0% { left: -300px; top: 15%; transform: scale(0.8) rotate(0deg); }
    100% { left: 110%; top: 15%; transform: scale(1) rotate(0deg); }
}

.fire {
    position: fixed;
    top: 22%;
    left: 150px;
    width: 80px;
    height: 20px;
    background: radial-gradient(circle, #ffcc00, #ff6600, transparent);
    border-radius: 50%;
    filter: blur(8px);
    animation: fireBlast 0.4s infinite alternate;
    z-index: 1;
}

/* REDUCED GLASS BOX SIZE */
.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding: 15px 25px; 
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    color: white;
    text-align: center;
    margin: 50px auto; 
    max-width: 350px; /* Adjust this number to make it even smaller/larger */
    border: 1px solid rgba(255,255,255,0.1);
}

h1 {
    font-size: 1.5rem;
    color: #fff;
    text-shadow: 0 0 15px #ff6600;
}
</style>

""", unsafe_allow_html=True)





import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Job Research Dashboard", layout="wide")

# ---------------- LOAD DATA ----------------

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stButton>button {
    background-color:#1f77b4;
    color:white;
    border-radius:8px;
    padding:8px 18px;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Job Market Research Dashboard")

# ---------------- SIDEBAR FILTERS ----------------
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# ---------------- LOAD DATA ----------------


# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 Filter Dashboard")

country = st.sidebar.multiselect(
    "Select Country",
    df["Location Country"].dropna().unique()
)

category = st.sidebar.multiselect(
    "Select Job Category",
    df["Job Category"].dropna().unique()
)

remote = st.sidebar.multiselect(
    "Remote Type",
    df["Is Remote"].dropna().unique()
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df.copy()

if country:
    filtered_df = filtered_df[filtered_df["Location Country"].isin(country)]

if category:
    filtered_df = filtered_df[filtered_df["Job Category"].isin(category)]

if remote:
    filtered_df = filtered_df[filtered_df["Is Remote"].isin(remote)]

# ---------------- TOGGLE FUNCTION ----------------
def toggle_chart(key):
    if key not in st.session_state:
        st.session_state[key] = False
    st.session_state[key] = not st.session_state[key]

# ---------------- CHART 1 ----------------
st.subheader("1. Which Job Titles Have the Highest Average Salary?")

if st.button("Show Chart 1"):
    toggle_chart("chart1")

if st.session_state.get("chart1", False):
    fig, ax = plt.subplots(figsize=(10,5))
    
    top = filtered_df.groupby("Job Title")["Avg Salary (K)"]\
        .mean()\
        .sort_values(ascending=False)\
        .head(10)

    sns.barplot(x=top.values, y=top.index, ax=ax)
    ax.set_title("Top Paying Job Titles")
    st.pyplot(fig)

# ---------------- CHART 2 ----------------
st.subheader("2. Which Countries Offer Highest Salary?")

if st.button("Show Chart 2"):
    toggle_chart("chart2")

if st.session_state.get("chart2", False):
    fig, ax = plt.subplots(figsize=(10,5))

    top = filtered_df.groupby("Location Country")["Avg Salary (K)"]\
        .mean()\
        .sort_values(ascending=False)\
        .head(10)

    sns.barplot(x=top.values, y=top.index, ax=ax)
    ax.set_title("Highest Salary by Country")
    st.pyplot(fig)


# Continue from your current code and add CHART 3 to CHART 20 below

# ---------------- CHART 3 ----------------
st.subheader("3. Which Job Categories Pay the Most?")
if st.button("Show Chart 3"):
    toggle_chart("chart3")

if st.session_state.get("chart3", False):
    fig, ax = plt.subplots(figsize=(10,5))
    top = filtered_df.groupby("Job Category")["Avg Salary (K)"].mean().sort_values(ascending=False).head(10)
    sns.barplot(x=top.values, y=top.index, ax=ax)
    ax.set_title("Highest Paying Job Categories")
    st.pyplot(fig)

# ---------------- CHART 4 ----------------
st.subheader("4. Does Seniority Affect Salary?")
if st.button("Show Chart 4"):
    toggle_chart("chart4")

if st.session_state.get("chart4", False):
    fig, ax = plt.subplots(figsize=(10,5))
    sns.boxplot(data=filtered_df, x="Job Seniority", y="Avg Salary (K)", ax=ax)
    plt.xticks(rotation=45)
    ax.set_title("Salary by Seniority")
    st.pyplot(fig)

# ---------------- CHART 5 ----------------
st.subheader("5. Remote vs Non-Remote Salary Comparison")
if st.button("Show Chart 5"):
    toggle_chart("chart5")

if st.session_state.get("chart5", False):
    fig, ax = plt.subplots(figsize=(8,5))
    sns.boxplot(data=filtered_df, x="Is Remote", y="Avg Salary (K)", ax=ax)
    ax.set_title("Remote vs Non-Remote Salary")
    st.pyplot(fig)

# ---------------- CHART 6 ----------------
st.subheader("6. Top Hiring Cities")
if st.button("Show Chart 6"):
    toggle_chart("chart6")

if st.session_state.get("chart6", False):
    fig, ax = plt.subplots(figsize=(10,5))
    top = filtered_df["Location City"].value_counts().head(10)
    sns.barplot(x=top.values, y=top.index, ax=ax)
    ax.set_title("Top Hiring Cities")
    st.pyplot(fig)

# ---------------- CHART 7 ----------------
st.subheader("7. Does Company Rating Relate to Salary?")
if st.button("Show Chart 7"):
    toggle_chart("chart7")

if st.session_state.get("chart7", False):
    fig, ax = plt.subplots(figsize=(8,5))
    sns.scatterplot(data=filtered_df, x="Rating", y="Avg Salary (K)", ax=ax)
    ax.set_title("Rating vs Salary")
    st.pyplot(fig)

# ---------------- CHART 8 ----------------
st.subheader("8. Company Size Distribution")
if st.button("Show Chart 8"):
    toggle_chart("chart8")

if st.session_state.get("chart8", False):
    fig, ax = plt.subplots(figsize=(10,5))
    filtered_df["Size"].value_counts().plot(kind="bar", ax=ax)
    ax.set_title("Company Size Distribution")
    st.pyplot(fig)

# ---------------- CHART 9 ----------------
st.subheader("9. Industries With Most Job Openings")
if st.button("Show Chart 9"):
    toggle_chart("chart9")

if st.session_state.get("chart9", False):
    fig, ax = plt.subplots(figsize=(10,5))
    top = filtered_df["Industry"].value_counts().head(10)
    sns.barplot(x=top.values, y=top.index, ax=ax)
    ax.set_title("Top Industries Hiring")
    st.pyplot(fig)

# ---------------- CHART 10 ----------------
st.subheader("10. Sector vs Average Salary")
if st.button("Show Chart 10"):
    toggle_chart("chart10")

if st.session_state.get("chart10", False):
    fig, ax = plt.subplots(figsize=(10,5))
    top = filtered_df.groupby("Sector")["Avg Salary (K)"].mean().sort_values(ascending=False).head(10)
    sns.barplot(x=top.values, y=top.index, ax=ax)
    ax.set_title("Average Salary by Sector")
    st.pyplot(fig)

# ---------------- CHART 11 ----------------
st.subheader("11. Revenue Band Distribution")
if st.button("Show Chart 11"):
    toggle_chart("chart11")

if st.session_state.get("chart11", False):
    fig, ax = plt.subplots(figsize=(10,5))
    filtered_df["Revenue Band"].value_counts().plot(kind="bar", ax=ax)
    ax.set_title("Revenue Band Distribution")
    st.pyplot(fig)

# ---------------- CHART 12 ----------------
st.subheader("12. Older Companies Pay More?")
if st.button("Show Chart 12"):
    toggle_chart("chart12")

if st.session_state.get("chart12", False):
    fig, ax = plt.subplots(figsize=(8,5))
    sns.scatterplot(data=filtered_df, x="Company Age", y="Avg Salary (K)", ax=ax)
    ax.set_title("Company Age vs Salary")
    st.pyplot(fig)

# ---------------- CHART 13 ----------------
st.subheader("13. Founded Year Distribution")
if st.button("Show Chart 13"):
    toggle_chart("chart13")

if st.session_state.get("chart13", False):
    fig, ax = plt.subplots(figsize=(10,5))
    sns.histplot(filtered_df["Founded"].dropna(), bins=20, ax=ax)
    ax.set_title("Founded Year Distribution")
    st.pyplot(fig)

# ---------------- CHART 14 ----------------
st.subheader("14. Ownership Type Distribution")
if st.button("Show Chart 14"):
    toggle_chart("chart14")

if st.session_state.get("chart14", False):
    fig, ax = plt.subplots(figsize=(10,5))
    filtered_df["Type of ownership"].value_counts().head(10).plot(kind="bar", ax=ax)
    ax.set_title("Ownership Types")
    st.pyplot(fig)

# ---------------- CHART 15 ----------------
st.subheader("15. Min Salary vs Max Salary")
if st.button("Show Chart 15"):
    toggle_chart("chart15")

if st.session_state.get("chart15", False):
    fig, ax = plt.subplots(figsize=(8,5))
    sns.scatterplot(data=filtered_df, x="Min Salary (K)", y="Max Salary (K)", ax=ax)
    ax.set_title("Min vs Max Salary")
    st.pyplot(fig)

# ---------------- CHART 16 ----------------
st.subheader("16. Salary Distribution")
if st.button("Show Chart 16"):
    toggle_chart("chart16")

if st.session_state.get("chart16", False):
    fig, ax = plt.subplots(figsize=(10,5))
    sns.histplot(filtered_df["Avg Salary (K)"], bins=30, kde=True, ax=ax)
    ax.set_title("Salary Distribution")
    st.pyplot(fig)

# ---------------- CHART 17 ----------------
st.subheader("17. Top Rated Companies")
if st.button("Show Chart 17"):
    toggle_chart("chart17")

if st.session_state.get("chart17", False):
    fig, ax = plt.subplots(figsize=(10,5))
    top = filtered_df.groupby("Company Name")["Rating"].mean().sort_values(ascending=False).head(10)
    sns.barplot(x=top.values, y=top.index, ax=ax)
    ax.set_title("Top Rated Companies")
    st.pyplot(fig)

# ---------------- CHART 18 ----------------
st.subheader("18. Competitor Count by Industry")
if st.button("Show Chart 18"):
    toggle_chart("chart18")

if st.session_state.get("chart18", False):
    fig, ax = plt.subplots(figsize=(10,5))
    top = filtered_df.groupby("Industry")["Competitor Count"].mean().sort_values(ascending=False).head(10)
    sns.barplot(x=top.values, y=top.index, ax=ax)
    ax.set_title("Competitor Count by Industry")
    st.pyplot(fig)

# ---------------- CHART 19 ----------------
st.subheader("19. Jobs Available by Seniority")
if st.button("Show Chart 19"):
    toggle_chart("chart19")

if st.session_state.get("chart19", False):
    fig, ax = plt.subplots(figsize=(10,5))
    filtered_df["Job Seniority"].value_counts().plot(kind="bar", ax=ax)
    ax.set_title("Jobs by Seniority")
    st.pyplot(fig)

# ---------------- CHART 20 ----------------
st.subheader("20. Correlation Between Numeric Variables")
if st.button("Show Chart 20"):
    toggle_chart("chart20")

if st.session_state.get("chart20", False):
    fig, ax = plt.subplots(figsize=(12,8))
    num = filtered_df.select_dtypes(include="number")
    sns.heatmap(num.corr(), annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)



#####
import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time
import re

st.markdown("---")
st.header("📩 Send Feedback")

# Session state
if "name" not in st.session_state:
    st.session_state.name = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "message" not in st.session_state:
    st.session_state.message = ""

# Email validation function
import re

def is_valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@(gmail\.com|yahoo\.com)$"
    return re.match(pattern, email, re.IGNORECASE) is not None

with st.form("feedback_form", clear_on_submit=True):
    name = st.text_input("Your Name", key="name")
    email = st.text_input("Your Email", key="email")
    message = st.text_area("Your Message", key="message")

    submit = st.form_submit_button("Send Feedback")

if submit:
    if name and email and message:
        if not is_valid_email(email):
            st.warning("⚠️ Please enter a valid email address (example: name@gmail.com)")
        else:
            try:
                sender_email = "opethesaint@gmail.com"
                receiver_email = "opethesaint@gmail.com"
                app_password = "lofevlbskhzcvfde"

                subject = f"New Feedback from {name}"
                body = f"""
You have received new feedback:

Name: {name}
Email: {email}

Message:
{message}
"""

                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = sender_email
                msg["To"] = receiver_email

                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, app_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                server.quit()

                success_box = st.empty()
                success_box.success("✅ Feedback sent successfully!")
                time.sleep(3)
                success_box.empty()

            except Exception as e:
                st.error(f"❌ Failed to send feedback: {e}")
    else:
        st.warning("⚠️ Please fill all fields.")





import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Job Data Explorer", layout="wide")

# ---------------- DRAGON SIDEBAR BACKGROUND ----------------
st.markdown("""
<style>

/* Sidebar container */
[data-testid="stSidebar"]{
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #ff512f);
    background-size: 400% 400%;
    animation: dragonBG 12s ease infinite;
    position: relative;
    overflow: hidden;
}

/* Animated gradient */
@keyframes dragonBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Flying dragon emoji */
[data-testid="stSidebar"]::before{
    content: "🐉";
    position: absolute;
    top: 25px;
    left: 25px;
    font-size: 90px;
    opacity: 0.95;
    animation: flyDragon 7s ease-in-out infinite;
}

/* Fire effect */
[data-testid="stSidebar"]::after{
    content: "🔥";
    position: absolute;
    top: 90px;
    left: 110px;
    font-size: 32px;
    animation: fireBlast 0.5s infinite alternate;
}

/* Dragon movement */
@keyframes flyDragon{
    0%   {transform: translate(0px,0px) rotate(0deg);}
    25%  {transform: translate(15px,-10px) rotate(5deg);}
    50%  {transform: translate(0px,5px) rotate(0deg);}
    75%  {transform: translate(-15px,-10px) rotate(-5deg);}
    100% {transform: translate(0px,0px) rotate(0deg);}
}

/* Fire pulse */
@keyframes fireBlast{
    from {transform: scale(1); opacity: 0.7;}
    to   {transform: scale(1.3); opacity: 1;}
}

/* Sidebar text */
[data-testid="stSidebar"] *{
    color: white !important;
}

/* Selectbox styling */
[data-baseweb="select"] > div{
    background: rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

/* Sidebar spacing */
[data-testid="stSidebar"] .block-container{
    padding-top: 7rem;
}

</style>
""", unsafe_allow_html=True)





with st.sidebar:
    st.info("🌤️ Lagos: 28°C")





with st.sidebar:
    st.markdown("💡 *Success is built one query at a time.*")



import streamlit as st

st.markdown("""
    <style>
    /* The container and the button */
    .whatsapp-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
    }
    
    .whatsapp-button {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 60px;
        background-color: #25D366;
        color: white;
        border-radius: 50%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        text-decoration: none;
        transition: all 0.3s ease;
        font-size: 30px;
    }

    /* Hover effect to make it feel "Live" */
    .whatsapp-button:hover {
        background-color: #128C7E;
        transform: scale(1.1);
        box-shadow: 0 6px 16px rgba(0,0,0,0.3);
        color: white;
    }

    /* Optional: Tooltip that appears near the button */
    .whatsapp-container::after {
        content: "Chat with us!";
        position: absolute;
        right: 70px;
        top: 15px;
        background: white;
        color: #444;
        padding: 5px 12px;
        border-radius: 10px;
        font-size: 14px;
        font-weight: 500;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        white-space: nowrap;
        opacity: 0;
        transition: opacity 0.3s;
        pointer-events: none;
    }

    .whatsapp-container:hover::after {
        opacity: 1;
    }
    </style>

    <div class="whatsapp-container">
        <a href="https://wa.me/2349036633374?text=%E2%80%8E%20Hello%20Data%20Analyst%20" class="whatsapp-button" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" viewBox="0 0 16 16">
              <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>
            </svg>
        </a>
    </div>
""", unsafe_allow_html=True)




import streamlit as st
import streamlit.components.v1 as components

# ===============================
# SOCIAL MEDIA FOOTER
# ===============================
social_footer = """
<div style="
    text-align:center;
    padding:20px;
    margin-top:40px;
    border-top:1px solid #ddd;
">
    <a href="https://x.com/Opethesaint" target="_blank" style="margin:15px;">
        <img src="https://cdn-icons-png.flaticon.com/512/5968/5968830.png" width="40">
    </a>
    <a href="https://facebook.com/Ogundiperilwanrotimi" target="_blank" style="margin:15px;">
        <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" width="40">
    </a>

    <a href="https://instagram.com/opethesaint/" target="_blank" style="margin:15px;">
        <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" width="40">
    </a>

 
</div>
"""

components.html(social_footer, height=100)

