import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

image = Image.open('./static/MerkleLogo.jpg')
st.sidebar.image(image)

st.title("""
 Product Recommendations Systems
 """)
 


 
df = pd.read_csv('data/baseproductsExport.csv')

dataFrame = pd.DataFrame({
   
  'Product Id': df['id'],
  'Title': df['title'],
  'Description' : df['description'],
  'Price' : df['price'],
  'Category' : df['product_type'],
  'Specifications' : df['specifications']
})

dataFrame



form = st.sidebar.form("Basic form")
selectedProducts = form.multiselect(":black[Add your purchase history]", df['title'])
searchText = form.text_input("Search Text","")
submitted = form.form_submit_button("Submit")

if submitted :
    st.session_state['user_select_value'] = selectedProducts
    st.session_state['user_search_Text'] = searchText
    switch_page("recommendation")
    
