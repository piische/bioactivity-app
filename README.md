# Bioactivity prediction to inhibit the Monoamine Oxidase B enzyme

Predicting the bioactivity of molecules in SMILES format towards a known target molecule Monoamine Oxidase B (CHEMBL2039)

# Start the web app

1. Clone the project

```
git clone git@github.com:piische/bioactivity-app.git
```

2. cd into project

```
cd bioactivity-app
```

3. Create a conda environment called bioactivity

```
conda create -n bioactivity python=3.7.9
```

4. Login to the _bioactivity_ environment

```
conda activate bioactivity
```

5. Install the dependencies

```
pip install -r requirements.txt
```

6. Unzip the model

```
unzip moab_model.zip
```

7. Start the app

```
streamlit run small_molecules.py
```
