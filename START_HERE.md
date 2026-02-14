# 🚀 SETUP INSTRUCTIONS - START HERE!

## Quick Start (3 Steps)

### 1️⃣ Get Google AI API Key (FREE)
1. Visit: https://aistudio.google.com/apikey
2. Sign in with Google account
3. Click "Create API key"
4. Copy the key

### 2️⃣ Run Setup
```bash
# Double-click this file:
setup.bat

# OR run manually in terminal:
cd "d:\ML\Projects\AI_assignment\AI Voice Bot"
setup.bat
```

This will:
- Create Python virtual environment
- Install backend dependencies
- Install frontend dependencies
- Create .env file

### 3️⃣ Add Your API Key
Edit `backend\.env` file:
```
GOOGLE_API_KEY=paste_your_key_here
```

## Run the Application

### Terminal 1 - Backend:
```bash
run-backend.bat
```
Wait for: "Server: http://0.0.0.0:8000"

### Terminal 2 - Frontend:
```bash
run-frontend.bat
```
Wait for: "Local: http://localhost:5173"

## Open & Test
1. Open: http://localhost:5173 in **Chrome or Edge**
2. Allow microphone permissions
3. Click "Start Talking"
4. Start speaking!

## 📝 Important Notes

- **Browser**: Use Chrome, Edge, or Safari (NOT Firefox)
- **Microphone**: Must grant permission
- **Sample Image**: Add any child-friendly image to `frontend/public/sample_image.png`
  - OR use the placeholder generator: Open `frontend/public/generate_sample_image.html` and screenshot it

## 💰 Cost: 100% FREE
- Google Gemini: Free tier (1500 requests/day)
- Speech APIs: Built into browser (unlimited)

## 📚 Full Documentation
- README.md - Complete documentation
- walkthrough.md - Detailed walkthrough
- QUICKSTART.md - Quick reference

## ❓ Issues?

**"GOOGLE_API_KEY not set"**
→ Edit backend/.env and add your key

**"Speech recognition not supported"**
→ Use Chrome or Edge

**"Microphone access denied"**
→ Allow permissions in browser settings

---

**That's it! You're ready to go! 🎉**
