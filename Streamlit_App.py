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
import streamlit as st
import json
import time
import base64
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

st.set_page_config(page_title="Chat App", layout="wide", initial_sidebar_state="collapsed")

# ===============================================================
# CONFIGURATION
# ===============================================================
DATA_DIR = Path("chat_backend")
DATA_DIR.mkdir(exist_ok=True)

CHAT_FILE = DATA_DIR / "messages.json"
USERS_FILE = DATA_DIR / "users.json"
TYPING_FILE = DATA_DIR / "typing.json"
READ_RECEIPTS_FILE = DATA_DIR / "read_receipts.json"
FILES_DIR = DATA_DIR / "shared_files"
FILES_DIR.mkdir(exist_ok=True)
REACTIONS_FILE = DATA_DIR / "reactions.json"

MAX_FILE_SIZE_MB = 10
MAX_CHAT_HISTORY_DAYS = 30
AUTO_REFRESH_INTERVAL = 2

# ===============================================================
# JSON BACKEND FUNCTIONS
# ===============================================================

def load_json(filepath, default=None):
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default if default is not None else {}

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)

def load_messages():
    return load_json(CHAT_FILE, {"messages": [], "last_cleanup": datetime.now().isoformat()})

def save_messages(data):
    save_json(CHAT_FILE, data)

def load_users():
    return load_json(USERS_FILE, {})

def save_users(users):
    save_json(USERS_FILE, users)

def load_typing():
    return load_json(TYPING_FILE, {})

def save_typing(data):
    save_json(TYPING_FILE, data)

def load_read_receipts():
    return load_json(READ_RECEIPTS_FILE, {})

def save_read_receipts(data):
    save_json(READ_RECEIPTS_FILE, data)

def load_reactions():
    return load_json(REACTIONS_FILE, {})

def save_reactions(data):
    save_json(REACTIONS_FILE, data)

# ===============================================================
# USER MANAGEMENT
# ===============================================================

def update_user_status(username, status="online"):
    users = load_users()
    users[username] = {
        "status": status,
        "last_seen": datetime.now().isoformat(),
        "joined_at": users.get(username, {}).get("joined_at", datetime.now().isoformat())
    }
    save_users(users)

def get_online_users(exclude=None):
    users = load_users()
    now = datetime.now()
    online = {}
    for user, info in users.items():
        if user == exclude:
            continue
        last_seen = datetime.fromisoformat(info["last_seen"])
        if (now - last_seen).seconds <= 30 and info["status"] == "online":
            online[user] = info
    return online

def get_all_users():
    return load_users()

# ===============================================================
# MESSAGE FUNCTIONS
# ===============================================================

def add_message(from_user, to_user, text, msg_type="text", file_data=None):
    data = load_messages()
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
    save_messages(data)
    return msg["id"]

def edit_message(msg_id, new_text):
    data = load_messages()
    for msg in data["messages"]:
        if msg["id"] == msg_id:
            msg["text"] = new_text
            msg["edited"] = True
            msg["edited_at"] = datetime.now().isoformat()
            save_messages(data)
            return True
    return False

def delete_message(msg_id):
    data = load_messages()
    for msg in data["messages"]:
        if msg["id"] == msg_id:
            msg["deleted"] = True
            msg["text"] = "This message was deleted"
            save_messages(data)
            return True
    return False

def get_messages_for_chat(username, chat_with):
    data = load_messages()
    messages = data.get("messages", [])

    if chat_with == "global":
        return [m for m in messages if m.get("chat_type") == "global"]
    else:
        return [
            m for m in messages
            if m.get("chat_type") == "private"
            and (
                (m["from"] == username and m["to"] == chat_with) or
                (m["from"] == chat_with and m["to"] == username)
            )
        ]

def mark_messages_as_read(username, chat_with):
    receipts = load_read_receipts()
    messages = get_messages_for_chat(username, chat_with)

    for msg in messages:
        if msg["from"] != username:
            msg_id = msg["id"]
            if msg_id not in receipts:
                receipts[msg_id] = {}
            receipts[msg_id][username] = datetime.now().isoformat()

    save_read_receipts(receipts)

