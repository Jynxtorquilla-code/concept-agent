import streamlit as st

st.set_page_config(
    page_title="Natuurhuisje Agent V2",
    page_icon="🌲",
    layout="wide"
)

st.markdown('<h1 style="color: #2E7D32; text-align: center;">🌲 Natuurhuisje Agent V2</h1>', unsafe_allow_html=True)

st.success("✅ App werkt! We kunnen nu stap voor stap de functionaliteit toevoegen.")

st.info("""
Deze test versie laat zien dat Streamlit correct werkt.
Nu kunnen we de agent functionaliteit toevoegen.
""")

# Test of we training data kunnen laden
import os
if os.path.exists('training_data.csv'):
    st.success("✅ training_data.csv gevonden!")
    import pandas as pd
    df = pd.read_csv('training_data.csv')
    st.write(f"Aantal voorbeelden: {len(df)}")
else:
    st.error("❌ training_data.csv niet gevonden")

# Test of we de agent kunnen importeren
try:
    from natuurhuisje_agent_v2 import ImprovedNatuurhuisjeAgent
    st.success("✅ Agent module kan worden geïmporteerd!")
except Exception as e:
    st.error(f"❌ Kan agent niet importeren: {e}")
