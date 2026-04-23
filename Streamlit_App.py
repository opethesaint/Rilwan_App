import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# Assume df is your DataFrame
df = pd.read_csv("Analysis_Ready_DS_jobs.csv")


import streamlit.components.v1 as components



TAWK_SCRIPT = """
<style>
#tawk-position {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9999;
}
</style>

<div id="tawk-position"></div>

<script type="text/javascript">
var Tawk_API = Tawk_API || {}, Tawk_LoadStart = new Date();

(function() {
    var s1 = document.createElement("script");
    s1.async = true;
    s1.src = 'https://embed.tawk.to/69e9b89cb84bb21c2c7155f8/1jmsfi8us';
    s1.charset = 'UTF-8';
    s1.setAttribute('crossorigin', '*');
    document.body.appendChild(s1);
})();
</script>
"""

components.html(TAWK_SCRIPT, height=100)


<div style="text-align:center;">

<script>
function changeText(){
    document.getElementById("text").innerHTML = "🔥 JavaScript is working!";
}
</script>
""", height=0)





















with st.sidebar:
    st.markdown("💡 *Success is built one query at a time.*")




