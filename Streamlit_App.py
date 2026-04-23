import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# Assume df is your DataFrame
df = pd.read_csv("Analysis_Ready_DS_jobs.csv")


import streamlit as st
import streamlit as st
import streamlit.components.v1 as components

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

components.html(TAWK_SCRIPT, height=0, width=0)


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

# Floating style container


















with st.sidebar:
    st.info("🌤️ Lagos: 28°C")






with st.sidebar:
    st.markdown("💡 *Success is built one query at a time.*")




