# Instagram Comment Sentiment Analysis

## Description
The Instagram Comment Sentiment Analysis application is designed to generate synthetic Instagram comments, store them in a Snowflake database, and perform sentiment analysis on these comments. The application uses Streamlit for the user interface, allowing users to generate comments, store them in Snowflake, and visualize the sentiment analysis results.

## Features
- **Generate Synthetic Instagram Comments**: Create a dataset of synthetic Instagram comments with varying sentiments.
- **Store Data in Snowflake**: Connect to a Snowflake database and store the generated comments.
- **Perform Sentiment Analysis**: Analyze the sentiment of the comments using Snowflake's built-in sentiment analysis function.
- **Visualize Results**: Display the sentiment distribution and sentiment score histogram using Streamlit and Matplotlib.

## Installation
To set up the project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ryanklapperhakkoda/abbvie_demos
    cd abbvie_demos
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the project root directory and add your Snowflake credentials:
    ```
    SNOWFLAKE_USERNAME=<your_snowflake_username>
    SNOWFLAKE_PASSWORD=<your_snowflake_password>
    SNOWFLAKE_ACCOUNT=<your_snowflake_account>
    SNOWFLAKE_WAREHOUSE=<your_snowflake_warehouse>
    SNOWFLAKE_DATABASE=<your_snowflake_database>
    SNOWFLAKE_SCHEMA=<your_snowflake_schema>
    ```

## Usage
To run the application, use the following command:
```bash
streamlit run app.py
```

### Steps to Use the Application
1. **Generate Data**: The application will automatically generate synthetic Instagram comments when it starts.
2. **Store Data in Snowflake**: The generated comments will be stored in the specified Snowflake table.
3. **Perform Sentiment Analysis**: Click the "Perform Sentiment Analysis" button to analyze the sentiment of the comments.
4. **View Results**: The sentiment analysis results will be displayed in a table, along with visualizations of the sentiment distribution and sentiment score histogram.

## Configuration
The application requires configuration of Snowflake credentials through environment variables. Ensure that the `.env` file is correctly set up with the necessary credentials.

## Dependencies
- **pandas**: Data manipulation and analysis library.
- **random**: Python's built-in module for generating random numbers.
- **uuid**: Python's built-in module for generating unique identifiers.
- **os**: Python's built-in module for interacting with the operating system.
- **dotenv**: Library for loading environment variables from a `.env` file.
- **snowflake-connector-python**: Snowflake's Python connector for database interaction.
- **streamlit**: Framework for creating interactive web applications.
- **matplotlib**: Library for creating static, animated, and interactive visualizations in Python.

## Example
Here is an example of how to run the application:
```bash
streamlit run app.py
```

Once the application is running, you can interact with the Streamlit interface to generate comments, store them in Snowflake, perform sentiment analysis, and visualize the results.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements
- The sentiment analysis functionality leverages Snowflake's built-in sentiment analysis capabilities.
- The application interface is built using Streamlit, a powerful tool for creating interactive web applications.