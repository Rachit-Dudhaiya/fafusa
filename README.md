# STOP! Word Party Game

A fast-paced, real-time vocabulary game where players race to find words starting with a specific letter across multiple categories!

## 🚀 How to Play Locally

1. Ensure you have Python installed.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python server.py
   ```
4. Open your browser and go to `http://localhost:8090` to play!

## 🌍 How to Host Online (Free)

To let your friends play from anywhere, the easiest way to host this for free is using **Render.com**.

### Step 1: Upload to GitHub
Upload this entire folder (`index.html`, `server.py`, `requirements.txt`) to a new public repository on GitHub.
*You can drag and drop these files directly into GitHub in your browser if you don't have Git installed.*

### Step 2: Deploy Backend to Render
1. Go to [Render.com](https://render.com) and sign up.
2. Click **New +** and select **Web Service**.
3. Connect your GitHub account and select your repository.
4. Set the following configuration:
   - **Name**: stop-game-backend (or whatever you want)
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
5. Click **Create Web Service**. 
6. Once deployed, Render will give you a URL (e.g., `https://stop-game.onrender.com`).

### Step 3: Connect Frontend
1. Open your `index.html` file.
2. Look around line 1395 for `// Example: wsUrl = 'wss://my-stop-game-server.onrender.com';`.
3. Change the `wsUrl` on the next line to point to your new Render Web Service URL, replacing `https://` with `wss://`.
   *(Example: `wsUrl = 'wss://stop-game.onrender.com';`)*
4. Commit/Save the change to GitHub.

### Step 4: Deploy Frontend (Optional but Recommended)
For best performance, host your `index.html` on **GitHub Pages**, **Vercel**, or **Netlify**:
1. On GitHub, go to your repository **Settings** > **Pages**.
2. Select the `main` branch and click **Save**.
3. Wait a minute, and GitHub will give you a public URL (e.g., `https://your-username.github.io/stop-game/`).
4. Share that link with your friends to play!
