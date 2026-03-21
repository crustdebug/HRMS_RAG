# Gemini Free Tier Models

This chatbot uses Google's Gemini free tier models with automatic fallback.

## Available Models (in priority order):

### 1. gemini-2.5-flash-lite (Primary)
- **Rate Limit**: 15 requests per minute (RPM)
- **Daily Limit**: 1,000 requests per day (RPD)
- **Best for**: High-volume demos and testing
- **Speed**: Fastest
- **Use case**: Default model for most queries

### 2. gemini-2.5-flash (Fallback 1)
- **Rate Limit**: 10 RPM
- **Daily Limit**: 250 RPD
- **Best for**: Balanced performance
- **Speed**: Fast
- **Use case**: When lite model is rate-limited

### 3. gemini-2.5-pro (Fallback 2)
- **Rate Limit**: 2 RPM
- **Daily Limit**: 50-100 RPD
- **Best for**: Complex queries requiring more reasoning
- **Speed**: Slower but more capable
- **Use case**: Last resort when other models fail

## Shared Limits:
- **Token Limit**: 250,000 tokens per minute (TPM) across all models
- **Context Window**: 1 million tokens

## How Fallback Works:
1. System tries `gemini-2.5-flash-lite` first
2. If it fails (rate limit, error, etc.), automatically switches to `gemini-2.5-flash`
3. If that fails, tries `gemini-2.5-pro`
4. Only returns error if all three models fail

## Note:
Gemini 3.0 Pro and 3.1 Pro are NOT available in the free tier and are excluded from this implementation.
