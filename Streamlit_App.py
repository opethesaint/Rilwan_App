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
# ═══════════════════════════════════════════════════════════════
# PRO WHATSAPP CHAT - PASTE INTO YOUR EXISTING app.py
# Uses ONLY native Streamlit elements - zero HTML, zero escaping issues
# ═══════════════════════════════════════════════════════════════

import json
import time
import base64
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

# ===============================================================
# CONFIG
# ===============================================================
CHAT_DIR = Path("chat_backend")
CHAT_DIR.mkdir(exist_ok=True)

CHAT_FILE = CHAT_DIR / "messages.json"
CHAT_USERS_FILE = CHAT_DIR / "users.json"
CHAT_TYPING_FILE = CHAT_DIR / "typing.json"
CHAT_READ_FILE = CHAT_DIR / "read_receipts.json"
CHAT_REACT_FILE = CHAT_DIR / "reactions.json"
CHAT_FILES_DIR = CHAT_DIR / "shared_files"
CHAT_FILES_DIR.mkdir(exist_ok=True)

MAX_FILE_MB = 10
HISTORY_DAYS = 30

EMOJIS = ["👍", "❤️", "😂", "😮", "😢", "🔥", "👏", "🎉", "🤔", "👎", "🙏", "💯"]

# ===============================================================
# JSON HELPERS
# ===============================================================

def _load(fp, default=None):
    return json.load(open(fp)) if fp.exists() else (default or {})

def _save(fp, data):
    json.dump(data, open(fp, 'w'), indent=2, default=str)

# ===============================================================
# USERS
# ===============================================================

def _update_status(user, status="online"):
    u = _load(CHAT_USERS_FILE, {})
    u[user] = {"status": status, "last_seen": datetime.now().isoformat(),
               "joined_at": u.get(user, {}).get("joined_at", datetime.now().isoformat())}
    _save(CHAT_USERS_FILE, u)

def _get_online(exclude=None):
    u = _load(CHAT_USERS_FILE, {})
    now = datetime.now()
    return {k: v for k, v in u.items() if k != exclude
            and (now - datetime.fromisoformat(v["last_seen"])).seconds <= 30
            and v["status"] == "online"}

# ===============================================================
# MESSAGES
# ===============================================================

def _load_msgs():
    return _load(CHAT_FILE, {"messages": [], "last_cleanup": datetime.now().isoformat()})

def _save_msgs(data):
    _save(CHAT_FILE, data)

def _add_msg(from_u, to_u, text, mtype="text", fdata=None):
    d = _load_msgs()
    msg = {
        "id": hashlib.md5(f"{from_u}{to_u}{datetime.now().isoformat()}".encode()).hexdigest()[:12],
        "from": from_u, "to": to_u, "text": text, "type": mtype,
        "file_data": fdata, "time": datetime.now().strftime("%H:%M"),
        "timestamp": datetime.now().isoformat(),
        "chat_type": "global" if to_u == "global" else "private",
        "edited": False, "edited_at": None, "deleted": False
    }
    d["messages"].append(msg)
    _save_msgs(d)
    return msg["id"]

def _edit_msg(mid, new_text):
    d = _load_msgs()
    for m in d["messages"]:
        if m["id"] == mid:
            m["text"] = new_text
            m["edited"] = True
            m["edited_at"] = datetime.now().isoformat()
            _save_msgs(d)
            return True
    return False

def _delete_msg(mid):
    d = _load_msgs()
    for m in d["messages"]:
        if m["id"] == mid:
            m["deleted"] = True
            m["text"] = "🗑️ This message was deleted"
            _save_msgs(d)
            return True
    return False

def _get_msgs(user, chat_with):
    d = _load_msgs()
    m = d.get("messages", [])
    if chat_with == "global":
        return [x for x in m if x.get("chat_type") == "global"]
    return [x for x in m if x.get("chat_type") == "private"
            and ((x["from"] == user and x["to"] == chat_with) or
                 (x["from"] == chat_with and x["to"] == user))]

# ===============================================================
# READ RECEIPTS
# ===============================================================

def _mark_read(user, chat_with):
    r = _load(CHAT_READ_FILE, {})
    for m in _get_msgs(user, chat_with):
        if m["from"] != user:
            mid = m["id"]
            r.setdefault(mid, {})[user] = datetime.now().isoformat()
    _save(CHAT_READ_FILE, r)

def _read_status(mid):
    return _load(CHAT_READ_FILE, {}).get(mid, {})

# ===============================================================
# REACTIONS
# ===============================================================

