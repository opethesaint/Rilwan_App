import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components


components.html("""
<div style="text-align:center;">

<script>
function changeText(){
    document.getElementById("text").innerHTML = "🔥 JavaScript is working!";
}
</script>
""", height=0)


# Assume df is your DataFrame
df = pd.read_csv("Analysis_Ready_DS_jobs.csv")



























