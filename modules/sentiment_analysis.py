import pandas as pd
import random
import uuid
import os
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import streamlit as st
import matplotlib.pyplot as plt

class InstagramCommentGenerator:
    def __init__(self):
        self.data = None
        self.df = None
        self.conn = None

    def generate_username(self):
        return 'user_' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))

    def generate_data(self, num_records=100):
        self.data = {
            'INSTAGRAM_POSTER_ID': [str(uuid.uuid4()) for _ in range(num_records)],
            'INSTAGRAM_POST_ID': [str(uuid.uuid4()) for _ in range(num_records)],
            'INSTAGRAM_COMMENTER_ID': [str(uuid.uuid4()) for _ in range(num_records)],
            'INSTAGRAM_USERNAME': [self.generate_username() for _ in range(num_records)],
            'INSTAGRAM_COMMENT': [
        random.choice([
            # Positive comments
            "This skincare product is amazing!", "Love this beauty tip!", "Your skin looks flawless!", "Great beauty routine!",
            "This makeup tutorial is fantastic!", "Thanks for the beauty advice!", "Your hair looks stunning!", "This is really inspiring!",
            "Keep up the great work with these beauty tips!", "This made my day!", "Fantastic beauty shot!", "You're so talented with makeup!",
            "This is beauty goals!", "Can't stop looking at this flawless skin!", "Absolutely stunning makeup!",
            "Incredible beauty routine!", "You nailed this look!", "This is perfection!", "So impressive!",
            "You've outdone yourself with this beauty tip!", "This deserves more likes!", "I'm in awe of your beauty skills!", "Brilliant beauty content!",
            "This is next level beauty!", "You're killing it with these tips!", "Masterpiece makeup!", "I'm blown away by your skills!",
            "This is pure gold for skincare!", "You're an inspiration in the beauty world!", "Phenomenal beauty post!", "This is everything I needed!",
            "You've got beauty skills!", "I'm obsessed with this look!", "Top-notch beauty content!", "This is fire!",
            "You're a beauty genius!", "This deserves an award!", "I'm speechless!", "Absolutely incredible!",
            "You've raised the bar in beauty!", "This is art!", "Mind-blowing beauty tips!",
            
            # Neutral comments
            "Interesting beauty tip.", "Okay, I see.", "Not bad.", "It's alright.", "Hmm, interesting perspective on skincare.",
            "I'm not sure what to think.", "This is different.", "I guess it's cool.", "Meh.",
            "It's a beauty post.", "Just scrolling by.", "I have no strong feelings about this.",
            "Fair enough.", "I suppose.", "Could be worse.", "It exists.", "Noted.",
            "Moving on.", "Whatever works for you.", "If you say so.", "Sure, why not.",
            "I'll think about it.", "Huh.", "That's a thing.", "Okay then.", "I see what you did there.",
            "Well, that happened.", "Interesting choice.", "That's one way to do it.", "I guess that's valid.",
            "Not my thing, but okay.", "To each their own.", "I'm indifferent.", "It's certainly unique.",
            "I'll reserve judgment.", "That's... something.", "I have questions, but I'll keep scrolling.",
            "Not what I expected, but okay.", "I'm processing this.",
            
            # Negative comments
            "I don't get it.", "This beauty tip is overrated.", "Not my cup of tea.", "I've seen better.",
            "Why would you post this?", "This is disappointing.", "I expected more.",
            "This doesn't make sense.", "I'm not impressed.", "You could do better.",
            "This is a letdown.", "I'm cringing.", "This ain't it.", "Hard pass.",
            "You've done better before.", "This feels forced.", "I'm not feeling it.",
            "This is a miss for me.", "Yikes.", "This is problematic.", "Not your best work.",
            "This feels off.", "I'm confused and not in a good way.", "This is a no from me.",
            "I can't support this.", "This missed the mark.", "I'm actually offended.",
            "This is tone-deaf.", "Did you even try?", "This is embarrassing.",
            "I'm unfollowing after this.", "This is why we can't have nice things.",
            "I regret clicking on this.", "This is a waste of time.", "Do better.",
            "I'm disappointed in you.", "This is just bad.",
            
            # Questions or engagement
            "What's the story behind this beauty tip?", "Where was this skincare routine developed?", "How did you achieve that look?",
            "Can you explain more about this product?", "When's your next beauty post?", "Do you have a tutorial for this makeup look?",
            "What inspired you to create this?", "How long did this skincare routine take?", "What products did you use?",
            "Can you share your beauty process?", "Is this part of a series?", "What's your favorite part of this routine?",
            "Any behind-the-scenes info on this look?", "Who else was involved in this beauty project?", "What challenges did you face with this look?",
            "How does this relate to your previous beauty work?", "What's next for you in beauty?",
            "Can you recommend similar beauty content?", "How can we support your beauty work?",
            "What's the best way to learn this beauty skill?", "Do you offer beauty classes or workshops?",
            "How do you come up with your beauty ideas?", "What's your creative process like for beauty content?",
            "Can you share any beauty tips for beginners?", "How has your beauty style evolved over time?",
            "What's the most important lesson you've learned in beauty?",
            "How do you stay motivated in the beauty industry?", "What's your ultimate goal with your beauty content?",
            "How do you handle criticism in the beauty world?", "What's the best beauty advice you've ever received?",
            "How do you balance creativity and commercial success in beauty?",
            
            # Emoji-only responses
            "😍 Love it!", "👍 Nice one", "🔥 Fire", "💯 Spot on", "🙌 Yasss", "😊 Sweet", "🤔 Hmm", "😐 Meh", "😕 Unsure", "👎 Nah",
            "❤️ Adore", "🎉 Congrats", "👏 Bravo", "🤩 Awesome", "😎 Cool", "🥰 Adorable", "😮 Wow", "🤯 Mind blown", "😂 Hilarious", "😍 Gorgeous",
            "💪 Strong work", "👀 Interesting", "🙏 Thanks", "💖 Love this", "🌟 Stellar", "✨ Magic", "💕 Lovely", "🔝 Top notch", "👌 Perfect", "💥 Boom",
            "🚀 Next level", "💡 Brilliant", "🏆 Winner", "🎨 Artistic", "📸 Great shot", "🎭 Dramatic", "🌈 Colorful", "🦄 Unique", "🍾 Cheers", "🥳 Party time",
            
            # Longer, more detailed responses
            "This post really resonates with me. It reminds me of my own experiences with skincare.",
            "I'm not sure I agree with the message here, but I appreciate you sharing your beauty perspective.",
            "This beauty content feels a bit repetitive. Maybe try something new next time?",
            "Your growth as a beauty content creator is really evident in this post. Well done!",
            "I'm conflicted about this. On one hand it's visually appealing, but the message is problematic.",
            "I've been following your beauty journey for a while now, and it's incredible to see how far you've come. This post is a testament to your dedication and creativity.",
            "While I understand what you're trying to convey, I think there might be some unintended implications here. Have you considered how this might be interpreted by different audiences?",
            "This post challenges my preconceptions and makes me reconsider my stance on the beauty topic. Thank you for providing such thought-provoking content.",
            "I appreciate the effort you've put into this, but I feel like it's missing some crucial context. Perhaps adding some background information would make it more impactful?",
            "Your unique perspective shines through in this beauty post. It's refreshing to see content that doesn't just follow trends but actually adds value to the conversation.",
            "I'm impressed by the technical skill displayed here, but I'm left wondering about the ethical considerations behind this beauty project. Could you elaborate on that aspect?",
            "This post perfectly captures the zeitgeist of our current beauty moment. It's both a reflection of and a commentary on our society. Brilliantly done!",
            "I've seen similar beauty content before, but your take on it is truly original. You've managed to breathe new life into a familiar concept.",
            "The attention to detail in this beauty post is remarkable. It's clear that you've put a lot of thought and effort into every aspect of it.",
            "This post has sparked an interesting debate in the comments. It's fascinating to see how different people interpret and react to your beauty work."
        ])
                for _ in range(num_records)
            ]
        }
        self.df = pd.DataFrame(self.data)

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

    def write_to_snowflake(self, df, table_name):
        write_pandas(self.conn, df, table_name)

    def get_sentiment_analysis(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT INSTAGRAM_POSTER_ID, INSTAGRAM_POST_ID, INSTAGRAM_COMMENTER_ID, INSTAGRAM_USERNAME, INSTAGRAM_COMMENT, SNOWFLAKE.CORTEX.SENTIMENT(INSTAGRAM_COMMENT) AS COMMENT_SENTIMENT FROM INSTAGRAM_COMMENTS")
        return cursor.fetchall()
    
    def read_from_snowflake(self, table_name):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        return cursor.fetchall()

class StreamlitApp:
    def __init__(self):
        self.comment_generator = InstagramCommentGenerator()

    def run(self):
        st.title('IG Sentiment Analysis Module')

        # self.comment_generator.generate_data()
        self.comment_generator.connect_to_snowflake()
        # self.comment_generator.write_to_snowflake(self.comment_generator.df, 'INSTAGRAM_COMMENTS')

        if st.button('Perform Sentiment Analysis'):
            results = self.comment_generator.read_from_snowflake('INSTAGRAM_SENTIMENT_ANALYSIS')
            results_df = pd.DataFrame(results, columns=['INSTAGRAM_POSTER_ID', 'INSTAGRAM_POST_ID', 'INSTAGRAM_COMMENTER_ID', 'INSTAGRAM_USERNAME', 'INSTAGRAM_COMMENT', 'INSTAGRAM_SENTIMENT_SCORE', 'INSTAGRAM_SENTIMENT_LABEL'])
            results_df = results_df[['INSTAGRAM_COMMENT', 'INSTAGRAM_SENTIMENT_SCORE', 'INSTAGRAM_SENTIMENT_LABEL']]
            st.dataframe(results_df)

            embed_url = 'https://app.sigmacomputing.com/embed/4dwK1x1CduWhcE4238JaiX'

            iframe_html = f"""
            <div style="display: flex; justify-content: center; width: 80vw;">
                <iframe src="{embed_url}" style="width: 100%; height: 800px;" frameborder="0"></iframe>
            </div>
            """

            st.markdown(iframe_html, unsafe_allow_html=True)

def main():
    app = StreamlitApp()
    app.run()

if __name__ == "__main__":
    main()