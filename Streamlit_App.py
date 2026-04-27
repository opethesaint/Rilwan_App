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
import json
import os
import hashlib
from datetime import datetime

st.set_page_config(page_title="Ayobami App", layout="wide")

USER_FILE = "users.json"

# ---------------------------
# FUNCTIONS
# ---------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password(password):
    # Updated rules:
    # - At least 6 characters
    # - Starts with capital letter
    # - Number no longer required

    if len(password) < 6:
        return False, "Password must be at least 6 characters"

    if not password[0].isupper():
        return False, "Password must start with a capital letter"

    return True, "OK"


def password_strength(password):
    score = 0

    if len(password) >= 6:
        score += 1
    if len(password) >= 10:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(not c.isalnum() for c in password):
        score += 1

    if score <= 2:
        return "Weak", 0.33
    elif score <= 4:
        return "Medium", 0.66
    else:
        return "Strong", 1.0


def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


# ---------------------------
# SESSION
# ---------------------------
if "users" not in st.session_state:
    st.session_state.users = load_users()

if "username" not in st.session_state:
    st.session_state.username = None


# ---------------------------
# AUTH PAGE
# ---------------------------
if st.session_state.username is None:

    st.title("🔐 Ayobami Authentication System")

    page = st.radio(
        "Choose option",
        ["Login", "Create Account", "Forgot Password"],
        horizontal=True
    )

    # ---------------------------
    # LOGIN
    # ---------------------------
    if page == "Login":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):

            if u == "admin" and p == "admin123":
                st.session_state.username = "admin"
                st.rerun()

            elif (
                u in st.session_state.users and
                st.session_state.users[u]["password"] == hash_password(p)
            ):
                st.session_state.username = u
                st.rerun()

            else:
                st.error("Invalid login")

    # ---------------------------
    # CREATE ACCOUNT
    # ---------------------------
    elif page == "Create Account":

        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        question = st.selectbox(
            "Recovery Question",
            [
                "What is your favorite food?",
                "What is your mother's first name?",
                "What city were you born in?",
                "What is your best friend's name?",
                "What is your favorite color?"
            ]
        )

        answer = st.text_input("Recovery Answer")

        if p:
            level, bar = password_strength(p)
            st.write(f"Password Strength: **{level}**")
            st.progress(bar)

        st.info("Password rules: Start with capital letter, minimum 6 characters.")

        if st.button("Create Account", use_container_width=True):

            if u and p and answer:

                valid, msg = validate_password(p)

                if not valid:
                    st.error(msg)

                elif u in st.session_state.users:
                    st.error("Username already exists")

                else:
                    st.session_state.users[u] = {
                        "password": hash_password(p),
                        "plain_password": p,
                        "recovery_question": question,
                        "recovery_answer": answer.lower().strip(),
                        "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    save_users(st.session_state.users)
                    st.success("Account created successfully!")

            else:
                st.warning("Please fill all fields")

    # ---------------------------
    # FORGOT PASSWORD
    # ---------------------------
    elif page == "Forgot Password":

        u = st.text_input("Username")

        if u in st.session_state.users:

            saved_question = st.session_state.users[u].get(
                "recovery_question",
                "No recovery question set"
            )

            st.info(f"Recovery Question: {saved_question}")

            answer = st.text_input("Recovery Answer")
            new_pass = st.text_input("New Password", type="password")

            if new_pass:
                level, bar = password_strength(new_pass)
                st.write(f"New Password Strength: **{level}**")
                st.progress(bar)

            if st.button("Reset Password", use_container_width=True):

                saved_answer = st.session_state.users[u].get(
                    "recovery_answer", ""
                )

                if answer.lower().strip() == saved_answer:

                    valid, msg = validate_password(new_pass)

                    if not valid:
                        st.error(msg)

                    else:
                        st.session_state.users[u]["password"] = hash_password(new_pass)
                        st.session_state.users[u]["plain_password"] = new_pass
                        save_users(st.session_state.users)
                        st.success("Password reset successful!")

                else:
                    st.error("Wrong recovery answer")

        else:
            if u:
                st.warning("Username not found")

    st.stop()


# ---------------------------
# HEADER
# ---------------------------
col1, col2 = st.columns([8, 1])

with col1:
    st.title("Welcome 🎉")

with col2:
    if st.button("Logout"):
        st.session_state.username = None
        st.rerun()

st.success(f"Logged in as: {st.session_state.username}")


# ---------------------------
# ADMIN DASHBOARD
# ---------------------------
if st.session_state.username == "admin":

    st.markdown("---")
    st.header("🛠 Admin Dashboard")

    users = st.session_state.users
    st.metric("Total Users", len(users))

    if users:
        rows = []

        for username, data in users.items():
            rows.append({
                "Username": username,
                "Real Password": data.get("plain_password", ""),
                "Recovery Question": data.get("recovery_question", ""),
                "Registered At": data.get("registered_at", "")
            })

        st.dataframe(rows, use_container_width=True)

        st.subheader("🗑 Delete User")

        user_to_delete = st.selectbox("Select user", list(users.keys()))

        if st.button("Delete User", use_container_width=True):
            del st.session_state.users[user_to_delete]
            save_users(st.session_state.users)
            st.success(f"{user_to_delete} deleted successfully")
            st.rerun()

    else:
        st.warning("No users registered yet.")

# ---------------------------
# USER DASHBOARD
# ---------------------------
else:
    st.markdown("---")
  
   























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

##########
#########
# ═══════════════════════════════════════════════════════════════
# PASTE THIS ENTIRE BLOCK INTO YOUR EXISTING app.py
# Place it AFTER your login code (where users are already authenticated)
# ═══════════════════════════════════════════════════════════════

import json
import time
import base64
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

# ===============================================================
# CONFIGURATION
# ===============================================================
CHAT_DATA_DIR = Path("chat_backend")
CHAT_DATA_DIR.mkdir(exist_ok=True)

CHAT_FILE = CHAT_DATA_DIR / "messages.json"
CHAT_USERS_FILE = CHAT_DATA_DIR / "users.json"
CHAT_TYPING_FILE = CHAT_DATA_DIR / "typing.json"
CHAT_READ_RECEIPTS_FILE = CHAT_DATA_DIR / "read_receipts.json"
CHAT_REACTIONS_FILE = CHAT_DATA_DIR / "reactions.json"
CHAT_FILES_DIR = CHAT_DATA_DIR / "shared_files"
CHAT_FILES_DIR.mkdir(exist_ok=True)

CHAT_MAX_FILE_MB = 10
CHAT_HISTORY_DAYS = 30
CHAT_REFRESH = 2

CHAT_EMOJIS = ["👍", "❤️", "😂", "😮", "😢", "🔥", "👏", "🎉", "🤔", "👎", "🙏", "💯"]

# ===============================================================
# JSON HELPERS
# ===============================================================

def _chat_load_json(filepath, default=None):
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default if default is not None else {}

def _chat_save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)