def get_read_status(msg_id):
    receipts = load_read_receipts()
    return receipts.get(msg_id, {})

# ===============================================================
# REACTIONS
# ===============================================================

def add_reaction(msg_id, username, emoji):
    reactions = load_reactions()
    if msg_id not in reactions:
        reactions[msg_id] = {}

    # Toggle: if user already reacted with this emoji, remove it
    user_reactions = reactions[msg_id].get(username, [])
    if emoji in user_reactions:
        user_reactions.remove(emoji)
    else:
        user_reactions.append(emoji)

    reactions[msg_id][username] = user_reactions
    save_reactions(reactions)

def get_message_reactions(msg_id):
    reactions = load_reactions()
    msg_reactions = reactions.get(msg_id, {})

    # Count each emoji
    emoji_counts = {}
    for user, emojis in msg_reactions.items():
        for emoji in emojis:
            if emoji not in emoji_counts:
                emoji_counts[emoji] = []
            emoji_counts[emoji].append(user)

    return emoji_counts

# ===============================================================
# TYPING INDICATORS
# ===============================================================

def set_typing(username, chat_with, is_typing=True):
    typing_data = load_typing()
    key = f"{username}:{chat_with}"
    if is_typing:
        typing_data[key] = {
            "since": datetime.now().isoformat(),
            "to": chat_with
        }
    else:
        typing_data.pop(key, None)
    save_typing(typing_data)

def get_typing_users(chat_with, exclude):
    typing_data = load_typing()
    now = datetime.now()
    typing_users = []

    for key, info in typing_data.items():
        parts = key.split(":", 1)
        if len(parts) != 2:
            continue
        user, to = parts
        if user == exclude:
            continue
        if to == chat_with or (chat_with == "global" and to == "global"):
            since = datetime.fromisoformat(info["since"])
            if (now - since).seconds <= 5:
                typing_users.append(user)

    return typing_users

# ===============================================================
# FILE SHARING
# ===============================================================

def save_uploaded_file(uploaded_file, username):
    if uploaded_file is None:
        return None

    file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(f"File too large! Max {MAX_FILE_SIZE_MB}MB")
        return None

    ext = Path(uploaded_file.name).suffix
    unique_name = f"{hashlib.md5(f'{username}{datetime.now().isoformat()}'.encode()).hexdigest()[:16]}{ext}"
    file_path = FILES_DIR / unique_name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    return {
        "original_name": uploaded_file.name,
        "saved_name": unique_name,
        "size_mb": round(file_size_mb, 2),
        "type": uploaded_file.type
    }

def get_file_download_link(file_data):
    if not file_data:
        return None

    file_path = FILES_DIR / file_data["saved_name"]
    if not file_path.exists():
        return None

    with open(file_path, "rb") as f:
        data = f.read()

    b64 = base64.b64encode(data).decode()
    mime = file_data.get("type", "application/octet-stream")

    return f"data:{mime};base64,{b64}"

# ===============================================================
# CHAT HISTORY CLEANUP
# ===============================================================

def cleanup_old_messages(force=False):
    data = load_messages()
    last_cleanup = datetime.fromisoformat(data.get("last_cleanup", datetime.now().isoformat()))
    now = datetime.now()

    if not force and (now - last_cleanup).days < 1:
        return 0

    cutoff = now - timedelta(days=MAX_CHAT_HISTORY_DAYS)
    messages = data.get("messages", [])
    original_count = len(messages)

    kept_messages = []
    for msg in messages:
        msg_time = datetime.fromisoformat(msg["timestamp"])
        if msg_time > cutoff:
            kept_messages.append(msg)

    deleted = original_count - len(kept_messages)
    data["messages"] = kept_messages
    data["last_cleanup"] = now.isoformat()
    save_messages(data)

    cleanup_old_files()

    return deleted

def cleanup_old_files():
    cutoff = datetime.now() - timedelta(days=MAX_CHAT_HISTORY_DAYS)
    deleted = 0
    for file_path in FILES_DIR.iterdir():
        if file_path.is_file():
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if mtime < cutoff:
                file_path.unlink()
                deleted += 1
    return deleted