def _add_reaction(mid, user, emoji):
    r = _load(CHAT_REACT_FILE, {})
    r.setdefault(mid, {})
    ur = r[mid].get(user, [])
    if emoji in ur:
        ur.remove(emoji)
    else:
        ur.append(emoji)
    r[mid][user] = ur
    _save(CHAT_REACT_FILE, r)

def _get_reactions(mid):
    r = _load(CHAT_REACT_FILE, {}).get(mid, {})
    counts = {}
    for user, emojis in r.items():
        for e in emojis:
            counts.setdefault(e, []).append(user)
    return counts

# ===============================================================
# TYPING
# ===============================================================

def _set_typing(user, chat_with, typing=True):
    d = _load(CHAT_TYPING_FILE, {})
    key = f"{user}:{chat_with}"
    if typing:
        d[key] = {"since": datetime.now().isoformat(), "to": chat_with}
    else:
        d.pop(key, None)
    _save(CHAT_TYPING_FILE, d)

def _get_typing(chat_with, exclude):
    d = _load(CHAT_TYPING_FILE, {})
    now = datetime.now()
    users = []
    for key, info in d.items():
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

def _save_file(uploaded_file, user):
    if not uploaded_file:
        return None
    size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    if size_mb > MAX_FILE_MB:
        st.error(f"File too large! Max {MAX_FILE_MB}MB")
        return None
    ext = Path(uploaded_file.name).suffix
    unique = f"{hashlib.md5(f'{user}{datetime.now().isoformat()}'.encode()).hexdigest()[:16]}{ext}"
    path = CHAT_FILES_DIR / unique
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return {"original_name": uploaded_file.name, "saved_name": unique,
            "size_mb": round(size_mb, 2), "type": uploaded_file.type}

def _file_link(fdata):
    if not fdata:
        return None
    path = CHAT_FILES_DIR / fdata["saved_name"]
    if not path.exists():
        return None
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    mime = fdata.get("type", "application/octet-stream")
    return f"data:{mime};base64,{b64}"

# ===============================================================
# CLEANUP
# ===============================================================

def _cleanup(force=False):
    d = _load_msgs()
    last = datetime.fromisoformat(d.get("last_cleanup", datetime.now().isoformat()))
    now = datetime.now()
    if not force and (now - last).days < 1:
        return 0
    cutoff = now - timedelta(days=HISTORY_DAYS)
    msgs = d.get("messages", [])
    kept = [m for m in msgs if datetime.fromisoformat(m["timestamp"]) > cutoff]
    deleted = len(msgs) - len(kept)
    d["messages"] = kept
    d["last_cleanup"] = now.isoformat()
    _save_msgs(d)
    for fp in CHAT_FILES_DIR.iterdir():
        if fp.is_file() and datetime.fromtimestamp(fp.stat().st_mtime) < cutoff:
            fp.unlink()
    return deleted

def _clear_all():
    _save_msgs({"messages": [], "last_cleanup": datetime.now().isoformat()})
    for fp in CHAT_FILES_DIR.iterdir():
        if fp.is_file():
            fp.unlink()
    _save(CHAT_READ_FILE, {})
    _save(CHAT_TYPING_FILE, {})
    _save(CHAT_REACT_FILE, {})

# ===============================================================
# SESSION STATE
# ===============================================================

if "chat_current" not in st.session_state:
    st.session_state.chat_current = "global"
if "chat_editing" not in st.session_state:
    st.session_state.chat_editing = None
if "chat_reacting" not in st.session_state:
    st.session_state.chat_reacting = None

# ===============================================================
# ===============================================================
# CHAT POPUP DIALOG
# ===============================================================
# ===============================================================