# ===============================================================
# USER STATUS
# ===============================================================

def _chat_update_status(username, status="online"):
    users = _chat_load_json(CHAT_USERS_FILE, {})
    users[username] = {
        "status": status,
        "last_seen": datetime.now().isoformat(),
        "joined_at": users.get(username, {}).get("joined_at", datetime.now().isoformat())
    }
    _chat_save_json(CHAT_USERS_FILE, users)

def _chat_get_online(exclude=None):
    users = _chat_load_json(CHAT_USERS_FILE, {})
    now = datetime.now()
    online = {}
    for user, info in users.items():
        if user == exclude:
            continue
        last_seen = datetime.fromisoformat(info["last_seen"])
        if (now - last_seen).seconds <= 30 and info["status"] == "online":
            online[user] = info
    return online

# ===============================================================
# MESSAGES
# ===============================================================

def _chat_load_messages():
    return _chat_load_json(CHAT_FILE, {"messages": [], "last_cleanup": datetime.now().isoformat()})

def _chat_save_messages(data):
    _chat_save_json(CHAT_FILE, data)

def _chat_add_msg(from_user, to_user, text, msg_type="text", file_data=None):
    data = _chat_load_messages()
    msg = {
        "id": hashlib.md5(f"{from_user}{to_user}{datetime.now().isoformat()}".encode()).hexdigest()[:12],
        "from": from_user,
        "to": to_user,
        "text": text,
        "type": msg_type,
        "file_data": file_data,
        "time": datetime.now().strftime("%H:%M"),
        "timestamp": datetime.now().isoformat(),
        "chat_type": "global" if to_user == "global" else "private",
        "edited": False,
        "edited_at": None,
        "deleted": False
    }
    data["messages"].append(msg)
    _chat_save_messages(data)
    return msg["id"]

