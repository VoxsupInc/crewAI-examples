# Jaeger Tracing Setup

This document explains the OpenTelemetry tracing configuration for the stock analysis project.

## Overview

The project is configured to export traces to Jaeger using OpenTelemetry (OTEL) with CrewAI instrumentation. This provides visibility into:
- Agent execution flow
- Task completion times
- Tool usage and performance
- LLM API calls
- Error tracking and debugging

**Required Package**: The project uses `openinference-instrumentation-crewai` to properly instrument CrewAI for tracing. This package is automatically installed with the project dependencies.

## Quick Start

### 1. Start Jaeger

Run Jaeger locally using Docker:

```bash
docker run -d --name jaeger \
  -p 4317:4317 \
  -p 16686:16686 \
  jaegertracing/all-in-one:latest
```

**Ports:**
- `4317`: OTLP gRPC endpoint (receives traces)
- `16686`: Jaeger UI (web interface)

### 2. Verify Jaeger is Running

Open http://localhost:16686 in your browser. You should see the Jaeger UI.

### 3. Run the Stock Analysis

```bash
cd /Users/jamesliu/git/crewAI-examples/crews/stock_analysis
uv run python src/stock_analysis/main.py
```

### 4. View Traces

1. Go to http://localhost:16686
2. In the "Service" dropdown, select `stock-analysis-crew`
3. Click "Find Traces"
4. Click on any trace to see detailed execution information

## Configuration

Tracing is configured via environment variables in `.env`:

```bash
# Enable CrewAI tracing
CREWAI_TRACING_ENABLED=true

# OpenTelemetry configuration
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_SERVICE_NAME=stock-analysis-crew
```

## What Gets Traced

With tracing enabled, you can observe:

1. **Crew Execution**
   - Overall crew run duration
   - Task sequence and dependencies

2. **Agent Activities**
   - Agent initialization
   - Task assignments
   - Decision-making process

3. **Tool Usage**
   - SEC filing fetches
   - Web scraping operations
   - Calculator invocations

4. **LLM Calls**
   - Bedrock API requests
   - Token usage
   - Response times

## Disabling Tracing

To disable tracing (useful for production or to reduce overhead):

1. Set in `.env`:
   ```bash
   CREWAI_TRACING_ENABLED=false
   ```

2. Or remove the OTEL configuration variables

## Troubleshooting

### Traces Not Appearing

1. **Check Jaeger is running:**
   ```bash
   curl http://localhost:16686
   ```

2. **Verify OTEL endpoint is accessible:**
   ```bash
   curl http://localhost:4317
   ```

3. **Check environment variables are loaded:**
   ```bash
   cat .env | grep OTEL
   ```

4. **Look for OTEL errors in console output**

### Jaeger Connection Issues

If you see OTEL connection errors:

1. Ensure Jaeger container is running:
   ```bash
   docker ps | grep jaeger
   ```

2. Restart Jaeger if needed:
   ```bash
   docker restart jaeger
   ```

3. Check Docker logs:
   ```bash
   docker logs jaeger
   ```

## Advanced Configuration

### Custom Service Name

To distinguish between different environments:

```bash
# Development
OTEL_SERVICE_NAME=stock-analysis-dev

# Production
OTEL_SERVICE_NAME=stock-analysis-prod
```

### Remote Jaeger Instance

To send traces to a remote Jaeger instance:

```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://your-jaeger-host:4317
```

### Sampling

To reduce trace volume in production, you can configure sampling (if supported by CrewAI):

```bash
OTEL_TRACES_SAMPLER=parentbased_traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1  # Sample 10% of traces
```

## Benefits of Tracing

1. **Performance Analysis**: Identify slow operations and bottlenecks
2. **Debugging**: Understand agent decision flows when troubleshooting
3. **Optimization**: Find opportunities to improve task efficiency
4. **Monitoring**: Track system behavior in production
5. **Cost Analysis**: See which LLM calls consume the most tokens

## Learn More

- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [CrewAI Observability](https://docs.crewai.com/)

