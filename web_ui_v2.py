"""
Streamlit Web UI V2 - Met Training Data Support
Run with: streamlit run web_ui_v2.py
"""

import streamlit as st
import requests
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from natuurhuisje_agent_v2 import ImprovedNatuurhuisjeAgent, ScoringResult

# Page config
st.set_page_config(
    page_title="Natuurhuisje Agent V2",
    page_icon="🌲",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .score-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .score-high {
        background-color: #C8E6C9;
        border-left: 5px solid #2E7D32;
    }
    .score-medium {
        background-color: #FFF9C4;
        border-left: 5px solid #F9A825;
    }
    .score-low {
        background-color: #FFCDD2;
        border-left: 5px solid #C62828;
    }
    .training-badge {
        background-color: #E3F2FD;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def fetch_page_content(url: str) -> str:
    """Fetch HTML content from a URL"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text

def get_score_class(score: float) -> str:
    """Determine CSS class based on score"""
    if score >= 70:
        return "score-high"
    elif score >= 50:
        return "score-medium"
    else:
        return "score-low"

# Initialize agent (cached)
@st.cache_resource
def load_agent():
    """Load agent with training data"""
    try:
        agent = ImprovedNatuurhuisjeAgent(training_file='training_data.csv')
        return agent
    except Exception as e:
        st.error(f"⚠️ Kon agent niet laden: {e}")
        st.info("Zorg dat training_data.csv bestaat in dezelfde map.")
        return None

# Header
st.markdown('<h1 class="main-header">🌲 Natuurhuisje Agent V2</h1>', unsafe_allow_html=True)

# Check if training data loaded
agent = load_agent()

if agent:
    # Count training examples
    ja_count = len(agent.training_examples.get('ja', []))
    nee_count = len(agent.training_examples.get('nee', []))
    total_count = ja_count + nee_count
    
    if total_count > 0:
        st.markdown(f"""
        <div class="training-badge">
            🎓 Getraind met {total_count} voorbeelden 
            (✅ {ja_count} JA | ✗ {nee_count} NEE)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Geen training data geladen. Agent werkt op basis criteria.")

st.markdown("### AI-powered natuurhuisje classificatie met jouw training data")

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ Over deze tool")
    st.markdown("""
    Deze AI-agent is **getraind op jouw voorkeuren** en bepaalt of een accommodatie 
    een echt "natuurhuisje" is.
    
    **Hoe het werkt:**
    1. Agent ziet jouw gelabelde voorbeelden
    2. Vergelijkt nieuw huisje met jouw data
    3. Geeft score op basis van jouw patroon
    
    **Criteria:**
    - 🌳 Natuur nabijheid (30%)
    - 🏡 Privacy & rust (20%)
    - 🏞️ Omgeving kwaliteit (25%)
    - ✨ Authenticiteit (15%)
    - 🏘️ Bebouwing (10%)
    
    **Categorieën:**
    - ✅ Natuurhuisje (≥60 punten)
    - ❌ Geen natuurhuisje (<60 punten)
    """)
    
    st.divider()
    
    if agent and total_count > 0:
        st.markdown("**Training Data:**")
        st.metric("JA voorbeelden", ja_count)
        st.metric("NEE voorbeelden", nee_count)
        
        # Show some example URLs
        with st.expander("📋 Voorbeeld URLs"):
            if ja_count > 0:
                st.markdown("**✅ JA voorbeelden:**")
                for ex in agent.training_examples['ja'][:2]:
                    st.text(ex.url.split('/')[-1])
            if nee_count > 0:
                st.markdown("**✗ NEE voorbeelden:**")
                for ex in agent.training_examples['nee'][:2]:
                    st.text(ex.url.split('/')[-1])

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    url_input = st.text_input(
        "🔗 Voer een natuurhuisje.nl URL in:",
        value=st.session_state.get('test_url', ''),
        placeholder="https://www.natuurhuisje.nl/vakantiehuisje/..."
    )

with col2:
    st.write("")
    st.write("")
    analyze_button = st.button("🔍 Analyseer", type="primary", use_container_width=True)

# Analysis
if analyze_button and url_input and agent:
    if not url_input.startswith('http'):
        st.error("⚠️ Voer een geldige URL in")
    else:
        with st.spinner("🤖 AI aan het werk (met training data)..."):
            try:
                # Fetch content
                html_content = fetch_page_content(url_input)
                
                # Analyze
                result = agent.analyze_listing(url_input, html_content)
                
                # Display results
                score_class = get_score_class(result.confidence_score)
                
                # Main score card
                st.markdown(f"""
                <div class="score-box {score_class}">
                    <h2>{result.category}</h2>
                    <h1 style="margin: 0;">{result.confidence_score:.1f}/100</h1>
                </div>
                """, unsafe_allow_html=True)
                
                # Show similarity if available
                if result.similar_to:
                    similarity_emoji = {
                        'ja': '✅',
                        'nee': '✗'
                    }
                    similarity_label = {
                        'ja': 'JA voorbeelden',
                        'nee': 'NEE voorbeelden'
                    }
                    st.info(f"{similarity_emoji.get(result.similar_to, '🔍')} **Vergelijkbaar met:** {similarity_label.get(result.similar_to, result.similar_to)}")
                
                # Breakdown
                st.subheader("📊 Criterium Breakdown")
                
                cols = st.columns(2)
                criteria_list = list(result.breakdown.items())
                
                for idx, (criterion, score) in enumerate(criteria_list):
                    col = cols[idx % 2]
                    with col:
                        config = agent.criteria[criterion]
                        st.metric(
                            label=config['description'],
                            value=f"{score:.1f}/10",
                            delta=f"{((score - 5)/5 * 100):.0f}% vs gemiddeld" if score != 5 else None
                        )
                        st.progress(score / 10)
                
                # Reasoning
                st.subheader("💭 AI Redenering")
                st.info(result.reasoning)
                
                # Visual breakdown
                st.subheader("📈 Gewogen Impact")
                import pandas as pd
                
                breakdown_data = []
                for criterion, score in result.breakdown.items():
                    config = agent.criteria[criterion]
                    weighted_score = (score / 10) * config['weight']
                    breakdown_data.append({
                        'Criterium': config['description'][:30],
                        'Score': score,
                        'Gewicht': config['weight'],
                        'Bijdrage': weighted_score
                    })
                
                df = pd.DataFrame(breakdown_data)
                st.bar_chart(df.set_index('Criterium')['Bijdrage'])
                
                # Add feedback section
                st.divider()
                st.subheader("📝 Feedback")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✅ Klopt!", use_container_width=True):
                        st.success("Bedankt! Deze feedback helpt de agent verbeteren.")
                
                with col2:
                    if st.button("❌ Klopt niet", use_container_width=True):
                        st.warning("Voeg deze URL toe aan training_data.csv met jouw oordeel!")
                
            except Exception as e:
                st.error(f"❌ Fout tijdens analyse: {e}")
                st.info("💡 Tip: Check of de URL correct is en toegankelijk.")

elif not agent:
    st.error("⚠️ Agent kon niet worden geladen. Check of training_data.csv bestaat.")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666;">
    Gemaakt met ❤️ voor natuurhuisje.nl | Powered by Claude 4.5 Sonnet
</div>
""", unsafe_allow_html=True)

# Instructions for first-time users
with st.expander("🆘 Hulp nodig?"):
    st.markdown("""
    **Voor eerste keer gebruikers:**
    
    1. Plak een natuurhuisje.nl URL in het veld
    2. Klik op "Analyseer"
    3. Wacht 5-10 seconden
    4. Bekijk de score en redenering
    
    **Training data bijwerken:**
    
    1. Open training_data.csv
    2. Voeg nieuwe voorbeelden toe
    3. Herstart de app (klik R in terminal)
    
    **Problemen?**
    
    - "URL not found" → Check of URL correct is
    - "API key error" → Check ANTHROPIC_API_KEY environment variable
    - "Slow response" → Dit is normaal, AI analyse duurt 5-15 sec
    """)