def _chat_edit_msg(msg_id, new_text):
    data = _chat_load_messages()
    for msg in data["messages"]:
        if msg["id"] == msg_id:
            msg["text"] = new_text
            msg["edited"] = True
            msg["edited_at"] = datetime.now().isoformat()
            _chat_save_messages(data)
            return True
    return False

def _chat_delete_msg(msg_id):
    data = _chat_load_messages()
    for msg in data["messages"]:
        if msg["id"] == msg_id:
            msg["deleted"] = True
            msg["text"] = "This message was deleted"
            _chat_save_messages(data)
            return True
    return False

def _chat_get_msgs(username, chat_with):
    data = _chat_load_messages()
    messages = data.get("messages", [])
    if chat_with == "global":
        return [m for m in messages if m.get("chat_type") == "global"]
    return [
        m for m in messages
        if m.get("chat_type") == "private"
        and ((m["from"] == username and m["to"] == chat_with) or
             (m["from"] == chat_with and m["to"] == username))
    ]

# ===============================================================
# READ RECEIPTS
# ===============================================================

def _chat_mark_read(username, chat_with):
    receipts = _chat_load_json(CHAT_READ_RECEIPTS_FILE, {})
    messages = _chat_get_msgs(username, chat_with)
    for msg in messages:
        if msg["from"] != username:
            mid = msg["id"]
            if mid not in receipts:
                receipts[mid] = {}
            receipts[mid][username] = datetime.now().isoformat()
    _chat_save_json(CHAT_READ_RECEIPTS_FILE, receipts)

def _chat_read_status(msg_id):
    return _chat_load_json(CHAT_READ_RECEIPTS_FILE, {}).get(msg_id, {})

# ===============================================================
# REACTIONS
# ===============================================================

def _chat_add_reaction(msg_id, username, emoji):
    reactions = _chat_load_json(CHAT_REACTIONS_FILE, {})
    if msg_id not in reactions:
        reactions[msg_id] = {}
    user_reactions = reactions[msg_id].get(username, [])
    if emoji in user_reactions:
        user_reactions.remove(emoji)
    else:
        user_reactions.append(emoji)
    reactions[msg_id][username] = user_reactions
    _chat_save_json(CHAT_REACTIONS_FILE, reactions)

def _chat_get_reactions(msg_id):
    reactions = _chat_load_json(CHAT_REACTIONS_FILE, {}).get(msg_id, {})
    counts = {}
    for user, emojis in reactions.items():
        for e in emojis:
            counts.setdefault(e, []).append(user)
    return counts

# ===============================================================
# TYPING
# ===============================================================

def _chat_set_typing(username, chat_with, is_typing=True):
    data = _chat_load_json(CHAT_TYPING_FILE, {})
    key = f"{username}:{chat_with}"
    if is_typing:
        data[key] = {"since": datetime.now().isoformat(), "to": chat_with}
    else:
        data.pop(key, None)
    _chat_save_json(CHAT_TYPING_FILE, data)

def _chat_get_typing(chat_with, exclude):
    data = _chat_load_json(CHAT_TYPING_FILE, {})
    now = datetime.now()
    users = []
    for key, info in data.items():
        parts = key.split(":", 1)
        if len(parts) != 2:
            continue
        user, to = parts
        if user == exclude:
            continue
        if to == chat_with or (chat_with == "global" and to == "global"):
            if (now - datetime.fromisoformat(info["since"])).seconds <= 5:
                users.append(user)
    return users

