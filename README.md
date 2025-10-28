## Live link

Vercel: https://binance-proj.vercel.app/

Netlify: https://binancefrontend.netlify.app/

## Setup Steps

---

Step 1: Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

---

Step 2: Install required dependencies
```python
pip install -r requirements.txt
```

---

Step 3: Run backend server
```bash
uvicorn main:app --port 8000
```

Websocker server will be running at `ws://localhost:8000/ws`

---

Step 4: Get into ./client_ui, modify the WEBSOCKET_URL in TraderTicker.jsx component to `ws://localhost:8000/ws`, and then run:
```bash
npm run dev
```

---

App will be available at `http://localhost:5173`

---