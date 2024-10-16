import instaloader
import pandas as pd
import os
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

class InstagramCommentScraper:
    def __init__(self):
        self.data = None
        self.df = None
        self.conn = None
        self.L = instaloader.Instaloader()
        self.L.login(os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))

    def scrape_comments(self, post_url):
        st.write(post_url)
        shortcode = post_url.split("/")[-1]
        if shortcode == "p":
            shortcode = post_url.split("/")[-2]
        st.write(shortcode)
        post = instaloader.Post.from_shortcode(self.L.context, shortcode)
        
        comments = []
        for comment in post.get_comments():
            comments.append({
                'INSTAGRAM_POSTER_ID': post.owner_id,
                'INSTAGRAM_POST_ID': post.mediaid,
                'INSTAGRAM_COMMENTER_ID': comment.owner.userid,
                'INSTAGRAM_USERNAME': comment.owner.username,
                'INSTAGRAM_COMMENT': comment.text
            })
        
        self.df = pd.DataFrame(comments)

    def connect_to_snowflake(self):
        load_dotenv()
        self.conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USERNAME'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )

    def write_to_snowflake(self, table_name='INSTAGRAM_COMMENTS'):
        write_pandas(self.conn, self.df, table_name)

    def get_sentiment_analysis(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT INSTAGRAM_COMMENT, SNOWFLAKE.CORTEX.SENTIMENT(INSTAGRAM_COMMENT) AS COMMENT_SENTIMENT FROM INSTAGRAM_COMMENTS")
        return cursor.fetchall()

class StreamlitApp:
    def __init__(self):
        self.comment_scraper = InstagramCommentScraper()

    def run(self):
        st.title('Instagram Comment Scraper and Sentiment Analysis')

        post_url = st.text_input('Enter Instagram post URL:')
        if st.button('Scrape Comments'):
            self.comment_scraper.scrape_comments(post_url)
            self.comment_scraper.connect_to_snowflake()
            self.comment_scraper.write_to_snowflake()
            st.success(f"Scraped {len(self.comment_scraper.df)} comments and wrote to Snowflake.")

        if st.button('Perform Sentiment Analysis'):
            results = self.comment_scraper.get_sentiment_analysis()
            for comment, sentiment in results:
                st.write(f"Comment: {comment}")
                st.write(f"Sentiment: {sentiment}")
                st.write("---")

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()