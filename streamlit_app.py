# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie:cup_with_straw: ")
st.write(
  """Choose the Fruits you want in your Custom smoothie
  """
)
name_on_order=st.text_input('Name on Smoothie')
st.write('The Name on Smoothie will be :',name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list=st.multiselect('choose upto 5 ingredients:',
                               my_dataframe,max_selections=5)
if ingredients_list:
   
    ingredients_string=''
    for x in ingredients_list:
        ingredients_string+=x+ ' '
        st.subheader(x+'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+x)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string  + """','""" + name_on_order  + """')"""

    st.write(my_insert_stmt)
    time_to_insert = st.button('submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("""Your Smoothie is ordered,""" + name_on_order  + """!""", icon="✅")








        