def cleanup_all_chat_history():
    save_messages({"messages": [], "last_cleanup": datetime.now().isoformat()})
    for file_path in FILES_DIR.iterdir():
        if file_path.is_file():
            file_path.unlink()
    save_read_receipts({})
    save_typing({})
    save_reactions({})

# ===============================================================
# SESSION STATE INIT
# ===============================================================

if "username" not in st.session_state:
    st.session_state.username = None
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None
if "show_settings" not in st.session_state:
    st.session_state.show_settings = False
if "editing_msg" not in st.session_state:
    st.session_state.editing_msg = None
if "show_reactions" not in st.session_state:
    st.session_state.show_reactions = None

# ===============================================================
# CSS STYLING
# ===============================================================

st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        max-width: 75%;
        word-wrap: break-word;
        position: relative;
    }
    .chat-message-me {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        text-align: right;
    }
    .chat-message-other {
        background: #f0f2f6;
        color: #333;
        margin-right: auto;
    }
    .chat-message-deleted {
        opacity: 0.6;
        font-style: italic;
    }
    .typing-indicator {
        color: #888;
        font-style: italic;
        padding: 0.5rem;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }
    .read-receipt {
        font-size: 0.7rem;
        color: #4CAF50;
        margin-top: 2px;
    }
    .read-receipt-pending {
        font-size: 0.7rem;
        color: #aaa;
        margin-top: 2px;
    }
    .edited-tag {
        font-size: 0.65rem;
        opacity: 0.7;
        font-style: italic;
    }
    .file-attachment {
        background: rgba(255,255,255,0.2);
        border-radius: 8px;
        padding: 8px;
        margin-top: 5px;
    }
    .image-attachment {
        border-radius: 8px;
        max-width: 300px;
        margin-top: 5px;
    }
    .reaction-bar {
        margin-top: 5px;
        display: flex;
        gap: 5px;
        flex-wrap: wrap;
    }
    .reaction-badge {
        background: rgba(0,0,0,0.1);
        border-radius: 12px;
        padding: 2px 8px;
        font-size: 0.8rem;
        cursor: pointer;
    }
    .reaction-badge:hover {
        background: rgba(0,0,0,0.2);
    }
    .msg-actions {
        opacity: 0;
        transition: opacity 0.2s;
        font-size: 0.75rem;
    }
    .chat-message:hover .msg-actions {
        opacity: 1;
    }
    .emoji-picker {
        background: white;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 8px;
        display: flex;
        gap: 5px;
        flex-wrap: wrap;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .emoji-btn {
        background: none;
        border: none;
        font-size: 1.2rem;
        cursor: pointer;
        padding: 4px;
        border-radius: 50%;
        transition: background 0.2s;
    }
    .emoji-btn:hover {
        background: #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

# ===============================================================
# EMOJI LIST
# ===============================================================

COMMON_EMOJIS = ["👍", "❤️", "😂", "😮", "😢", "🔥", "👏", "🎉", "🤔", "👎", "🙏", "💯"]

# ===============================================================
# USER LOGIN / NAME ENTRY
# ===============================================================

if not st.session_state.username:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center;">
            <h1>Chat App</h1>
            <p style="color: #666;">Real-time messaging with reactions, edits & file sharing</p>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            name = st.text_input("Enter your display name", placeholder="John Doe", key="name_input")

            if st.button("Join Chat", type="primary", use_container_width=True):
                if name.strip():
                    st.session_state.username = name.strip()
                    update_user_status(name.strip(), "online")
                    st.rerun()
                else:
                    st.error("Please enter a name")

        st.markdown("""
        <div style="text-align: center; color: #888; margin-top: 20px;">
            <small>Features: Real-time chat | Read receipts | Typing indicators | File sharing | Reactions | Edit/Delete</small>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ===============================================================
# MAIN APP - LOGGED IN
# ===============================================================

username = st.session_state.username
update_user_status(username, "online")

cleanup_old_messages()

# ===============================================================
# SIDEBAR - USERS & SETTINGS
# ===============================================================

with st.sidebar:
    st.header(f"{username}")
    st.caption("You are online")

    if st.button("Logout", use_container_width=True):
        update_user_status(username, "offline")
        st.session_state.username = None
        st.session_state.current_chat = None
        st.session_state.editing_msg = None
        st.rerun()

    st.divider()

    # Online Users
    st.subheader("Online Users")
    online_users = get_online_users(exclude=username)
    all_users = get_all_users()

    if not online_users:
        st.info("No one else online")

    for user in sorted(online_users.keys()):
        if st.button(f"Chat with {user}", key=f"sidebar_user_{user}", use_container_width=True):
            st.session_state.current_chat = user
            st.session_state.editing_msg = None
            st.rerun()

    st.divider()

    # All Users
    st.subheader("All Users")
    for user in sorted(all_users.keys()):
        if user == username:
            continue
        info = all_users[user]
        status = "Online" if user in online_users else "Offline"
        last_seen = datetime.fromisoformat(info["last_seen"])
        time_ago = "just now" if (datetime.now() - last_seen).seconds < 60 else f"{(datetime.now() - last_seen).seconds // 60}m ago"

        if st.button(f"{user} ({status} - {time_ago})", key=f"all_user_{user}", use_container_width=True):
            st.session_state.current_chat = user
            st.session_state.editing_msg = None
            st.rerun()

    st.divider()

    # Settings
    st.subheader("Settings")

    with st.expander("Chat History"):
        st.write(f"Messages kept for: {MAX_CHAT_HISTORY_DAYS} days")

        msg_data = load_messages()
        msg_count = len(msg_data.get("messages", []))
        st.write(f"Current messages: {msg_count}")

        if st.button("Cleanup Old Messages", use_container_width=True):
            deleted = cleanup_old_messages(force=True)
            st.success(f"Deleted {deleted} old messages!")
            time.sleep(1)
            st.rerun()

        confirm_clear = st.checkbox("Confirm clear all")
        if st.button("Clear ALL History", use_container_width=True):
            if confirm_clear:
                cleanup_all_chat_history()
                st.success("All chat history cleared!")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("Check the box to confirm")

# ===============================================================
# MAIN CONTENT AREA
# ===============================================================

# Header
header_col1, header_col2, header_col3 = st.columns([3, 2, 1])
with header_col1:
    st.title("Chat App")
with header_col2:
    online_count = len(get_online_users(exclude=username))
    st.markdown(f"<p style='margin-top: 15px; color: #4CAF50;'>{online_count} user(s) online</p>", unsafe_allow_html=True)
with header_col3:
    if st.button("Settings", key="settings_btn"):
        st.session_state.show_settings = not st.session_state.show_settings

st.divider()

# ===============================================================
# CHAT SELECTION OR DASHBOARD
# ===============================================================

if not st.session_state.current_chat:
    # DASHBOARD VIEW
    st.markdown("""
    <div style="text-align: center; padding: 40px;">
        <h2>Welcome to Chat!</h2>
        <p style="color: #666;">Select a user from the sidebar or start a global chat below</p>
    </div>
    """, unsafe_allow_html=True)

    # Global Chat Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Open Global Chat", type="primary", use_container_width=True):
            st.session_state.current_chat = "global"
            st.session_state.editing_msg = None
            st.rerun()

    # Quick access to online users
    if online_users:
        st.subheader("Start a conversation:")
        cols = st.columns(min(len(online_users), 4))
        for idx, user in enumerate(sorted(online_users.keys())):
            with cols[idx % len(cols)]:
                if st.button(f"Chat with {user}", key=f"quick_{user}", use_container_width=True):
                    st.session_state.current_chat = user
                    st.session_state.editing_msg = None
                    st.rerun()

else:
    # CHAT VIEW
    chat_with = st.session_state.current_chat
    is_global = chat_with == "global"

    # Chat Header
    chat_header_col1, chat_header_col2, chat_header_col3 = st.columns([5, 2, 1])

    with chat_header_col1:
        if is_global:
            st.header("Global Chat")
            st.caption("Everyone can see these messages")
        else:
            online_users = get_online_users(exclude=username)
            is_online = chat_with in online_users
            status_text = "online" if is_online else "offline"
            st.header(f"{chat_with}")
            st.caption(f"User is {status_text}")

    with chat_header_col3:
        if st.button("Back", key="back_btn", use_container_width=True):
            st.session_state.current_chat = None
            st.session_state.editing_msg = None
            st.session_state.show_reactions = None
            st.rerun()

    st.divider()

    # Mark messages as read when opening chat
    mark_messages_as_read(username, chat_with)

    # ===========================================================
    # TYPING INDICATOR
    # ===========================================================

    typing_users = get_typing_users(chat_with, username)
    if typing_users:
        typing_text = ", ".join(typing_users)
        if len(typing_users) == 1:
            st.markdown(f"<div class='typing-indicator'>{typing_text} is typing...</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='typing-indicator'>{typing_text} are typing...</div>", unsafe_allow_html=True)

    # ===========================================================
    # MESSAGES DISPLAY
    # ===========================================================

    messages = get_messages_for_chat(username, chat_with)

    chat_container = st.container(height=450)
    with chat_container:
        if not messages:
            st.markdown("""
            <div style="text-align: center; color: #aaa; padding: 50px;">
                <h3>No messages yet</h3>
                <p>Start the conversation!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in messages:
                is_me = msg["from"] == username
                is_deleted = msg.get("deleted", False)
                msg_class = "chat-message-me" if is_me else "chat-message-other"
                if is_deleted:
                    msg_class += " chat-message-deleted"

                # Read receipts
                read_status_html = ""
                if is_me and not is_deleted:
                    read_by = get_read_status(msg["id"])
                    if chat_with == "global":
                        read_count = len([u for u in read_by if u != username])
                        if read_count > 0:
                            read_status_html = f"<div class='read-receipt'>Read by {read_count}</div>"
                        else:
                            read_status_html = "<div class='read-receipt-pending'>Sent</div>"
                    else:
                        if chat_with in read_by:
                            read_status_html = "<div class='read-receipt'>Read</div>"
                        else:
                            read_status_html = "<div class='read-receipt-pending'>Sent</div>"

                # Edited tag
                edited_html = ""
                if msg.get("edited") and not is_deleted:
                    edited_time = datetime.fromisoformat(msg["edited_at"]).strftime("%H:%M")
                    edited_html = f"<span class='edited-tag'>(edited {edited_time})</span>"

                # File/image handling
                attachment_html = ""
                if msg.get("file_data") and not is_deleted:
                    file_data = msg["file_data"]
                    download_link = get_file_download_link(file_data)

                    if msg["type"] == "image" and download_link:
                        attachment_html = f'<img src="{download_link}" class="image-attachment" />'
                    elif download_link:
                        text_color = "white" if is_me else "#333"
                        attachment_html = f'<div class="file-attachment"><a href="{download_link}" download="{file_data["original_name"]}" style="color: {text_color}; text-decoration: underline;">{file_data["original_name"]} ({file_data["size_mb"]} MB)</a></div>'

                # Reactions
                reactions_html = ""
                if not is_deleted:
                    reactions = get_message_reactions(msg["id"])
                    if reactions:
                        reaction_badges = []
                        for emoji, users in reactions.items():
                            count = len(users)
                            tooltip = ", ".join(users)
                            reaction_badges.append(f'<span class="reaction-badge" title="{tooltip}">{emoji} {count}</span>')
                        reactions_html = '<div class="reaction-bar">' + "".join(reaction_badges) + '</div>'

                # Message actions (edit/delete for my messages, react for all)
                actions_html = ""
                if is_me and not is_deleted:
                    # Edit/Delete buttons
                    edit_key = f"edit_{msg['id']}"
                    delete_key = f"delete_{msg['id']}"
                    react_key = f"react_{msg['id']}"

                    # We use Streamlit buttons below the message instead of inline HTML buttons
                    pass

                st.markdown(f"""
                <div class="chat-message {msg_class}" id="msg_{msg['id']}">
                    <small><b>{msg["from"]}</b> - {msg["time"]}</small><br>
                    {msg["text"]}
                    {edited_html}
                    {attachment_html}
                    {reactions_html}
                    {read_status_html}
                </div>
                <div style="clear: both;"></div>
                """, unsafe_allow_html=True)

                # Message action buttons row
                if not is_deleted:
                    action_cols = st.columns([1, 1, 1, 8])

                    # React button
                    with action_cols[0]:
                        if st.button("😊", key=f"react_btn_{msg['id']}", help="Add reaction"):
                            if st.session_state.show_reactions == msg["id"]:
                                st.session_state.show_reactions = None
                            else:
                                st.session_state.show_reactions = msg["id"]
                            st.rerun()

                    # Edit button (only my messages)
                    if is_me:
                        with action_cols[1]:
                            if st.button("✏️", key=f"edit_btn_{msg['id']}", help="Edit message"):
                                st.session_state.editing_msg = msg["id"]
                                st.rerun()

                        with action_cols[2]:
                            if st.button("🗑️", key=f"delete_btn_{msg['id']}", help="Delete message"):
                                delete_message(msg["id"])
                                st.rerun()

                # Emoji picker
                if st.session_state.show_reactions == msg["id"]:
                    emoji_cols = st.columns(len(COMMON_EMOJIS))
                    for idx, emoji in enumerate(COMMON_EMOJIS):
                        with emoji_cols[idx]:
                            if st.button(emoji, key=f"emoji_{msg['id']}_{emoji}"):
                                add_reaction(msg["id"], username, emoji)
                                st.session_state.show_reactions = None
                                st.rerun()

                # Edit form
                if st.session_state.editing_msg == msg["id"] and is_me:
                    with st.container(border=True):
                        new_text = st.text_input("Edit message", value=msg["text"], key=f"edit_input_{msg['id']}")
                        edit_col1, edit_col2 = st.columns([1, 1])
                        with edit_col1:
                            if st.button("Save", key=f"save_edit_{msg['id']}", type="primary"):
                                if new_text.strip():
                                    edit_message(msg["id"], new_text.strip())
                                    st.session_state.editing_msg = None
                                    st.rerun()
                        with edit_col2:
                            if st.button("Cancel", key=f"cancel_edit_{msg['id']}"):
                                st.session_state.editing_msg = None
                                st.rerun()

    # ===========================================================
    # MESSAGE INPUT AREA
    # ===========================================================

    st.divider()

    # File upload area
    upload_col1, upload_col2 = st.columns([3, 1])
    with upload_col1:
        uploaded_file = st.file_uploader(
            "Attach file (image, doc, etc.)", 
            type=["jpg", "jpeg", "png", "gif", "pdf", "txt", "doc", "docx"],
            key=f"file_uploader_{chat_with}",
            label_visibility="collapsed"
        )

    # Message input
    message_col1, message_col2 = st.columns([5, 1])

    with message_col1:
        message_text = st.text_input(
            "Type a message...", 
            key=f"msg_input_{chat_with}",
            label_visibility="collapsed",
            placeholder="Type a message..."
        )

        # Update typing status
        if message_text:
            set_typing(username, chat_with, True)
        else:
            set_typing(username, chat_with, False)

    with message_col2:
        if st.button("Send", type="primary", use_container_width=True, key=f"send_btn_{chat_with}"):
            if message_text.strip() or uploaded_file:
                file_data = None
                msg_type = "text"

                if uploaded_file:
                    file_data = save_uploaded_file(uploaded_file, username)
                    if file_data:
                        if uploaded_file.type.startswith("image/"):
                            msg_type = "image"
                        else:
                            msg_type = "file"

                text_to_send = message_text.strip() if message_text.strip() else ""
                if msg_type != "text" and not text_to_send:
                    text_to_send = f"Shared {file_data['original_name']}"

                add_message(username, chat_with, text_to_send, msg_type, file_data)
                set_typing(username, chat_with, False)
                st.rerun()
            else:
                st.warning("Type a message or attach a file")

# ===============================================================
# AUTO REFRESH
# ===============================================================

time.sleep(AUTO_REFRESH_INTERVAL)
st.rerun()








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

