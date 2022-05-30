import pandas
import streamlit
import requests
import snowflake.connector

streamlit.title("New Healthly Dinner")


streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥑🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('🍞Hard-Boiled Free-Range Egg')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fuits_selected = streamlit.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado','Strawberries']   )
fruits_to_show = my_fruit_list.loc[fuits_selected]

streamlit.dataframe(fruits_to_show)



streamlit.header("FruitVice Fruit Advice")
fruit_choice  = streamlit.text_input('What fruit you would like te information about?', "Kiwi")
streamlit.write("The user entered: ", fruit_choice)

fruitvice_reposnes = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

fruityvice_normalized = pandas.json_normalize(fruitvice_reposnes.json())
streamlit.dataframe(fruityvice_normalized)



#Snowflake connection
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)





