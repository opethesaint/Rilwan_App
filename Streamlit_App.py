import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# Assume df is your DataFrame
df = pd.read_csv("Analysis_Ready_DS_jobs.csv")


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









def chart1_salary_distribution(df):
    st.subheader("1. What is the distribution of salaries across all jobs?")
    fig, ax = plt.subplots()
    sns.histplot(df['Avg Salary (K)'], bins=30, kde=True, ax=ax)
    ax.set_title("Distribution of Average Salaries")
    st.pyplot(fig)

def chart2_salary_by_category(df):
    st.subheader("2. How do average salaries vary by job category?")
    fig, ax = plt.subplots()
    sns.barplot(x='Job Category', y='Avg Salary (K)', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

def chart3_salary_by_title(df):
    st.subheader("3. Which job titles have the highest average salary?")
    top_titles = df.groupby('Job Title')['Avg Salary (K)'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top_titles.values, y=top_titles.index, ax=ax)
    st.pyplot(fig)

def chart4_seniority_vs_salary(df):
    st.subheader("4. How does job seniority affect salary estimates?")
    fig, ax = plt.subplots()
    sns.boxplot(x='Job Seniority', y='Avg Salary (K)', data=df, ax=ax)
    st.pyplot(fig)

def chart5_remote_jobs(df):
    st.subheader("5. What proportion of jobs are remote vs non-remote?")
    fig, ax = plt.subplots()
    df['Is Remote'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
    st.pyplot(fig)

def chart6_rating_vs_salary(df):
    st.subheader("6. How does company rating correlate with average salary?")
    fig, ax = plt.subplots()
    sns.scatterplot(x='Rating', y='Avg Salary (K)', data=df, ax=ax)
    st.pyplot(fig)

def chart7_industry_salary(df):
    st.subheader("7. Which industries have the highest salary ranges?")
    fig, ax = plt.subplots()
    sns.barplot(x='Industry', y='Avg Salary (K)', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

def chart8_size_vs_salary(df):
    st.subheader("8. How does company size relate to salary estimates?")
    fig, ax = plt.subplots()
    sns.boxplot(x='Size', y='Avg Salary (K)', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

def chart9_company_age(df):
    st.subheader("9. What is the distribution of company ages?")
    fig, ax = plt.subplots()
    sns.histplot(df['Company Age'], bins=30, ax=ax)
    st.pyplot(fig)

def chart10_sector_salary(df):
    st.subheader("10. How do salaries differ across sectors?")
    fig, ax = plt.subplots()
    sns.barplot(x='Sector', y='Avg Salary (K)', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

def chart11_state_salary(df):
    st.subheader("11. Which states have the highest average salaries?")
    state_salary = df.groupby('Location State')['Avg Salary (K)'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=state_salary.values, y=state_salary.index, ax=ax)
    st.pyplot(fig)

def chart12_revenue_vs_rating(df):
    st.subheader("12. How does revenue band relate to company rating?")
    fig, ax = plt.subplots()
    sns.violinplot(x='Revenue Band', y='Rating', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

def chart13_job_category_counts(df):
    st.subheader("13. Which job categories are most common?")
    fig, ax = plt.subplots()
    sns.countplot(y='Job Category', data=df, order=df['Job Category'].value_counts().index, ax=ax)
    st.pyplot(fig)

def chart14_hq_salary(df):
    st.subheader("14. How does salary vary by headquarters location?")
    fig, ax = plt.subplots()
    sns.barplot(x='HQ State', y='Avg Salary (K)', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

def chart15_competitors_vs_salary(df):
    st.subheader("15. What is the relationship between competitor count and salary?")
    fig, ax = plt.subplots()
    sns.scatterplot(x='Competitor Count', y='Avg Salary (K)', data=df, ax=ax)
    st.pyplot(fig)

def chart16_top_rated_companies(df):
    st.subheader("16. Which companies have the highest ratings?")
    top_companies = df.groupby('Company Name')['Rating'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top_companies.values, y=top_companies.index, ax=ax)
    st.pyplot(fig)

def chart17_ownership_vs_salary(df):
    st.subheader("17. How does salary vary by type of ownership?")
    fig, ax = plt.subplots()
    sns.boxplot(x='Type of ownership', y='Avg Salary (K)', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

def chart18_founded_years(df):
    st.subheader("18. What is the distribution of founded years?")
    fig, ax = plt.subplots()
    sns.histplot(df['Founded'], bins=30, ax=ax)
    st.pyplot(fig)

def chart19_remote_by_sector(df):
    st.subheader("19. Which sectors have the most remote jobs?")
    fig, ax = plt.subplots()
    sns.countplot(x='Sector', hue='Is Remote', data=df, ax=ax)
    plt.xticks(rotation=90)
    st.pyplot(fig)

def chart20_description_length_vs_salary(df):
    st.subheader("20. How does job description length relate to salary?")
    df['Desc Length'] = df['Job Description'].str.len()
    fig, ax = plt.subplots()
    sns.scatterplot(x='Desc Length', y='Avg Salary (K)', data=df, ax=ax)
    st.pyplot(fig)













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

# ---------------- SIDEBAR MENU ----------------
st.sidebar.title("Job Data Explorer")

options = {
    "Salary Distribution": chart1_salary_distribution,
    "Salary by Job Category": chart2_salary_by_category,
    "Top Job Titles by Salary": chart3_salary_by_title,
    "Seniority vs Salary": chart4_seniority_vs_salary,
    "Remote vs Non-Remote": chart5_remote_jobs,
    "Rating vs Salary": chart6_rating_vs_salary,
    "Industry Salary": chart7_industry_salary,
    "Size vs Salary": chart8_size_vs_salary,
    "Company Age Distribution": chart9_company_age,
    "Sector Salary": chart10_sector_salary,
    "State Salary": chart11_state_salary,
    "Revenue vs Rating": chart12_revenue_vs_rating,
    "Job Category Counts": chart13_job_category_counts,
    "HQ Salary": chart14_hq_salary,
    "Competitors vs Salary": chart15_competitors_vs_salary,
    "Top Rated Companies": chart16_top_rated_companies,
    "Ownership vs Salary": chart17_ownership_vs_salary,
    "Founded Years": chart18_founded_years,
    "Remote Jobs by Sector": chart19_remote_by_sector,
    "Description Length vs Salary": chart20_description_length_vs_salary
}

choice = st.sidebar.selectbox("Choose a chart", list(options.keys()))

# ---------------- DISPLAY CHART ----------------
options[choice](df)



with st.sidebar:
    st.info("🌤️ Lagos: 28°C")




import streamlit as st
import time
import random

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "quick_pick" not in st.session_state:
    st.session_state.quick_pick = "Select one..."

# ---------------- SIDEBAR AI ASSISTANT ----------------
with st.sidebar:
    st.markdown("""
    <div style="
        background:rgba(255,255,255,0.08);
        padding:15px;
        border-radius:18px;
        box-shadow:0 0 15px rgba(0,255,255,0.3);
        text-align:center;">
        <h2 style="color:white;">🤖 AI Assistant</h2>
        <p style="color:lightgray;">Ask me anything</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- INPUTS ----------------
question = st.sidebar.text_input("💬 Type your question", key="user_input")

suggestion = st.sidebar.selectbox(
    "⚡ Quick Questions",
    ["Select one...", "Show summary", "Best chart?", "Explain data", "Top insights"],
    key="quick_pick"
)
# Use dropdown question if selected
if suggestion != "Select one...":
    question = suggestion

# ---------------- RESPONSES ----------------
responses = {
    "Show summary": "📊 Your dataset contains multiple columns with salary, jobs, and company insights.",
    "Best chart?": "📈 A bar chart or box plot would work best for salary comparisons.",
    "Explain data": "🧠 This dataset helps analyze salaries, remote jobs, ratings, and industries.",
    "Top insights": "🚀 Highest salaries appear in senior remote tech roles."
}

# ---------------- REPLY ----------------
if question and question != st.session_state.last_question:
    st.session_state.last_question = question

    with st.sidebar:
        placeholder = st.empty()

        reply = responses.get(question, random.choice([
            "🤔 Interesting question! Let me think...",
            "📊 I’d recommend visualizing that with a chart.",
            "🚀 That could reveal useful business insights.",
            "💡 Try filtering your data for better results."
        ]))

        text = ""
        for char in reply:
            text += char
            placeholder.markdown(f"**{text}**")
            time.sleep(0.03)

        st.session_state.chat_history.append(("You", question))
        st.session_state.chat_history.append(("AI", reply))

# ---------------- CHAT HISTORY ----------------
if st.session_state.chat_history:
    st.sidebar.markdown("### 📝 Chat History")
    for sender, msg in st.session_state.chat_history[-6:]:
        st.sidebar.write(f"**{sender}:** {msg}")

# ---------------- CLEAR BUTTON ----------------
if st.sidebar.button("🗑 Clear Chat", use_container_width=True):
    st.session_state.chat_history = []
    st.session_state.last_question = ""
    st.session_state.user_input = ""
    st.session_state.quick_pick = "Select one..."
    st.rerun()






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
        <a href="https://wa.me/message/J37UJJHFVN2WO1" class="whatsapp-button" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" viewBox="0 0 16 16">
              <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>
            </svg>
        </a>
    </div>
""", unsafe_allow_html=True)




