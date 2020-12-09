import streamlit as st
import pickle
from google_trans_new import google_translator


def main():
	"""
	A simple NLP app
	"""


	with open('sentiment analysis app/pickle files/log_reg.pkl', 'rb') as f:
		model = pickle.load(f)
		
	with open('sentiment analysis app/pickle files/tf_idf.pkl', 'rb') as f:
		tf_idf = pickle.load(f)

	st.title('Olist User Review')
	menu = ['Home', 'About']
	choice = st.sidebar.selectbox('Menu', menu)

	if choice == 'Home':
		st.subheader('Sentiment Analysis')
		review = st.text_area('Review Text', 'Enter your Review in Portuguese')

		translator = google_translator()
		trans_text = translator.translate(text=review, lang_tgt='en')
		st.write('Would you like to translate')
		if st.button('Translate'):
			st.text_area('Translated Review Text', trans_text)
		if st.button('Get Sentiment'):
			prediction = int(model.predict(tf_idf.transform([review])))
			if prediction == 1:
				st.success('**Review text is Positive :joy: :yum:**')
			elif prediction == -1:
				st.error('**Review text is Negative :cry: :worried:**')


	if choice == 'About':
		st.subheader('Learn More About Sentiment Analysis')
		st.write('## Model was built using Logistic Regression :sunglasses:')
		st.write('Model was train in **Portuguese language**')
		st.write('''For Best Performance Review should be in that language' \n
		'Option to translate to English is Available''')
		# st.write('If you want other language Translation')




if __name__ == '__main__':
	main()