@st.dialog("💬 Chat", width="large")
def open_chat_popup():
    """Opens a WhatsApp-style chat popup. Call this from a button."""

    # Get current user - ADJUST THIS to match your login system
    user = st.session_state.get("username") or st.session_state.get("user") or "User"

    _update_status(user, "online")
    chat_with = st.session_state.chat_current
    is_global = chat_with == "global"

    _mark_read(user, chat_with)

    # ═══════════════════════════════════════════════════════════
    # HEADER
    # ═══════════════════════════════════════════════════════════

    h1, h2 = st.columns([3, 1])
    with h1:
        if is_global:
            st.subheader("🌍 Global Chat")
            st.caption("Everyone can see these messages")
        else:
            online = _get_online(exclude=user)
            status = "🟢 Online" if chat_with in online else "⚪ Offline"
            st.subheader(f"💬 {chat_with}")
            st.caption(status)

    with h2:
        all_users = _load(CHAT_USERS_FILE, {})
        others = [u for u in all_users.keys() if u != user]
        options = ["🌍 Global Chat"] + sorted(others)
        current = f"🌍 Global Chat" if is_global else chat_with
        idx = options.index(current) if current in options else 0
        new_chat = st.selectbox("Switch", options, index=idx, key="chat_switch", label_visibility="collapsed")
        target = "global" if new_chat == "🌍 Global Chat" else new_chat
        if target != chat_with:
            st.session_state.chat_current = target
            st.rerun()

    st.divider()

    # ═══════════════════════════════════════════════════════════
    # TYPING INDICATOR
    # ═══════════════════════════════════════════════════════════

    typing = _get_typing(chat_with, user)
    if typing:
        verb = "is" if len(typing) == 1 else "are"
        st.caption(f"✏️ {', '.join(typing)} {verb} typing...")

    # ═══════════════════════════════════════════════════════════
    # MESSAGES - NATIVE STREAMLIT ONLY
    # ═══════════════════════════════════════════════════════════

    messages = _get_msgs(user, chat_with)

    msg_container = st.container(height=400)
    with msg_container:
        if not messages:
            st.info("👋 No messages yet. Start the conversation!")
        else:
            for msg in messages:
                is_me = msg["from"] == user
                is_deleted = msg.get("deleted", False)

                # Choose avatar
                avatar = "👤" if is_me else "🧑"
                name = "You" if is_me else msg["from"]

                # Build message content
                content_parts = []

                # Main text
                text = msg["text"]
                if msg.get("edited") and not is_deleted:
                    text += " *(edited)*"
                content_parts.append(text)

                # File attachment
                if msg.get("file_data") and not is_deleted:
                    fd = msg["file_data"]
                    link = _file_link(fd)
                    if msg["type"] == "image" and link:
                        content_parts.append(f"\n📷 {fd['original_name']}")
                    elif link:
                        content_parts.append(f"\n📎 {fd['original_name']} ({fd['size_mb']} MB)")

                # Reactions
                reactions = _get_reactions(msg["id"])
                if reactions and not is_deleted:
                    react_str = "  ".join([f"{emoji} {len(users)}" for emoji, users in reactions.items()])
                    content_parts.append(f"\n\n{react_str}")

                # Read receipt
                if is_me and not is_deleted:
                    by = _read_status(msg["id"])
                    if chat_with == "global":
                        cnt = len([u for u in by if u != user])
                        if cnt > 0:
                            content_parts.append(f"\n\n✓✓ Read by {cnt}")
                        else:
                            content_parts.append("\n\n✓ Sent")
                    else:
                        if chat_with in by:
                            content_parts.append("\n\n✓✓ Read")
                        else:
                            content_parts.append("\n\n✓ Sent")

                # Display using native st.chat_message
                full_content = "\n".join(content_parts)

                with st.chat_message(name, avatar=avatar):
                    st.write(full_content)

                    # Show image inline if it's an image
                    if msg.get("file_data") and not is_deleted and msg["type"] == "image":
                        fd = msg["file_data"]
                        link = _file_link(fd)
                        if link:
                            st.image(link, width=250)

                    # Action buttons in columns below message
                    if not is_deleted:
                        c1, c2, c3, c4 = st.columns([1, 1, 1, 6])

                        with c1:
                            if st.button("😊", key=f"react_{msg['id']}", help="React"):
                                st.session_state.chat_reacting = msg["id"] if st.session_state.chat_reacting != msg["id"] else None
                                st.rerun()

                        if is_me:
                            with c2:
                                if st.button("✏️", key=f"edit_{msg['id']}", help="Edit"):
                                    st.session_state.chat_editing = msg["id"]
                                    st.rerun()
                            with c3:
                                if st.button("🗑️", key=f"del_{msg['id']}", help="Delete"):
                                    _delete_msg(msg["id"])
                                    st.rerun()

                # Emoji picker (appears below the message)
                if st.session_state.chat_reacting == msg["id"]:
                    st.caption("Pick a reaction:")
                    emoji_cols = st.columns(len(EMOJIS))
                    for i, emoji in enumerate(EMOJIS):
                        with emoji_cols[i]:
                            if st.button(emoji, key=f"em_{msg['id']}_{emoji}"):
                                _add_reaction(msg["id"], user, emoji)
                                st.session_state.chat_reacting = None
                                st.rerun()

                # Edit form
                if st.session_state.chat_editing == msg["id"] and is_me:
                    with st.container(border=True):
                        new_text = st.text_input("Edit message", value=msg["text"], key=f"edit_in_{msg['id']}", label_visibility="collapsed")
                        ec1, ec2 = st.columns([1, 1])
                        with ec1:
                            if st.button("💾 Save", key=f"save_{msg['id']}", type="primary"):
                                if new_text.strip():
                                    _edit_msg(msg["id"], new_text.strip())
                                    st.session_state.chat_editing = None
                                    st.rerun()
                        with ec2:
                            if st.button("❌ Cancel", key=f"cancel_{msg['id']}"):
                                st.session_state.chat_editing = None
                                st.rerun()

    # ═══════════════════════════════════════════════════════════
    # INPUT AREA
    # ═══════════════════════════════════════════════════════════

    st.divider()

    # File upload
    uploaded = st.file_uploader(
        "📎 Attach file",
        type=["jpg", "jpeg", "png", "gif", "pdf", "txt", "doc", "docx"],
        key=f"file_{chat_with}",
        label_visibility="collapsed"
    )

    # Message input
    ic1, ic2 = st.columns([5, 1])
    with ic1:
        text = st.chat_input("Type a message...", key=f"input_{chat_with}")
        if text:
            _set_typing(user, chat_with, True)
        else:
            _set_typing(user, chat_with, False)

    # Send button (for file-only messages)
    if uploaded and not text:
        if st.button("📤 Send File", type="primary", use_container_width=True, key=f"send_file_{chat_with}"):
            fd = _save_file(uploaded, user)
            if fd:
                mtype = "image" if uploaded.type.startswith("image/") else "file"
                txt = f"📎 {fd['original_name']}"
                _add_msg(user, chat_with, txt, mtype, fd)
                _set_typing(user, chat_with, False)
                st.rerun()

    # Handle text message (from chat_input)
    if text:
        fd = None
        mtype = "text"
        if uploaded:
            fd = _save_file(uploaded, user)
            if fd:
                mtype = "image" if uploaded.type.startswith("image/") else "file"

        final_text = text.strip()
        if fd and mtype != "text" and not text.strip():
            final_text = f"📎 {fd['original_name']}"

        _add_msg(user, chat_with, final_text, mtype, fd)
        _set_typing(user, chat_with, False)
        st.rerun()

    # ═══════════════════════════════════════════════════════════
    # ONLINE USERS SIDEBAR (inside dialog)
    # ═══════════════════════════════════════════════════════════

    with st.expander("👥 Online Users"):
        online = _get_online(exclude=user)
        if not online:
            st.write("No one else is online")
        else:
            for u in sorted(online.keys()):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.write(f"🟢 {u}")
                with cols[1]:
                    if st.button("Chat", key=f"ou_btn_{u}"):
                        st.session_state.chat_current = u
                        st.rerun()

    # Settings
    with st.expander("⚙️ Settings"):
        st.write(f"Messages kept for: {HISTORY_DAYS} days")
        msg_count = len(_load_msgs().get("messages", []))
        st.write(f"Total messages: {msg_count}")

        if st.button("🧹 Cleanup Old Messages"):
            deleted = _cleanup(force=True)
            st.success(f"Deleted {deleted} old messages!")
            time.sleep(1)
            st.rerun()

        confirm = st.checkbox("I understand this will delete ALL messages")
        if st.button("💥 Clear ALL History", type="secondary"):
            if confirm:
                _clear_all()
                st.success("All history cleared!")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("Check the box to confirm")


# ═══════════════════════════════════════════════════════════════
# THE CHAT BUTTON - ADD THIS ANYWHERE IN YOUR APP AFTER LOGIN
# ═══════════════════════════════════════════════════════════════

# Example placement (put this wherever you want the chat button):
# st.divider()
# chat_col1, chat_col2, chat_col3 = st.columns([1, 2, 1])
# with chat_col2:
#     _cleanup()
#     current_user = st.session_state.get("username") or st.session_state.get("user") or "User"
#     _update_status(current_user, "online")
#     online_count = len(_get_online(exclude=current_user))
#     
#     if st.button(f"💬 Open Chat ({online_count} online)", type="primary", use_container_width=True):
#         st.session_state.chat_current = "global"
#         open_chat_popup()
# 
#     if online_count > 0:
#         st.caption("Quick chat:")
#         qcols = st.columns(min(online_count, 5))
#         for i, u in enumerate(sorted(_get_online(exclude=current_user).keys())):
#             with qcols[i % len(qcols)]:
#                 if st.button(f"💬 {u}", key=f"qc_{u}"):
#                     st.session_state.chat_current = u
#                     open_chat_popup()

















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

