import yfinance as yf
from langchain_core.prompts import PromptTemplate
from langchain.agents import tool, AgentExecutor, create_react_agent
from langchain_google_vertexai import ChatVertexAI, VectorSearchVectorStore
import os
import multiprocessing
# This environment variable is a fallback, good to keep it.
os.environ['GRPC_GCP_DISABLE_GCP_CLIENT_CHANNEL'] = '1'


# --- CONFIGURATION ---
# Ensure these values are correct
PROJECT_ID = "stonkbot007"
REGION = "asia-south1"
GCS_BUCKET_NAME = "stonkbot007"
INDEX_ID = "projects/stonkbot007/locations/asia-south1/indexes/680870376477032448"
ENDPOINT_ID = "3144444925764960256"
DEPLOYED_INDEX_ID = "stonkbot007"
# ---------------------

# --- 1. DEFINE TOOLS ---

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
    """Searches the market news database for relevant articles about a specific company, stock ticker, or economic topic."""
    print(f"INFO: Searching news database for '{query}'...")
    results = retriever.invoke(query)
    return "\n".join([f"Article: {doc.page_content}\n" for doc in results])


@tool
def get_stock_data(ticker: str) -> str:
    """Fetches the current price and key metrics for a given stock ticker from Yahoo Finance."""
    print(f"INFO: Fetching stock data for '{ticker}'...")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice', 'N/A')
        return f"Current Price of {ticker}: {price}"
    except Exception as e:
        return f"Could not fetch data for ticker {ticker}. Error: {e}"

# --- 2. DEFINE PROMPT ---


prompt_template = """
You are FinAI, an expert AI financial analyst. Your goal is to provide insightful, news-driven analysis of a user's stock portfolio.

ALWAYS start with this disclaimer:
"**Disclaimer:** I am an AI assistant. This is a simulated financial analysis and should not be considered real financial advice."

Workflow:
1. For each stock, use `search_market_news` to find recent news.
2. Then, use `get_stock_data` to get its latest price. Use the '.NS' suffix for Indian stocks (e.g., 'RELIANCE.NS').
3. After gathering all data, synthesize your findings into a final answer, providing a brief analysis for each stock and a portfolio summary.

Begin!

User's Portfolio: {input}
Thought: I need to analyze the user's portfolio. I will start with the first stock.
{agent_scratchpad}
"""
PROMPT = PromptTemplate.from_template(prompt_template)

# --- 3. CREATE AGENT ---


def create_financial_agent():
    """Initializes the LangChain agent executor."""
    llm = ChatVertexAI(model_name="gemini-pro",
                       temperature=0, project=PROJECT_ID)
    tools = [search_market_news, get_stock_data]
    agent = create_react_agent(llm, tools, PROMPT)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# --- 4. MAIN FUNCTION ---


def run_financial_agent(user_input: str):
    """The main function to run the financial agent."""
    print("Initializing agent...")
    financial_agent = create_financial_agent()
    print("Agent initialized. Invoking with user input...")
    try:
        response = financial_agent.invoke({"input": user_input})
        return response["output"]
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    # ------------------------------------------------------------------
    # THIS IS THE CRITICAL FIX
    # It MUST be the first thing inside the `if __name__ == "__main__":` block.
    # This forces Python to use a safer method for creating background processes, preventing the deadlock.
    multiprocessing.set_start_method('spawn', force=True)
    # ------------------------------------------------------------------

    example_portfolio = "Two stocks: 10 shares of Reliance Industries (RELIANCE.NS) and 5 shares of HDFC Bank (HDFCBANK.NS)"

    final_analysis = run_financial_agent(example_portfolio)

    print("\n--- FINAL ANALYSIS ---")
    print(final_analysis)
