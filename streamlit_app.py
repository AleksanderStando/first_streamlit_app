import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError 

streamlit.title('My Parents New Healthy Diner!')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_slected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_slected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choise)
  return pandas.json_normalize(fruityvice_response.json())

streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choise = streamlit.text_input('What fruit do you want to have information about?', 'Kiwi')
  if not fruit_choise:
    streamlit.error('Please select a fruit to get information')
  else:
    fruityvice_normalized = get_fruityvice_data(fruit_choise)
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('Would you like to add some fruit?', 'jackfruit')
my_cur.execute("INSERT INTO fruit_load_list VALUES ('{}')".format(add_my_fruit))

