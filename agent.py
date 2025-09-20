import os
from langchain_google_vertexai import ChatVertexAI, VectorSearchVectorStore
from langchain.agents import tool, AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
import yfinance as yf

# --- CONFIGURATION ---
# IMPORTANT: Fill in these values from your Google Cloud project.
# Before running, authenticate with gcloud: gcloud auth application-default login

PROJECT_ID = "your-gcp-project-id"
REGION = "asia-south1"  # e.g., "asia-south1" for Mumbai
GCS_BUCKET_NAME = "aivest-hackathon-bucket"

# Get these from the Vertex AI -> Vector Search console
# The numeric ID of the index
INDEX_ID = "projects/131196170322/locations/asia-south1/indexEndpoints/3144444925764960256"
ENDPOINT_ID = "3144444925764960256"  # The numeric ID of the endpoint

# When you deploy your index to an endpoint, you give that deployment an ID.
# The ID of the DEPLOYED index on the endpoint
DEPLOYED_INDEX_ID = "stonkbot007"
# ---------------------

# --- 1. DEFINE THE TOOLS THE AGENT CAN USE ---

# Tool to search your news database (Vertex AI Vector Search)
vector_store = VectorSearchVectorStore.from_components(
    project_id=PROJECT_ID,
    region=REGION,
    gcs_bucket_name=GCS_BUCKET_NAME,
    index_id=INDEX_ID,
    endpoint_id=ENDPOINT_ID,
    deployed_index_id=DEPLOYED_INDEX_ID,
)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})


@tool
def search_market_news(query: str) -> str:
    """
    Searches the market news database for relevant articles about a specific company,
    stock ticker, or economic topic. Use this to find the latest news and sentiment.
    """
    print(f"INFO: Searching news database for '{query}'...")
    results = retriever.invoke(query)
    return "\n".join([f"Article: {doc.page_content}\n" for doc in results])

# Tool to get live stock data


@tool
def get_stock_data(ticker: str) -> str:
    """
    Fetches the current price and key metrics for a given stock ticker from Yahoo Finance.
    Use this for real-time price information. Tickers for Indian stocks end in '.NS'.
    """
    print(f"INFO: Fetching stock data for '{ticker}'...")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice', 'N/A')
        prev_close = info.get('previousClose', 'N/A')
        market_cap = info.get('marketCap', 'N/A')
        return (f"Data for {ticker}:\n"
                f"- Current Price: {price}\n"
                f"- Previous Close: {prev_close}\n"
                f"- Market Cap: {market_cap}\n")
    except Exception as e:
        return f"Could not fetch data for ticker {ticker}. Error: {e}"

# --- 2. DEFINE THE AGENT'S PROMPT & PERSONALITY ---


# This prompt template guides the agent's reasoning process.
prompt_template = """
You are FinAI, an expert AI financial analyst designed for a hackathon project. Your goal is to provide insightful, news-driven analysis of a user's stock portfolio.

ALWAYS start your response with the following disclaimer, and nothing else before it:
"**Disclaimer:** I am an AI assistant. This is a simulated financial analysis for a hackathon project and should not be considered real financial advice."

When given a portfolio, your workflow is as follows:
1.  Acknowledge the portfolio and list the stocks you will analyze.
2.  For each stock in the portfolio, you MUST use your tools in this sequence:
    a. First, use the `search_market_news` tool to find recent news related to the company or its industry.
    b. Second, use the `get_stock_data` tool to get its latest market price. Use the '.NS' suffix for Indian stocks (e.g., 'RELIANCE.NS').
3.  After gathering data for all stocks, synthesize your findings into a coherent final answer.
4.  For each stock, provide a brief "Analysis" section that connects the news to the stock's potential performance.
5.  Conclude with a "Portfolio Summary" that gives an overall outlook.

Format your final output using Markdown for readability.

Begin!

User's Portfolio: {input}
Thought: I need to analyze the user's portfolio by fetching news and stock data for each holding. I will start with the first stock.
{agent_scratchpad}
"""

PROMPT = PromptTemplate.from_template(prompt_template)

# --- 3. CREATE THE AGENT AND THE EXECUTOR ---


def create_financial_agent():
    """Initializes and returns the LangChain agent executor."""
    llm = ChatVertexAI(model_name="gemini-pro",
                       temperature=0, project=PROJECT_ID)
    tools = [search_market_news, get_stock_data]
    agent = create_react_agent(llm, tools, PROMPT)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    return agent_executor

# --- 4. MAIN FUNCTION TO BE CALLED BY THE UI ---


def run_financial_agent(user_input: str):
    """
    The main function to run the financial agent.
    This will be called by the Streamlit app.
    """
    print("Initializing agent...")
    financial_agent = create_financial_agent()
    print("Agent initialized. Invoking with user input...")
    try:
        response = financial_agent.invoke({"input": user_input})
        return response["output"]
    except Exception as e:
        print(f"ERROR: An error occurred during agent execution: {e}")
        return ("**Disclaimer:** I am an AI assistant. This is a simulated financial analysis for a hackathon project and should not be considered real financial advice.\n\n"
                "I'm sorry, but I encountered an error while processing your request. Please try again.")


# Example of how to run this script directly for testing
if __name__ == "__main__":
    # Example portfolio. Use tickers with .NS for National Stock Exchange of India.
    example_portfolio = "Two stocks: 10 shares of Reliance Industries (RELIANCE.NS) and 5 shares of HDFC Bank (HDFCBANK.NS)"

    final_analysis = run_financial_agent(example_portfolio)

    print("\n--- FINAL ANALYSIS ---")
    print(final_analysis)
