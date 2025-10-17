# AI Crew for Stock Analysis
## Introduction
This project is an example using the CrewAI framework to automate the process of analyzing a stock. CrewAI orchestrates autonomous AI agents, enabling them to collaborate and execute complex tasks efficiently.

By [@joaomdmoura](https://x.com/joaomdmoura)

- [AI Crew for Stock Analysis](#ai-crew-for-stock-analysis)
  - [Introduction](#introduction)
  - [CrewAI Framework](#crewai-framework)
  - [Running the Script](#running-the-script)
  - [Details \& Explanation](#details--explanation)
  - [Jaeger Tracing](#jaeger-tracing)
    - [Running Jaeger Locally](#running-jaeger-locally)
    - [Viewing Traces](#viewing-traces)
  - [Using Different Models](#using-different-models)
    - [Using Different Claude Models](#using-different-claude-models)
    - [Cost Considerations](#cost-considerations)
  - [License](#license)

## CrewAI Framework
CrewAI is designed to facilitate the collaboration of role-playing AI agents. In this example, these agents work together to give a complete stock analysis and investment recommendation

## Running the Script
This project uses AWS Bedrock with Claude models by default.

***Disclaimer:** This will use AWS Bedrock which will cost you money based on token usage.*

- **Configure Environment**: Copy `.env.example` to `.env` and set up the environment variables:
  - AWS credentials: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
  - Model selection: `AWS_BEDROCK_MODEL` (default: Claude Sonnet 4.5)
  - [SEC-API](https://sec-api.io) key: `SEC_API_API_KEY`
  - Tracing: `CREWAI_TRACING_ENABLED=true` (for Jaeger tracing)
- **Install Dependencies**: Run `uv sync` (includes OpenTelemetry packages for Jaeger tracing).
- **Execute the Script**: Run `uv run stock_analysis` or `uv run python src/stock_analysis/main.py`.

## Details & Explanation
- **Running the Script**: Execute `uv run python src/stock_analysis/main.py` and input the stock ticker to be analyzed when prompted. The script will leverage the CrewAI framework to analyze the company and generate a detailed report.
- **Key Components**:
  - `src/stock_analysis/main.py`: Main script file.
  - `src/stock_analysis/crew.py`: Crew definition with agents and tasks.
  - `src/stock_analysis/config/`: Configuration files for agents and tasks.
  - `src/stock_analysis/tools/`: Contains tool classes used by the agents.

## Jaeger Tracing

This project is configured to export OpenTelemetry traces to Jaeger for observability and debugging.

### Running Jaeger Locally

Start Jaeger using Docker:

```bash
docker run -d --name jaeger \
  -p 4317:4317 \
  -p 16686:16686 \
  jaegertracing/all-in-one:latest
```

This exposes:
- **Port 4317**: OTLP gRPC endpoint (for receiving traces)
- **Port 16686**: Jaeger UI (for viewing traces)

### Viewing Traces

1. Run the stock analysis: `uv run python src/stock_analysis/main.py`
2. Open the Jaeger UI: http://localhost:16686
3. Select service: `stock-analysis-crew`
4. Click "Find Traces" to view the execution flow

## Using Different Models

This project is configured to use AWS Bedrock with Claude models. The LLM configuration is in `src/stock_analysis/crew.py`.

### Using Different Claude Models

To use a different Claude model, update the `AWS_BEDROCK_MODEL` environment variable in your `.env` file:

```bash
# Claude Sonnet 4.5 (default - most capable)
AWS_BEDROCK_MODEL=us.anthropic.claude-sonnet-4-5-20250929-v1:0

# Claude Haiku 4.5 (faster and cheaper)
AWS_BEDROCK_MODEL=us.anthropic.claude-haiku-4-5-20251001-v1:0

# Claude 3.5 Sonnet (previous generation)
AWS_BEDROCK_MODEL=anthropic.claude-3-5-sonnet-20240620-v1:0
```

### Cost Considerations

AWS Bedrock pricing varies by model:
- **Claude Sonnet 4.5**: ~$3/M input tokens, ~$15/M output tokens
- **Claude Haiku 4.5**: ~$0.80/M input tokens, ~$4/M output tokens

For development and testing, Claude Haiku 4.5 offers a good balance of performance and cost.

## License
This project is released under the MIT License.
