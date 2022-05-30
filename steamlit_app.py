import pandas
import streamlit
import requests
import snowflake.connector
from urllib.error import URLError

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


def get_fuityvice_data(this_fruit_choice):
    fruitvice_reposnes = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruitvice_reposnes.json())
    return fruityvice_normalized

streamlit.header("FruitVice Fruit Advice")
try: 
  fruit_choice  = streamlit.text_input('What fruit you would like te information about?', "Kiwi")
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_funcntion = get_fuityvice_data(fruit_choice)
    streamlit.dataframe(back_from_funcntion)
except URlerror as e:
  streamlit.error()


#Snowflake connection
streamlit.text("The fruit load list cotains:")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        return my_cur.fetchall()
    
if streamlit.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

    
add_my_fruit = streamlit.text_input('What fruit would you like to add?')

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("Insert into fruit_load_list values ('"+ new_fruit+ "')")
        return "Thanks for adding" + new_fruit
    
if streamlit.button('Add fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)





