from datetime import datetime
from connections import mongo_collection, mongo_client
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd

from crud import loans_collection, get_loan_by_book


def load_loan_data(book_id):
    loans = get_loan_by_book(book_id)
    print(loans)
    loan_dates = [loan['loan_date'] for loan in loans]
    loan_counts = pd.Series(1, index=pd.to_datetime(loan_dates))
    loan_counts = loan_counts.resample('ME').sum().fillna(0)
    print(loan_counts)
    return loan_counts


def fit_model(loan_counts):
    # Fit an Exponential Smoothing model
    model = ExponentialSmoothing(loan_counts, seasonal='add', seasonal_periods=12)
    model_fit = model.fit()
    return model_fit


def predict(book_id, periods=12):
    loan_counts = load_loan_data(book_id)
    if loan_counts.empty:
        return f"No loan data available for book ID {book_id}."

    model_fit = fit_model(loan_counts)
    forecast = model_fit.forecast(periods)

    forecast_dates = forecast.index.strftime('%Y-%m')
    forecast_values = forecast.values

    predictions = dict(zip(forecast_dates, forecast_values))
    return predictions


# Example usage
if __name__ == "__main__":
    book_id = 1
    prediction = predict(book_id)
    print(prediction)
