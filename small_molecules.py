from requests_cache import disabled
import streamlit as st
import pandas as pd
from PIL import Image
import subprocess
import os
import base64
import pickle

from sympy import true

# Molecular descriptor calculator


def desc_calc():
    # Performs the descriptor calculation
    bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    os.remove('molecule.smi')

# File download


def filedownload(df):
    csv = df.to_csv(index=False)
    # strings <-> bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

# Model building


def build_model(input_data):
    # Reads in saved regression model
    load_model = pickle.load(open('MOAB_model.pkl', 'rb'))
    # Apply model to make predictions
    prediction = load_model.predict(input_data)
    st.header('**Prediction output**')
    prediction_output = pd.Series(prediction, name='pIC50')
    molecule_name = pd.Series(load_data[1], name='molecule_name')
    df = pd.concat([molecule_name, prediction_output],
                   axis=1).sort_values(by=['pIC50'], ascending=False)
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)
    st.balloons()


# Logo image
image = Image.open('moab_image.png')

st.image(image, use_column_width=True)

# Page title
st.title("""Bioactivity prediction to inhibit the Monoamine Oxidase B enzyme""")

st.header("""This app allows you to predict the bioactivity towards inhibting the `Monoamine Oxidase B` enzyme (CHEMBL2039) which is a known drug target for Parkinson's disease.
""")


st.markdown("""
**Credits**
- App built with `Python` + `Streamlit`, influenced from a existing version of [Chanin Nantasenamat](https://github.com/dataprofessor)

- Descriptor calculated using [PaDEL-Descriptor](http://www.yapcwsoft.com/dd/padeldescriptor/) [[Read the Paper]](https://doi.org/10.1002/jcc.21707).

Patrick Meier MSc Medical IT | University of Applied Sciences and Arts Northwestern Switzerland
___


""")


# Sidebar
with st.sidebar.header('1. Upload SMILES file'):
    uploaded_file = st.sidebar.file_uploader(
        "Upload your input file", type=['txt'])
    if uploaded_file is not None:
        disabled_bool = False
    else:
        disabled_bool = True

    with st.sidebar.expander("SMILE file example"):
        st.text("""
    CC(C)NNC(=O)c1ccncc1 CHEMBL92401
    O=C1Nc2ccccc2C1=O CHEMBL326294
    Cl.NC1CC1c1ccccc1 CHEMBL542118
    COc1cc(O)ccc1O CHEMBL551075
    NNC(N)=O CHEMBL903    
        """)


if st.sidebar.button('Predict', disabled=disabled_bool):
    load_data = pd.read_table(uploaded_file, sep=' ', header=None)
    load_data.to_csv('molecule.smi', sep='\t', header=False, index=False)

    st.header('**Original input data**')
    st.write(load_data)

    with st.spinner("Calculating descriptors..."):
        desc_calc()

    # Read in calculated descriptors and display the dataframe
    st.header('**Calculated molecular descriptors**')
    desc = pd.read_csv('descriptors_output.csv')
    st.write(desc)
    st.write(desc.shape)

    # Read descriptor list used in previously built model
    st.header('**Subset of descriptors from previously built models**')
    Xlist = list(pd.read_csv('descriptor_list.csv').columns)
    desc_subset = desc[Xlist]
    st.write(desc_subset)
    st.write(desc_subset.shape)

    # Apply trained model to make prediction on query compounds
    build_model(desc_subset)
else:
    st.info('Upload input data in the sidebar to start!')