# ===============================================================
# FILES
# ===============================================================

def _chat_save_file(uploaded_file, username):
    if not uploaded_file:
        return None
    size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    if size_mb > CHAT_MAX_FILE_MB:
        st.error(f"File too large! Max {CHAT_MAX_FILE_MB}MB")
        return None
    ext = Path(uploaded_file.name).suffix
    unique = f"{hashlib.md5(f'{username}{datetime.now().isoformat()}'.encode()).hexdigest()[:16]}{ext}"
    path = CHAT_FILES_DIR / unique
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return {
        "original_name": uploaded_file.name,
        "saved_name": unique,
        "size_mb": round(size_mb, 2),
        "type": uploaded_file.type
    }

def _chat_file_link(file_data):
    if not file_data:
        return None
    path = CHAT_FILES_DIR / file_data["saved_name"]
    if not path.exists():
        return None
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    mime = file_data.get("type", "application/octet-stream")
    return f"data:{mime};base64,{b64}"

# ===============================================================
# CLEANUP
# ===============================================================

def _chat_cleanup(force=False):
    data = _chat_load_messages()
    last = datetime.fromisoformat(data.get("last_cleanup", datetime.now().isoformat()))
    now = datetime.now()
    if not force and (now - last).days < 1:
        return 0
    cutoff = now - timedelta(days=CHAT_HISTORY_DAYS)
    msgs = data.get("messages", [])
    kept = [m for m in msgs if datetime.fromisoformat(m["timestamp"]) > cutoff]
    deleted = len(msgs) - len(kept)
    data["messages"] = kept
    data["last_cleanup"] = now.isoformat()
    _chat_save_messages(data)
    # cleanup files
    for fp in CHAT_FILES_DIR.iterdir():
        if fp.is_file() and datetime.fromtimestamp(fp.stat().st_mtime) < cutoff:
            fp.unlink()
    return deleted

# ===============================================================
# SESSION STATE INIT (safe to call multiple times)
# ===============================================================

if "chat_current" not in st.session_state:
    st.session_state.chat_current = "global"
if "chat_editing" not in st.session_state:
    st.session_state.chat_editing = None
if "chat_reacting" not in st.session_state:
    st.session_state.chat_reacting = None

# ===============================================================
# POPUP CHAT DIALOG
# ===============================================================

