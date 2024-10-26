from flask import Flask, render_template, request, jsonify
import stock_prediction as sp
from plotly import graph_objs as go
from io import BytesIO
import base64
from datetime import date

app = Flask(__name__)

# Home route (user input form)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission and return JSON data
@app.route('/stock', methods=['POST'])
def stock():
    try:
        data = request.json
        years_of_prediction = int(data.get('years_of_prediction', 0))

        # Fetch stock data
        start = "2015-01-01"
        end = date.today().strftime("%Y-%m-%d")
        stock_data = sp.download_data(stock=data['stock_ticker'], start=start, end=end)
        
        if stock_data.empty:
            return jsonify({'message': 'Invalid stock ticker'}), 400
        
        # Fetch company name
        company_name = sp.get_ticker_info(data['stock_ticker'])
        print("Company name:", company_name)

        # Plot stock prices
        img = BytesIO()
        fig = sp.prepare_plot(stock_data)
        fig.write_image(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')

        # Predict future stock prices
        # if years_of_prediction > 0:
        #     forecast = sp.predict_stock(stock_data, period=365*years_of_prediction)
        #     forecast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail().to_dict(orient='records')
        # else:
        #     forecast_data = None



        return jsonify({
            'message': 'Success',
            'company_name': company_name,
            # 'plot_url': plot_url,
            # 'forecast': forecast_data
        })

    except Exception as e:
        return jsonify({'message': f'An error occurred: {e}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
