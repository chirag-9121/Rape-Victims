# Importing the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from streamlit import config

# Importing the datasets
#@st.cache
rape_victim = pd.read_csv('./Datasets/Victims_of_rape.csv')
country_pop = pd.read_csv('./Datasets/IndiaPopulation_2021.csv')
literacy = pd.read_csv('./Datasets/Literacy.csv')
state_pop = pd.read_csv('./Datasets/State Population.csv')

# CLeaning the datasets
rape_victim = rape_victim[['Area_Name','Year','Subgroup','Rape_Cases_Reported']]
rape_victim.rename({'Area_Name':'State'},axis=1,inplace=True)
rape_victim = rape_victim[rape_victim['Subgroup'] == 'Total Rape Victims'].reset_index().drop(['Subgroup','index'],axis=1)

country_pop = country_pop[(country_pop['Year']>=2001) & (country_pop['Year']<=2010)].sort_values('Year').set_index('Year').drop('GrowthRate',axis=1)

literacy = literacy[['Country/ States/ Union Territories Name','Literacy Rate (Persons) - Total - 2001']]
literacy.rename(columns=({'Country/ States/ Union Territories Name':'State',
                          'Literacy Rate (Persons) - Total - 2001':'Literacy Rate'}),inplace=True)
literacy.State.replace({'A & N Islands':'Andaman & Nicobar Islands',
                       'D & N Haveli':'Dadra & Nagar Haveli',
                       'NCT of Delhi':'Delhi'},inplace=True)
literacy = literacy.drop(0).sort_values('State').reset_index().drop('index',axis=1)

state_pop.columns = state_pop.columns.str.strip()
state_pop = state_pop[['State','Population']]
state_pop.State.replace({'Andaman & Nicobar Islands*':'Andaman & Nicobar Islands',
                         'Chhatisgarh':'Chhattisgarh',
                        'Jammu and Kashmir':'Jammu & Kashmir',
                        'Orissa':'Odisha',
                        'Pondicherry':'Puducherry',
                        'Uttaranchal':'Uttarakhand'},inplace=True)
state_pop = state_pop.drop(35).sort_values('State').reset_index().drop('index',axis=1)

# Merging the datasets
state_pop_and_literacy = pd.merge(state_pop,literacy,on='State')


# Interactive Plotting Function
def plot(Year=2001):

    # Setting up the variables
    rape_victim_plot = rape_victim[rape_victim['Year'] == Year].sort_values('Rape_Cases_Reported').reset_index().drop('index',axis=1)
    final_merge_plot = pd.merge(rape_victim_plot,state_pop_and_literacy,on='State')

    # Plotting with plotly.express
    fig = px.bar(final_merge_plot,x='Rape_Cases_Reported',y='State',orientation='h',title='Rape Victims in India (2001-2010)',
          labels={'Rape_Cases_Reported':'<b>Cases reported</b>','State':'<b>States</b>'},width=950,height=750,
          color='Rape_Cases_Reported',color_continuous_scale='viridis_r',hover_data=['Population', 'Literacy Rate'])
    
    # Setting the x-ticks
    layout = dict(yaxis=dict(tickmode="array",tickvals=final_merge_plot['State']))
    fig.update_layout(layout,title={'x':0.5,'y':0.95})
    
    # Few Annotations
    fig.add_annotation(dict(font=dict(size=15),x=0.5,y=0.12,
                            text="Country Population : {}<br><br>Year : {}".format(country_pop.loc[Year]['Population'],Year),
                            xanchor='left',xref="paper",yref="paper",bgcolor="White",
                            bordercolor="Black",borderpad=8,align='center'))

    return fig

# Adding to webpage
st.set_page_config(layout="wide")
st.title('Rape Victims In India (2001 - 2010)')
st.markdown("***")
st.write('The datasets that were used in this analysis are :')
st.markdown('1. <a href="https://www.kaggle.com/rajanand/crime-in-india?select=20_Victims_of_rape.csv">Rape Victim Dataset</a>',unsafe_allow_html=True)
st.markdown('2. <a href="https://www.kaggle.com/sansuthi/indian-population">Indian Population ( year-wise )</a>',unsafe_allow_html=True)
st.markdown('3. <a href="https://www.kaggle.com/doncorleone92/govt-of-india-literacy-rate">Literacy Rate ( state wise:  census-2001 )</a>',unsafe_allow_html=True)
st.markdown('4. <a href="http://cyberjournalist.org.in/census/cenindia.html">State Population ( census-2001 )</a>',unsafe_allow_html=True)
st.markdown("***")
st.header('Research Question :')
st.subheader('Which state in India had the highest number of rapes reported in a given year across a period of 2001 - 2010?')
st.markdown("***")
st.subheader('Year')
Year = st.slider('',min_value=2001,max_value=2010)
st.write(plot(Year))