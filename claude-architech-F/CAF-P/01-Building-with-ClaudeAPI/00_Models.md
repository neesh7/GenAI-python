# Claude Model Family

## Overview

| Model | Model ID | Capability | Speed | Cost | Context | Best For | Default |
|---|---|---|---|---|---|---|---|
| **Opus 4.7** | `claude-opus-4-7` | Highest | Slowest | Premium | 200K | Complex reasoning, accuracy critical | ❌ |
| **Sonnet 4.6** | `claude-sonnet-4-6` | Balanced | Fast | Standard | 200K | General purpose, Claude Code, APIs | ✅ |
| **Haiku 4.5** | `claude-haiku-4-5-20251001` | Fast | Fastest | Lowest | 200K | Speed/cost critical, simple tasks | ❌ |

## Key Points

- **All models** support: Caching, Extended Thinking, Batch Processing, Vision, Files API, Tool Use
- **Default recommendation**: Use **Sonnet 4.6** for most use cases
- **Upgrade to Opus** if results are insufficient
- **Downgrade to Haiku** if you need speed and cost optimization
- **200K token context window** available across all models
