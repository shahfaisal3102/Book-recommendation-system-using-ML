import pickle
import streamlit as st
import numpy as np

st.header("Book Recommendation System Using Machine Learning")

model = pickle.load(open("Books/book_model.pkl",'rb'))
book_name = pickle.load(open("Books/book_name.pkl",'rb'))
book_pivot = pickle.load(open("Books/book_pivot.pkl",'rb'))
final_df = pickle.load(open("Books/final_df.pkl",'rb'))


def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]:   # assuming suggestion returns clusters
        ids = np.where(final_df['Title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_df.iloc[idx]['Image-URL']   # ✅ correct column access
        poster_url.append(url)

    return poster_url


def recommend_books(book_name):
    book_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1),n_neighbors=6)

    poster_url = fetch_poster(suggestion)

    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            book_list.append(j)

    return book_list, poster_url


Selected_books = st.selectbox(
    "Search books", book_name
)

if st.button('Recommend'):
    recommendation_books, poster_url = recommend_books(Selected_books)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(poster_url[1])
        st.text(recommendation_books[1])
    
    with col2:
        st.image(poster_url[2])
        st.text(recommendation_books[2])

    with col3:
        st.image(poster_url[3])
        st.text(recommendation_books[3])

    with col4:
        st.image(poster_url[4])
        st.text(recommendation_books[4])
    
    with col5:
        st.image(poster_url[5])
        st.text(recommendation_books[5])


# Footer
st.markdown("---")
st.caption("Developed by **Shah Faisal Khan** | Collaborative Filtering with KNN")