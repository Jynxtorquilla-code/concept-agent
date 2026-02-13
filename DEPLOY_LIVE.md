# 🚀 LIVE DEPLOYMENT - Natuurhuisje Agent
## Van Local naar Live URL in 15 minuten

---

## ⭐ METHODE 1: Streamlit Cloud (AANBEVOLEN)

**Voordelen:**
- ✅ 5 minuten setup
- ✅ Gratis (unlimited apps!)
- ✅ Automatische HTTPS
- ✅ Geen server kennis nodig
- ✅ URL: `https://jouw-agent.streamlit.app`

### **Stap 1: GitHub Account maken (als je die nog niet hebt)**

1. Ga naar https://github.com
2. Klik "Sign up"
3. Maak account (gratis)

---

### **Stap 2: Repository maken**

1. Ga naar https://github.com/new
2. Repository naam: `natuurhuisje-agent`
3. Public aanvinken
4. Klik "Create repository"

---

### **Stap 3: Code uploaden naar GitHub**

**Optie A - Via GitHub Website (Makkelijkst):**

```
1. Op je repo pagina, klik "uploading an existing file"

2. Upload deze bestanden:
   - natuurhuisje_agent_v2.py
   - web_ui_v2.py (zie hieronder, nieuwe versie!)
   - training_data.csv
   - requirements.txt
   
3. Klik "Commit changes"
```

**Optie B - Via Command Line (Voor techies):**

```bash
# In de map met je bestanden:
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/JOUW-USERNAME/natuurhuisje-agent.git
git push -u origin main
```

---

### **Stap 4: Streamlit Cloud Account**

1. Ga naar https://share.streamlit.io
2. Klik "Sign up" 
3. **Sign in with GitHub** (makkelijkst!)
4. Geef Streamlit toegang tot je repositories

---

### **Stap 5: App Deployen**

1. Klik "New app"
2. Selecteer:
   - Repository: `jouw-username/natuurhuisje-agent`
   - Branch: `main`
   - Main file: `web_ui_v2.py`
3. Klik "Advanced settings"
4. Voeg toe onder "Secrets":

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-jouw-key-hier"
```

5. Klik "Deploy!"

---

### **Stap 6: Wacht 2-3 minuten**

Je ziet:
```
⏳ Building...
⏳ Installing dependencies...
✅ Your app is live!
```

**Je URL:** `https://natuurhuisje-agent-jouw-username.streamlit.app`

---

### **Stap 7: Deel met je team!**

Stuur de URL naar je collega's. Klaar! 🎉

---

## 🔒 BELANGRIJKE SECURITY NOTEN

### **API Key Beveiliging:**

**NOOIT doen:**
```python
api_key = "sk-ant-api03-abc123..."  # ❌ NOOIT in code!
```

**WEL doen:**
```python
import os
api_key = os.getenv('ANTHROPIC_API_KEY')  # ✅ Via secrets
```

In Streamlit Cloud:
- API key zit in "Secrets" (encrypted)
- Niet zichtbaar in code
- Veilig

---

## 💰 KOSTEN

### **Streamlit Cloud:**
- Gratis tier: Unlimited public apps
- Geen credit card nodig
- Perfect voor teams tot 50 gebruikers

### **Anthropic API:**
- ~€0.005 per analyse
- 1000 analyses = ~€5
- Budget instellen via console.anthropic.com

### **Totaal:**
- Setup: €0
- Maandelijks: €0 (Streamlit) + €5-50 (API gebruik)

**Dus: ~€10-50/maand voor 1000-10000 analyses**

---

## 📱 CUSTOM DOMAIN (Optioneel)

Als je eigen domain wilt (bijv. `natuurhuisje.jouwbedrijf.nl`):

1. Upgrade naar Streamlit Pro ($20/maand)
2. Of gebruik Cloudflare Workers (gratis)
3. Of deploy op eigen server (zie Methode 2)

---

## 🔄 UPDATES MAKEN

**Super simpel:**

```bash
# Maak wijzigingen in je code
# Upload naar GitHub (via website of git push)
# Streamlit detecteert dit automatisch
# App update binnen 1 minuut!
```

Of via GitHub website:
```
1. Ga naar je file op GitHub
2. Klik "Edit" (potlood icoon)
3. Maak wijzigingen
4. Klik "Commit changes"
5. Streamlit update automatisch!
```

---

## ⚠️ TROUBLESHOOTING

### "App won't start"
→ Check logs in Streamlit dashboard
→ Vaak: verkeerd filename (moet web_ui_v2.py zijn)

### "API Key not found"
→ Check Secrets in Streamlit dashboard
→ Format moet zijn: `ANTHROPIC_API_KEY = "sk-ant-..."`

### "Module not found"
→ Check requirements.txt is geupload
→ Alle dependencies moeten erin staan

### "Out of memory"
→ Streamlit gratis tier = 1GB RAM
→ Voor grotere apps: upgrade naar Pro

---

## 📊 MONITORING

**Via Streamlit Dashboard:**
- Aantal bezoekers
- Errors
- Uptime
- Resource gebruik

**Via Anthropic Dashboard:**
- API calls
- Kosten
- Rate limits

---

## 🔐 TOEGANGSBEHEER

### **Public (Gratis):**
- Iedereen met link kan gebruiken
- Goed voor: demos, open tools

### **Private (Streamlit Teams - $50/maand):**
- Alleen team members
- SSO integratie mogelijk
- Goed voor: interne tools

### **Custom Auth:**
Voeg toe in `web_ui_v2.py`:
```python
import streamlit_authenticator as stauth

# Login formulier
# Alleen toegang na login
```

---

## 🎓 VIDEO TUTORIAL

Kijk voor visuele uitleg:
https://docs.streamlit.io/deploy/streamlit-community-cloud

---

## ✅ DEPLOYMENT CHECKLIST

Voor je live gaat:

- [ ] GitHub account gemaakt
- [ ] Repository aangemaakt
- [ ] Alle bestanden geupload:
  - [ ] natuurhuisje_agent_v2.py
  - [ ] web_ui_v2.py
  - [ ] training_data.csv
  - [ ] requirements.txt
- [ ] Streamlit account gemaakt
- [ ] App deployment gestart
- [ ] API key toegevoegd in Secrets
- [ ] App getest (URL werkt)
- [ ] Gedeeld met team

---

## 🆘 HULP NODIG?

**Streamlit Support:**
- Forum: https://discuss.streamlit.io
- Docs: https://docs.streamlit.io

**Anthropic Support:**
- Docs: https://docs.anthropic.com
- Support: support@anthropic.com

**Of vraag ChatGPT/Claude:**
"Ik krijg error X bij Streamlit deployment, hoe los ik dit op?"

---

## 🚀 KLAAR OM TE DEPLOYEN?

Volg de stappen hierboven en binnen 15 minuten:
- ✅ Je agent is live
- ✅ Je hebt een URL om te delen
- ✅ Je team kan direct gebruiken

**Veel succes! 🌲**
