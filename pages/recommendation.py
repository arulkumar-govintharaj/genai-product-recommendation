import streamlit as st
from PIL import Image
import os, shutil
import json

from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


st.set_page_config(layout="wide")
image = Image.open('./static/MerkleLogo.jpg')
st.sidebar.image(image)

#st.header("#Product Recommendations")
st.sidebar.markdown("#Product Recommendations Page")



orders = st.session_state.user_select_value
user_search_Text = st.session_state.user_search_Text

class HomeDecorProduct:
    def __init__(self, id, title, description, price, product_type, specifications):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.product_type = product_type
        self.specifications = specifications


def displayProducts(homeDecorProducts : []):
    
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    length = len(homeDecorProducts) 
    
    if 1 <= length :
    
        with col1:
            st.header(homeDecorProducts[0].title)
            st.write(homeDecorProducts[0].id)
            image = Image.open('./static/'+homeDecorProducts[0].id.strip()+".jpg")
            st.image(image, caption=homeDecorProducts[0].title,use_column_width=True)
            #st.image("https://localhost:9002/fasttrackstorefront/_ui/responsive/theme-fasttrack-green/images/missing_product_EN_300x300.jpg")
            st.write(homeDecorProducts[0].price)
            st.caption(homeDecorProducts[0].product_type)
            st.write(homeDecorProducts[0].description)
    if 2 <= length :
            
        with col2:
            st.header(homeDecorProducts[1].title)
            st.write(homeDecorProducts[1].id)
            image = Image.open('./static/'+homeDecorProducts[1].id.strip()+".jpg")
            st.image(image, caption=homeDecorProducts[1].title,use_column_width=True)
            #st.image("https://localhost:9002/fasttrackstorefront/_ui/responsive/theme-fasttrack-green/images/missing_product_EN_300x300.jpg")
            st.write(homeDecorProducts[1].price)
            st.caption(homeDecorProducts[1].product_type)
            st.write(homeDecorProducts[1].description)
    
    if 3 <= length :
    
        with col3:
            st.header(homeDecorProducts[2].title)
            st.write(homeDecorProducts[2].id)
            image = Image.open('./static/'+homeDecorProducts[2].id.strip()+".jpg")
            st.image(image, caption=homeDecorProducts[2].title,use_column_width=True)
            #st.image("https://localhost:9002/fasttrackstorefront/_ui/responsive/theme-fasttrack-green/images/missing_product_EN_300x300.jpg")
            st.write(homeDecorProducts[2].price)
            st.caption(homeDecorProducts[2].product_type)
            st.write(homeDecorProducts[2].description)
            
    if 4 <= length :
            
       with col4:
            st.header(homeDecorProducts[3].title)
            st.write(homeDecorProducts[3].id)
            image = Image.open('./static/'+homeDecorProducts[3].id.strip()+".jpg")
            st.image(image, caption=homeDecorProducts[3].title,use_column_width=True)
            st.image("https://localhost:9002/fasttrackstorefront/_ui/responsive/theme-fasttrack-green/images/missing_product_EN_300x300.jpg")
            st.write(homeDecorProducts[3].price)
            st.caption(homeDecorProducts[3].product_type)
            st.write(homeDecorProducts[3].description)
            
   

def get_recommendations( userInput : []) : 

    with st.spinner(':blue[Loading recommendations...]'):
        #loader = CSVLoader(file_path='data/baseproductsExport.csv')
        #docs = loader.load()
        
        embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        persist_directory = 'data/chroma/'
        #shutil.rmtree("data/chroma/")  # remove old database files if any
        
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

        #vectordb = Chroma.from_documents(documents=docs, embedding=embedding, persist_directory=persist_directory)
            
        #vectordb.persist()
        

        questions = userInput
        #print(questions)
        #homeDecorProducts = []
        
        for userQuestion in questions :
            homeDecorProducts = []
            searchResults = vectordb.similarity_search(userQuestion,k=4 )
            
            #searchResults = vectordb.max_marginal_relevance_search(userQuestion,k=3)
            #st.write(searchResults)
            st.header(f"Recommendations for :green[{userQuestion}]", divider='rainbow')
            
            
            for searchResult in searchResults:
                productString = searchResult.page_content
                #st.write(productString)
                prodAttributes = productString.split("\n")
                homeDecorProducts.append(HomeDecorProduct(prodAttributes[0].split(":")[1], 
                                 prodAttributes[1].split(":")[1],
                                 prodAttributes[2].split(":")[1],
                                 prodAttributes[3].split(":")[1],
                                 prodAttributes[4].split(":")[1],
                                 prodAttributes[5].split(":")[1]))

            displayProducts(homeDecorProducts)
    st.success('Done!')



if len(orders) != 0 :
    get_recommendations(orders)
    
if len(user_search_Text) != 0 :
    searchString = []
    searchString.append(user_search_Text)
    get_recommendations(searchString)
    
    
 
    #recommended_products_json = json.dumps(HomeDecorProducts, default=vars)

