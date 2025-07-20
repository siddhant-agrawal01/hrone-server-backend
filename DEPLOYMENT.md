# Vercel Deployment Guide

## 🚀 Deploy to Vercel

### Prerequisites

1. [Vercel CLI](https://vercel.com/cli) installed: `npm i -g vercel`
2. MongoDB Atlas account with connection string
3. GitHub repository (recommended)

### Step 1: Environment Variables

Set up your environment variables in Vercel:

```bash
# Using Vercel CLI
vercel env add mongodb_url
# Enter your MongoDB Atlas connection string when prompted

vercel env add database_name
# Enter your database name (e.g., ecommerce_db)
```

Or through Vercel Dashboard:

1. Go to your project settings
2. Navigate to Environment Variables
3. Add:
   - `mongodb_url`: Your MongoDB Atlas connection string
   - `database_name`: Your database name

### Step 2: Deploy

```bash
# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### Step 3: Test Deployment

Your API will be available at: `https://your-project-name.vercel.app`

Test endpoints:

- Health check: `GET https://your-project-name.vercel.app/health`
- API docs: `https://your-project-name.vercel.app/docs`

## 🔧 Configuration Details

### MongoDB Connection Settings

- **Server Selection Timeout**: 30 seconds
- **Connect Timeout**: 30 seconds
- **Socket Timeout**: 30 seconds
- **Max Pool Size**: 10 connections
- **Retry Writes/Reads**: Enabled

### Function Settings

- **Max Duration**: 30 seconds
- **Region**: US East (iad1)
- **Runtime**: Python 3.9+

## 🐛 Troubleshooting

### Common Issues:

1. **MongoDB Connection Timeout**: Check your Atlas IP whitelist (0.0.0.0/0 for Vercel)
2. **Function Timeout**: Increase maxDuration in vercel.json
3. **Cold Start**: First request may be slower (normal)

### Monitoring:

- Check Vercel Function logs
- Monitor MongoDB Atlas metrics
- Use health check endpoint for uptime monitoring