@st.dialog("💬 Chat", width="large")
def open_chat_popup():
    """Call this function to open the chat popup"""

    # Use your logged-in username here
    # Replace st.session_state.username with however you store the current user
    username = st.session_state.get("username") or st.session_state.get("user") or "User"

    _chat_update_status(username, "online")
    chat_with = st.session_state.chat_current
    is_global = chat_with == "global"

    _chat_mark_read(username, chat_with)

    # Header
    hc1, hc2 = st.columns([3, 1])
    with hc1:
        if is_global:
            st.subheader("🌍 Global Chat")
        else:
            online = _chat_get_online(exclude=username)
            status = "🟢 Online" if chat_with in online else "⚪ Offline"
            st.subheader(f"{chat_with}")
            st.caption(status)

    with hc2:
        all_u = _chat_load_json(CHAT_USERS_FILE, {})
        others = [u for u in all_u.keys() if u != username]
        options = ["Global Chat"] + sorted(others)
        current_idx = options.index(chat_with) if chat_with in options else 0
        new_chat = st.selectbox("Switch", options, index=current_idx, key="chat_switch", label_visibility="collapsed")
        if new_chat == "Global Chat":
            new_chat = "global"
        if new_chat != chat_with:
            st.session_state.chat_current = new_chat
            st.rerun()

    st.divider()

    # Typing
    typing = _chat_get_typing(chat_with, username)
    if typing:
        verb = "is" if len(typing) == 1 else "are"
        st.markdown(f"<small style='color:#888;'>✏️ {', '.join(typing)} {verb} typing...</small>", unsafe_allow_html=True)

    # Messages
    messages = _chat_get_msgs(username, chat_with)

    container = st.container(height=350)
    with container:
        if not messages:
            st.info("No messages yet. Say hello! 👋")
        else:
            for msg in messages:
                is_me = msg["from"] == username
                is_deleted = msg.get("deleted", False)

                # Build message HTML
                edited = ""
                if msg.get("edited") and not is_deleted:
                    edited = " <small style='opacity:0.6;'>(edited)</small>"

                attachment = ""
                if msg.get("file_data") and not is_deleted:
                    fd = msg["file_data"]
                    link = _chat_file_link(fd)
                    if msg["type"] == "image" and link:
                        attachment = f'<br><img src="{link}" style="border-radius:8px;max-width:200px;margin-top:4px;" />'
                    elif link:
                        color = "white" if is_me else "#333"
                        attachment = f'<br><div style="background:rgba(255,255,255,0.2);border-radius:6px;padding:4px 8px;margin-top:4px;font-size:0.85rem;">📎 <a href="{link}" download="{fd["original_name"]}" style="color:{color};text-decoration:underline;">{fd["original_name"]} ({fd["size_mb"]} MB)</a></div>'

                reactions = ""
                if not is_deleted:
                    r = _chat_get_reactions(msg["id"])
                    if r:
                        badges = [f'<span style="background:rgba(0,0,0,0.08);border-radius:10px;padding:1px 6px;font-size:0.75rem;" title="{", ".join(users)}">{emoji} {len(users)}</span>' for emoji, users in r.items()]
                        align = "flex-end" if is_me else "flex-start"
                        reactions = f'<div style="display:flex;gap:4px;flex-wrap:wrap;justify-content:{align};margin-top:4px;">{"".join(badges)}</div>'

                read = ""
                if is_me and not is_deleted:
                    by = _chat_read_status(msg["id"])
                    if chat_with == "global":
                        cnt = len([u for u in by if u != username])
                        read = f'<div style="font-size:0.65rem;color:#90EE90;margin-top:2px;">✓✓ Read by {cnt}</div>' if cnt > 0 else '<div style="font-size:0.65rem;color:#ccc;margin-top:2px;">✓ Sent</div>'
                    else:
                        read = '<div style="font-size:0.65rem;color:#90EE50;margin-top:2px;">✓✓ Read</div>' if chat_with in by else '<div style="font-size:0.65rem;color:#ccc;margin-top:2px;">✓ Sent</div>'

                bg = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" if is_me else "#f0f2f6"
                color = "white" if is_me else "#333"
                align = "margin-left:auto;text-align:right;" if is_me else "margin-right:auto;text-align:left;"
                opacity = "opacity:0.6;font-style:italic;" if is_deleted else ""

                st.markdown(f"""
                <div style="background:{bg};color:{color};padding:0.7rem 1rem;border-radius:1rem;margin:0.4rem 0;max-width:78%;word-wrap:break-word;{align}{opacity}">
                    <small><b>{msg["from"]}</b> · {msg["time"]}</small><br>
                    {msg["text"]}{edited}
                    {attachment}
                    {reactions}
                    {read}
                </div>
                <div style="clear:both;"></div>
                """, unsafe_allow_html=True)

                # Action buttons
                if not is_deleted:
                    ac1, ac2, ac3, ac4 = st.columns([1, 1, 1, 10])
                    with ac1:
                        if st.button("😊", key=f"r_{msg['id']}", help="React"):
                            st.session_state.chat_reacting = msg["id"] if st.session_state.chat_reacting != msg["id"] else None
                            st.rerun()
                    if is_me:
                        with ac2:
                            if st.button("✏️", key=f"e_{msg['id']}", help="Edit"):
                                st.session_state.chat_editing = msg["id"]
                                st.rerun()
                        with ac3:
                            if st.button("🗑️", key=f"d_{msg['id']}", help="Delete"):
                                _chat_delete_msg(msg["id"])
                                st.rerun()

                # Emoji picker
                if st.session_state.chat_reacting == msg["id"]:
                    emojis = st.columns(len(CHAT_EMOJIS))
                    for i, emoji in enumerate(CHAT_EMOJIS):
                        with emojis[i]:
                            if st.button(emoji, key=f"em_{msg['id']}_{emoji}"):
                                _chat_add_reaction(msg["id"], username, emoji)
                                st.session_state.chat_reacting = None
                                st.rerun()

                # Edit form
                if st.session_state.chat_editing == msg["id"] and is_me:
                    with st.container(border=True):
                        nt = st.text_input("Edit", value=msg["text"], key=f"ei_{msg['id']}", label_visibility="collapsed")
                        ec1, ec2 = st.columns([1, 1])
                        with ec1:
                            if st.button("Save", key=f"es_{msg['id']}", type="primary"):
                                if nt.strip():
                                    _chat_edit_msg(msg["id"], nt.strip())
                                    st.session_state.chat_editing = None
                                    st.rerun()
                        with ec2:
                            if st.button("Cancel", key=f"ec_{msg['id']}"):
                                st.session_state.chat_editing = None
                                st.rerun()

    st.divider()

    # Input
    ic1, ic2 = st.columns([4, 1])
    with ic1:
        text = st.text_input("Message", key=f"ci_{chat_with}", label_visibility="collapsed", placeholder="Type a message...")
        if text:
            _chat_set_typing(username, chat_with, True)
        else:
            _chat_set_typing(username, chat_with, False)

        file = st.file_uploader("📎", type=["jpg","jpeg","png","gif","pdf","txt","doc","docx"], key=f"cf_{chat_with}", label_visibility="collapsed")

    with ic2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📤 Send", type="primary", use_container_width=True, key=f"cs_{chat_with}"):
            if text.strip() or file:
                fd = None
                mtype = "text"
                if file:
                    fd = _chat_save_file(file, username)
                    if fd:
                        mtype = "image" if file.type.startswith("image/") else "file"
                txt = text.strip() if text.strip() else (f"Shared {fd['original_name']}" if fd else "")
                _chat_add_msg(username, chat_with, txt, mtype, fd)
                _chat_set_typing(username, chat_with, False)
                st.rerun()
            else:
                st.warning("Type or attach something")

    # Online users
    with st.expander("👥 Online"):
        on = _chat_get_online(exclude=username)
        if not on:
            st.write("No one else")
        else:
            for u in sorted(on.keys()):
                if st.button(f"💬 {u}", key=f"ou_{u}", use_container_width=True):
                    st.session_state.chat_current = u
                    st.rerun()


