import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# Assume df is your DataFrame
df = pd.read_csv("Analysis_Ready_DS_jobs.csv")




# Define the script
TAWK_SCRIPT = """
    <script type="text/javascript">
        var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
        (function(){
            var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
            s1.async=true;
            s1.src='https://embed.tawk.to/69e9b89cb84bb21c2c7155f8/1jmsfi8us';
            s1.charset='UTF-8';
            s1.setAttribute('crossorigin','*');
            s0.parentNode.insertBefore(s1,s0);
        })();
    </script>
"""

# Render the script in a hidden component
# We use height=0 and width=0 to ensure it doesn't move your layout
components.html(TAWK_SCRIPT, height=100)

# The rest of your app code goes here
st.title("My Streamlit App")
st.write("The chat widget should appear in the bottom right corner.")





import streamlit as st
components.html("""
<div style="text-align:center;">

<script>
function changeText(){
    document.getElementById("text").innerHTML = "🔥 JavaScript is working!";
}
</script>
""", height=0)



















