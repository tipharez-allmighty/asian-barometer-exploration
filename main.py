import pandas as pd
import streamlit as st
import plotly.express as px
from io import StringIO

st.set_page_config(layout="centered")

def stata_to_csv(uploaded_file):
    stata_file = pd.read_stata(uploaded_file)
    csv_data = stata_file.to_csv(index=False)
    csv_file_like_object = StringIO(csv_data)
    df = pd.read_csv(csv_file_like_object)
    return df

def plot_questions(data, columns):
    for col in columns:
        data_counts = data[f'{col}'].value_counts(normalize=False)
        if not data_counts.empty:
            total_values = data_counts.sum()
            percentages = [(count/total_values) * 100 for count in data_counts.values]
            percentages = [f'{percent:.1f}%' for percent in percentages]
            combined_labels = [f'{value}\n({percent})' for value, percent in zip(data_counts,percentages)]
            fig = px.bar(data, y=data_counts.index, x=data_counts.values, text=combined_labels, color=data_counts.index,
                            labels={'x': '', 'y': ''})
            fig.update_traces(textposition='outside')
            fig.update_layout(yaxis=dict(autorange="reversed"),
                                xaxis_showticklabels=False,
                                showlegend=False, title=f'{col}') 
            st.plotly_chart(fig)
        else:
            st.write('No data avaliable')



uploaded_file = st.file_uploader('Upload dta (stata) file')

if uploaded_file:
    df = stata_to_csv(uploaded_file)
    columns_starting_with_q = [col for col in df.columns if col.startswith('Q')]
    options = st.multiselect("Please select columns", columns_starting_with_q)
    st.write(df.head())
    if options:
        st.sidebar.header('Please filter here:')
        gender = st.sidebar.multiselect('Filter by gender:',
                                        options=df['IR2a'].unique(),
                                        default=df['IR2a'].unique())
        level = st.sidebar.multiselect('Filter by area:',
                                        options=df['Level'].unique(),
                                        default=df['Level'].unique())
        ethnicity = st.sidebar.multiselect('Filter by ethnicity:',
                                        options=df['Se11_1'].unique(),
                                        default=df['Se11_1'].unique())
        religion = st.sidebar.multiselect('Filter by religion:',
                                        options=df['Se6'].unique(),
                                        default=df['Se6'].unique())
              
        df_selection = df.query('Level == @level & Se11_1 == @ethnicity & IR2a == @gender & Se6 == @religion')
        
        plot_questions(df_selection, options)
