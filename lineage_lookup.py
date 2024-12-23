import gzip
import pandas as pd
import streamlit as st

from collections import defaultdict

file_name = 'proteomes_proteome_type_1_2024_12_19.tsv.gz'

@st.cache_data
def load_data(file_name):
    with gzip.open(file_name, 'rb') as f:
        df = pd.read_csv(f, sep='\t')

    df = df[df['Taxonomic lineage'].apply(lambda x: isinstance(x, str))]
    df['Taxonomic lineage'] = df['Taxonomic lineage'].apply(lambda x: [item.strip() for item in x.split(",")])
    return df

df = load_data(file_name)

def find_organisms_and_sublevels(df, taxon):
    taxon = taxon.lower()
    result = defaultdict(list)
    for _, row in df.iterrows():
        taxonomy = [level.lower() for level in row["Taxonomic lineage"]]
        organism = row["Organism"]
        if taxon in taxonomy:
            index = taxonomy.index(taxon)
            if index + 1 < len(taxonomy):
                next_level = row["Taxonomic lineage"][index + 1]
                result[next_level].append(organism)
            else:
                result["Terminal Node"].append(organism)
    return result

st.title("Lineage lookup")
st.write("Search for closely related organisms by entering a taxon below.")

selected_taxon = st.text_input("Enter the taxon you wish to explore (e.g., Euteleostomi, Fungi, Streptophyta):") 

if selected_taxon:
    result = find_organisms_and_sublevels(df, selected_taxon)
    
    if result:
        st.write(f"### Organisms under '{selected_taxon}':")
        for sublevel, organisms in result.items():
            st.write(f"**{sublevel}**:")
            for organism in organisms:
                st.write(f"- {organism}")
    else:
        st.write(f"No organisms found for taxon '{selected_taxon}'.")