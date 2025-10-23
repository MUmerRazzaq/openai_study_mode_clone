# Hugging Face Spaces Setup Guide

## Why Your Space is Restarting Repeatedly

If your Space is restarting every 1-2 seconds, it means the container is **crashing immediately on startup**. This creates a crash loop where Hugging Face keeps trying to restart it.

### Most Common Causes:

1. **Missing Environment Variables** ❌

   - Your app needs `GEMINI_API_KEY` and `LLM_CHAT_COMPLETION_URL`
   - If these aren't set, the app crashes during import
   - Container restarts → crashes again → infinite loop

2. **Import Errors** ❌

   - Missing dependencies
   - Python version mismatch
   - Module not found errors

3. **Port Issues** ❌
   - App not listening on the correct port (7860)

## Required Environment Variables

Go to your Space Settings → **Variables and secrets** and add:

### Required:

```
GEMINI_API_KEY = your-gemini-api-key-here
LLM_CHAT_COMPLETION_URL = https://generativelanguage.googleapis.com/v1beta/openai/
```

### Optional:

```
LLM_MODEL = gemini-2.0-flash
CHAINLIT_URL = https://your-space-name.hf.space
```

## How to Debug

### 1. Check Container Logs

- Go to your Space
- Click on "Logs" tab
- Look for the LAST error before restart
- You'll see lines like:
  ```
  ==========================================
  STARTUP FAILED: Failed to initialize LLM client/model: GEMINI_API_KEY environment variable not set.
  ==========================================
  ```

### 2. Common Error Messages

#### "GEMINI_API_KEY environment variable not set"

**Solution:** Add the environment variable in Space secrets (see above)

#### "No module named 'openai_study_mode_clone'"

**Solution:** Check Dockerfile has `RUN pip install -e .` after copying files

#### "Address already in use" or port errors

**Solution:** Ensure README.md has `app_port: 7860` in frontmatter

#### "Session is disconnected" (after successful startup)

**Solution:** This is a reverse proxy issue, not a crash. The app is running but needs:

- `ENV FORWARDED_ALLOW_IPS="*"` in Dockerfile (already added)
- No `-h` flag in Chainlit command (already fixed)

### 3. Verify Dockerfile

Your Dockerfile should have:

```dockerfile
# Install the project package
RUN pip install -e .

# Trust reverse proxy headers
ENV FORWARDED_ALLOW_IPS="*"

# Start app on port 7860
CMD ["chainlit", "run", "src/openai_study_mode_clone/app.py", "--host", "0.0.0.0", "--port", "7860"]
```

### 4. Verify README.md Frontmatter

```yaml
---
title: Study Mode
emoji: 📚
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---
```

## Startup Sequence (When Working Correctly)

You should see these logs in order:

```
==========================================
STARTUP: Initializing LLM client and model...
==========================================
LLM client initialized with base_url: https://generativelanguage.googleapis.com/v1beta/openai/
LLM model initialized: gemini-2.0-flash
==========================================
STARTUP: LLM client and model initialized successfully
==========================================
CHAINLIT APP: Starting up...
==========================================
Your app is available at http://0.0.0.0:7860
```

## Still Having Issues?

### Check These:

1. **Are secrets visible to the Space?**

   - In Space settings, secrets should be marked as "Available"
   - Try deleting and re-adding them

2. **Is the Space using the latest build?**

   - After changing Dockerfile or code, Space needs to rebuild
   - Check "Building" status in Space header

3. **Python version compatibility?**

   - Dockerfile uses Python 3.13-slim
   - Some packages might not be compatible
   - Try changing to `python:3.11-slim` if issues persist

4. **Memory issues?**
   - Free tier has limited RAM
   - Check if container is being OOM killed
   - Consider upgrading Space hardware

## Testing Locally

Before deploying to Spaces, test locally:

```cmd
docker build -t studybuddy .
docker run -p 7860:7860 ^
  -e GEMINI_API_KEY=your-key ^
  -e LLM_CHAT_COMPLETION_URL=https://generativelanguage.googleapis.com/v1beta/openai/ ^
  studybuddy
```

Visit http://localhost:7860 and verify:

- No crash loops
- Logs show successful startup
- UI loads properly

## Quick Checklist

- [ ] GEMINI_API_KEY set in Space secrets
- [ ] LLM_CHAT_COMPLETION_URL set in Space secrets
- [ ] README.md has `app_port: 7860` in frontmatter
- [ ] README.md has `sdk: docker` in frontmatter
- [ ] Dockerfile has `RUN pip install -e .`
- [ ] Dockerfile has `ENV FORWARDED_ALLOW_IPS="*"`
- [ ] Dockerfile CMD uses port 7860
- [ ] No `-h` flag in Chainlit command
- [ ] Space has rebuilt after code changes
- [ ] Container logs show successful startup (not crash loop)

## Support

If you're still stuck:

1. Copy the FULL container logs
2. Check which error appears LAST before restart
3. Look for the "STARTUP FAILED" message
4. Verify all environment variables are set correctly
