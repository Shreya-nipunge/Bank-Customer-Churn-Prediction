
# 🏦 Bank Customer Churn Prediction Pro

This project is a high-performance **Machine Learning** application designed to predict bank customer churn. It features a premium, mobile-responsive **Streamlit** interface, real-time analytics, and comprehensive historical tracking.

## 🚀 Key Features

-   **Full 19-Feature Input**: Allows detailed analysis using every customer attribute from the dataset (Demographics, Financials, Activity).
-   **Random Forest Intelligence**: Powered by a retrained `RandomForestClassifier` with **96.1% accuracy** (scikit-learn 1.8.0).
-   **Confidence Scoring**: Real-time probability scoring for every prediction.
-   **Historical Tracking**: SQLite-backed history system that stores every prediction and confidence score.
-   **Premium UI/UX**: Modern glassmorphism design with interactive **Plotly** charts for data visualization.
-   **Mobile Responsive**: Optimized layout that scales beautifully from desktops to smartphones.

## 🛠️ Technology Stack

-   **Frontend/Backend**: [Streamlit](https://streamlit.io/)
-   **Machine Learning**: [scikit-learn](https://scikit-learn.org/), [pandas](https://pandas.pydata.org/), [numpy](https://numpy.org/)
-   **Visualizations**: [Plotly](https://plotly.com/)
-   **Persistence**: [SQLite](https://www.sqlite.org/)
-   **Model Serialization**: [joblib](https://joblib.readthedocs.io/)

## 📦 Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd BankChurnProject
    ```

2.  **Set up Virtual Environment**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    source venv/bin/activate  # macOS/Linux
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🏃 Run the Application

Start the local development server:
```bash
streamlit run streamlit_app.py
```
The application will be accessible at: `http://localhost:8501`

## 📂 Project Structure

-   `streamlit_app.py`: Main entry point for the Streamlit application and UI logic.
-   `churn_model.pkl`: The trained Random Forest model (scikit-learn 1.8.0).
-   `database.py`: Logic for SQLite history tracking.
-   `constants.py`: Feature mapping and categorical data definitions.
-   `BankChurners.csv`: Original dataset for reference.
-   `history.db`: (Auto-generated) Local database for historical predictions.

## 📊 Model Details

The model was retrained on the **BankChurners** dataset, dropping redundant columns and mapping categorical variables to numeric equivalents for optimal performance. The integration of 19 distinct features allows the model to capture complex relationships between customer demographics and retention risk.

---
*Created for proactive bank customer management and analytics.*
