# YouTube Comment Sentiment Analysis Web App

This web application built with Flask analyzes comments from a YouTube video. It extracts comments using the YouTube Data API, performs sentiment analysis on them, generates a word cloud, and calculates precision and recall metrics.

## Setup

1. **Clone Repository:** Clone this repository to your local machine:
   
   ```bash
   git clone https://github.com/your_username/your_repository.git
   ```

2. **Navigate to Directory:** Navigate to the project directory:

   ```bash
   cd your_repository
   ```

3. **Install Dependencies:** Install the required dependencies listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Obtain API Key:** Obtain a YouTube Data API key from the [Google Developers Console](https://console.developers.google.com/) and replace `'YOUR_API_KEY'` in `app.py` with your actual API key.

## Usage

1. **Run Application:** Run the Flask application:

   ```bash
   python app.py
   ```

2. **Access Web Interface:** Open a web browser and go to `http://localhost:5000` to access the web interface.

3. **Enter Video URL:** Enter the URL of the YouTube video you want to analyze and submit the form.

4. **View Analysis:** Wait for the analysis to complete. Once finished, the web page will display the word cloud of comments, the most positive and negative comments, and precision and recall metrics.

## File Structure

- `app.py`: Contains the Flask application code including routes and analysis functions.
- `templates/`: Directory containing HTML templates for rendering the web pages.
- `static/`: Directory for storing static files such as CSS stylesheets and client-side scripts.

## Credits

- [Flask](https://flask.palletsprojects.com/): Web framework for Python.
- [YouTube Data API](https://developers.google.com/youtube/v3): API for fetching YouTube data.
- [TextBlob](https://textblob.readthedocs.io/en/dev/): Python library for processing textual data.
- [WordCloud](https://amueller.github.io/word_cloud/): Python library for creating word clouds.
- [Matplotlib](https://matplotlib.org/): Python plotting library for visualization.
- [Bootstrap](https://getbootstrap.com/): Front-end component library for designing responsive web pages.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