# ═══════════════════════════════════════════════════════════════
# THE BUTTON - PUT THIS ANYWHERE IN YOUR APP AFTER LOGIN
# ═══════════════════════════════════════════════════════════════

# Example placement:
st.divider()
chat_btn_col1, chat_btn_col2, chat_btn_col3 = st.columns([1, 2, 1])
with chat_btn_col2:
    # Get online count for the button label
    _chat_cleanup()  # auto cleanup
    current_user = st.session_state.get("username") or st.session_state.get("user") or "User"
    _chat_update_status(current_user, "online")
    online_count = len(_chat_get_online(exclude=current_user))

    if st.button(
        f"💬 Open Chat ({online_count} online)",
        type="primary",
        use_container_width=True,
        key="chat_popup_btn"
    ):
        st.session_state.chat_current = "global"
        open_chat_popup()  # ← OPENS THE POPUP!

# Optional: Quick chat with specific users
if online_count > 0:
    st.caption("Quick chat:")
    qcols = st.columns(min(online_count, 5))
    for i, u in enumerate(sorted(_chat_get_online(exclude=current_user).keys())):
        with qcols[i % len(qcols)]:
            if st.button(f"💬 {u}", key=f"qc_{u}"):
                st.session_state.chat_current = u
                open_chat_popup()  # ← OPENS POPUP WITH THAT USER!




















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

