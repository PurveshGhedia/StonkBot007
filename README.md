# StonkBot007 - Portfolio Scanner Frontend

A comprehensive web-based portfolio scanning and analysis platform that provides real-time insights on your stock holdings based on news sentiment analysis.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Application
```bash
python start_portfolio_scanner.py
```

The application will automatically:
- Start the API server on `http://localhost:5000`
- Open your web browser to the frontend interface
- Display login credentials and usage instructions

### 3. Login and Use
- **Username**: `priya`, `rohan`, or `ananya`
- **Password**: `password123`

## 🌟 Features

### 🔐 Secure Authentication
- Multi-user login system with demo accounts
- Secure session management
- Personalized portfolio views

### 📊 Portfolio Management
- View your stock holdings with share counts
- Real-time portfolio summary statistics
- Interactive portfolio display

### 🔍 Advanced Portfolio Scanning
- **News Analysis**: Scans 100+ financial news articles
- **Stock Detection**: Identifies 100+ major Indian companies
- **Sentiment Analysis**: Analyzes positive/negative sentiment
- **Confidence Scoring**: Provides accuracy metrics

### 📈 Investment Insights
- **Recommendations**: BUY/SELL/HOLD with detailed reasoning
- **Risk Assessment**: Conservative, Moderate, or Aggressive risk levels
- **Price Outlook**: Bullish, Bearish, or Neutral expectations
- **Action Items**: Specific steps for investors

### 📰 News Integration
- Recent financial news with sentiment analysis
- Real-time news updates
- News sentiment scoring

## 🏗️ Architecture

### Frontend (`frontend_portfolio_scanner.html`)
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Clean, professional interface with animations
- **Real-time Updates**: Live portfolio analysis and news
- **Interactive Charts**: Visual representation of data

### Backend API (`api_server.py`)
- **Flask Server**: RESTful API endpoints
- **CORS Enabled**: Cross-origin resource sharing
- **Background Processing**: Asynchronous analysis
- **Error Handling**: Robust error management

### Core Components
- **Portfolio Scanner**: Main analysis orchestrator
- **Stock Extractor**: Symbol and company name recognition
- **Sentiment Analyzer**: News sentiment analysis
- **Insights Generator**: Investment recommendations

## 📡 API Endpoints

### Authentication & Portfolio
- `GET /` - Serve frontend interface
- `POST /api/scan-portfolio` - Scan portfolio stocks
- `GET /api/analysis-status/<id>` - Get analysis status

### Analysis & News
- `POST /api/analyze-stocks` - Analyze specific stocks
- `GET /api/news` - Get recent financial news
- `GET /api/health` - Health check

## 🎯 Demo Portfolios

### Priya Sharma
- **Focus**: Large-cap Indian stocks
- **Holdings**: RELIANCE, TCS, HDFC, INFOSYS, ICICI, KOTAK, ITC, BHARTIARTL, SUNPHARMA, TATAMOTORS

### Rohan Kapoor
- **Focus**: Diversified portfolio
- **Holdings**: RELIANCE, TCS, HDFC, INFOSYS, ICICI, KOTAK, ITC, BHARTIARTL, SUNPHARMA, TATAMOTORS, HINDUNILVR, ASIANPAINT

### Ananya Reddy
- **Focus**: Growth-oriented stocks
- **Holdings**: RELIANCE, TCS, HDFC, INFOSYS, ICICI, KOTAK, ITC, BHARTIARTL, SUNPHARMA, TATAMOTORS, HINDUNILVR, ASIANPAINT, MARUTI, TITAN

## 🔧 Configuration

### Environment Variables
- `NEWS_API_KEY`: Your NewsAPI key (configured in `config.py`)
- `FLASK_ENV`: Set to `development` for debug mode

### Customization
- **Portfolio Data**: Edit user portfolios in `api_server.py`
- **Analysis Parameters**: Modify in `portfolio_scanner.py`
- **UI Styling**: Update CSS in `frontend_portfolio_scanner.html`

## 📊 Sample Analysis Output

### Portfolio Overview
```
Portfolio Sentiment: POSITIVE
Total Stocks Analyzed: 10
Positive Stocks: 4
Negative Stocks: 2
Neutral Stocks: 4
```

### Individual Stock Analysis
```
RELIANCE - Reliance Industries
Sentiment: POSITIVE (Confidence: 0.85)
Recommendation: BUY - Strong positive sentiment with high confidence
Risk Level: MEDIUM
Price Outlook: Bullish - Strong positive momentum expected
Key Factors: Strong earnings, Market growth, Sector expansion
Action Items: Consider adding to portfolio, Set stop-loss at 5-10%
```

## 🛠️ Development

### Running in Development Mode
```bash
# Start API server
python api_server.py

# Open frontend in browser
open http://localhost:5000
```

### Adding New Features
1. **New Analysis Types**: Extend `insights_generator.py`
2. **Additional Data Sources**: Modify `news_fetcher.py`
3. **UI Components**: Update `frontend_portfolio_scanner.html`
4. **API Endpoints**: Add routes in `api_server.py`

## 🔒 Security Features

- **Input Validation**: All user inputs are validated
- **Error Handling**: Comprehensive error management
- **CORS Protection**: Configured for secure cross-origin requests
- **Session Management**: Secure user session handling

## 📱 Mobile Responsiveness

The frontend is fully responsive and optimized for:
- **Desktop**: Full-featured interface
- **Tablet**: Adapted layout for touch interaction
- **Mobile**: Streamlined interface for small screens

## 🚨 Troubleshooting

### Common Issues

1. **Port 5000 Already in Use**
   ```bash
   # Kill process using port 5000
   lsof -ti:5000 | xargs kill -9
   ```

2. **Module Not Found Errors**
   ```bash
   # Install missing dependencies
   pip install -r requirements.txt
   ```

3. **API Connection Issues**
   - Check if `api_server.py` is running
   - Verify NewsAPI key in `config.py`
   - Check internet connection

4. **Frontend Not Loading**
   - Clear browser cache
   - Check browser console for errors
   - Verify server is running on correct port

## 📈 Performance Optimization

- **Caching**: Analysis results are cached for faster access
- **Background Processing**: Long-running tasks run asynchronously
- **Lazy Loading**: UI components load on demand
- **Efficient Queries**: Optimized database queries (when implemented)

## 🔮 Future Enhancements

- **Real-time Data**: Live stock price integration
- **Advanced Analytics**: Technical analysis indicators
- **Portfolio Optimization**: AI-powered portfolio suggestions
- **Mobile App**: Native mobile application
- **Database Integration**: Persistent data storage
- **User Management**: Advanced user authentication
- **API Rate Limiting**: Enhanced security and performance

## 📞 Support

For issues, questions, or feature requests:
1. Check the troubleshooting section
2. Review the API documentation
3. Examine the source code comments
4. Create an issue in the repository

## ⚠️ Disclaimer

This tool is for educational and informational purposes only. The analysis is based on news sentiment and should not be considered as financial advice. Please consult with a qualified financial advisor before making investment decisions.

---

**StonkBot007 Portfolio Scanner** - Making investment analysis accessible and intelligent! 🚀📊
