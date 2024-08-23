import streamlit as st
import openai
import yfinance as yf


openai.api_key = st.secrets["OPEN_API_KEY"]


st.title('Interactive Financial Stock Market Comparative Analysis Tool')

# Function to fetch stock data
def get_stock_data(ticker, start_date='2024-01-01', end_date='2024-02-01'):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Sidebar for user inputs
st.sidebar.header('User Input Options')
selected_stock = st.sidebar.text_input('Enter Stock Ticker 1', 'AAPL').upper()
selected_stock2 = st.sidebar.text_input('Enter Stock Ticker 2', 'GOOGL').upper()

# Fetch stock data
stock_data = get_stock_data(selected_stock)
stock_data2 = get_stock_data(selected_stock2)

# Create two columns for displaying data and charts
col1, col2 = st.columns(2)

# Display stock data and charts for the first and second stock
with col1:
    st.subheader(f"Displaying data for: {selected_stock}")
    st.write(stock_data)
    chart_type = st.selectbox(f'Select Chart Type for {selected_stock}', ['Line', 'Bar'], key='chart1')
    if chart_type == 'Line':
        st.line_chart(stock_data['Close'])
    elif chart_type == 'Bar':
        st.bar_chart(stock_data['Close'])


with col2:
    st.subheader(f"Displaying data for: {selected_stock2}")
    st.write(stock_data2)
    chart_type2 = st.selectbox(f'Select Chart Type for {selected_stock2}', ['Line', 'Bar'], key='chart2')
    if chart_type2 == 'Line':
        st.line_chart(stock_data2['Close'])
    elif chart_type2 == 'Bar':
        st.bar_chart(stock_data2['Close'])

# Button to perform comparative performance analysis
if st.button('Comparative Performance'):
    # Prepare the content for the OpenAI request
    stock_data_str = stock_data.head().to_string()
    stock_data2_str = stock_data2.head().to_string()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial assistant that will retrieve two tables of financial market data and summarize the comparative performance in detail, highlighting key points for each stock and providing a conclusion in markdown format."},
                {"role": "user", "content": f"Stock data for {selected_stock}:\n{stock_data_str}\n\nStock data for {selected_stock2}:\n{stock_data2_str}"}
            ]
        )
        st.markdown(response.choices[0].message['content'])
    except openai.error.RateLimitError:
        st.error("Rate limit exceeded. Please try again later.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
