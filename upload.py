import streamlit as st
import pandas as pd
import pickle

def upload_data():
	st.subheader('Use Batch Sentiment Analyzer')
	st.write('Upload the review dataset to get the sentiment of each review')

	try:
		with open('sentiment analysis app/pickle files/log_reg.pkl', 'rb') as f:
			model = pickle.load(f)
			
		with open('sentiment analysis app/pickle files/tfidf_vectorizer.pkl', 'rb') as f:
			tfidf_vectorizer = pickle.load(f)
	except:
		print('file path not specified')

	try:
		uploaded_file = st.file_uploader('Review dataset here', type='csv')
		if uploaded_file:
			reviews = pd.read_csv(uploaded_file)
			reviews = reviews.dropna(subset=['review_comment_message']).drop_duplicates(subset=['review_comment_message']).reset_index()
			st.dataframe(reviews['review_comment_message'].head(10), width=600)
			rev_msg = reviews['review_comment_message'].tolist()
			predictions = model.predict(tfidf_vectorizer.transform(rev_msg))
			# prediction_proba = model.predict_proba(tfidf_vectorizer.transform(rev_msg)[:,1])
			reviews['sentiment_class'] = pd.Series(predictions)
			# reviews['sentiment_confidence_score'] = pd.Series(prediction_proba)

			reviews['sentiment_class'] = reviews['sentiment_class'].map({1:'Positive', 0:'Negative'})
			# view_sentiment = st.button('Click to View Sentiments')
			# n = int(st.text_input('number of rows to display?'))
			st.dataframe(reviews[['review_comment_message', 'sentiment_class']].head(20), width=600)
			pct_pos = reviews['sentiment_class'].value_counts(normalize=True)*100
			st.write(pct_pos)
			if reviews['sentiment_class'][0] == 'Positive':
				st.success('**Review text is Positive :joy: :yum:**')
				st.balloons()
			elif reviews['sentiment_class'][0] == 'Negative':
				st.error('**Review text is Negative :cry: :worried:**')

	except:
		print('Upload CSV files')


if __name__ == '__main__':
	upload_data()