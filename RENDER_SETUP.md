# Render Deployment Setup Guide

## Required Environment Variables

Set these environment variables in your Render dashboard:

### 1. SENDGRID_API_KEY
- **Value**: Your SendGrid API key (starts with `SG.`)
- **Description**: Your SendGrid API key for sending emails
- **Note**: Get this from your SendGrid dashboard under Settings > API Keys

### 2. MAIL_DEFAULT_SENDER
- **Value**: Your verified SendGrid sender email address
- **Description**: The email address that will appear as the sender
- **Example**: `noreply@yourdomain.com` or your verified email in SendGrid

### 3. GEMINI_API_KEY
- **Value**: Your Google Gemini API key
- **Description**: Required for AI-powered interview questions and scoring

## How to Set Environment Variables in Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on your web service (`interview-platform`)
3. Navigate to **Environment** tab
4. Click **Add Environment Variable**
5. Enter the **Key** and **Value** for each variable above
6. Click **Save Changes**
7. Render will automatically redeploy your service

## Verification

After setting the environment variables, check the logs to ensure:
- No `SENDGRID_API_KEY environment variable is not set` errors
- No `MAIL_DEFAULT_SENDER environment variable is not set` errors
- Email sending works correctly

## Notes

- The `sync: false` setting in `render.yaml` means these variables must be set manually in the Render dashboard
- Never commit API keys or secrets to Git (they are automatically blocked by GitHub)
- Always use environment variables for sensitive configuration

