import streamlit as st
import pandas as pd

# Load datasets
@st.cache_data
def load_data():
    pokemon_df = pd.read_csv("Emerald Imperium Pokemon Data - Pokemon data.csv")
    location_df = pd.read_csv("Emerald Imperium Pokemon Data - Location data.csv")

    # Add Generation column
    def determine_generation(num):
        if num <= 151:
            return 1
        elif num <= 251:
            return 2
        elif num <= 386:
            return 3
        elif num <= 493:
            return 4
        elif num <= 649:
            return 5
        elif num <= 721:
            return 6
        elif num <= 809:
            return 7
        elif num <= 898:
            return 8
        else:
            return 9

    pokemon_df["Generation"] = pokemon_df["Number"].apply(determine_generation)
    return pokemon_df, location_df

pokemon_df, location_df = load_data()

st.set_page_config(page_title="Emerald Imperium Locations", layout="wide")
st.title("Emerald Imperium Pokémon Locations")
st.markdown("Search for a Pokémon or a Location to find where and at what levels it can be encountered.")

# Sidebar for stat filters
st.sidebar.header("Stat Filters")
hp_range = st.sidebar.slider("HP", 0, 255, (0, 255))
attack_range = st.sidebar.slider("Attack", 0, 190, (0, 190))
defense_range = st.sidebar.slider("Defense", 0, 230, (0, 230))
spatk_range = st.sidebar.slider("Sp. Attack", 0, 194, (0, 194))
spdef_range = st.sidebar.slider("Sp. Defense", 0, 230, (0, 230))
speed_range = st.sidebar.slider("Speed", 0, 180, (0, 180))

# Layout: Filters in columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Pokémon Filters")
    selected_pokemon = st.selectbox("Pokémon", ["All"] + sorted(pokemon_df["Name"].unique().tolist()))
    type1_filter = st.multiselect("Type 1", sorted(pokemon_df["Type 1"].dropna().unique()))
    type2_filter = st.multiselect("Type 2", sorted(pokemon_df["Type 2"].dropna().unique()))
    gen_filter = st.multiselect("Generation", sorted(pokemon_df["Generation"].unique()))

with col2:
    st.subheader("Location Filters")
    selected_location = st.selectbox("Location", ["All"] + sorted(location_df["Area"].unique().tolist()))
    method_filter = st.multiselect("Method", sorted(location_df["Method"].dropna().unique()))
    min_level, max_level = st.slider("Level Range", 1, 100, (1, 100))

# Filter Pokémon data
filtered_pokemon = pokemon_df[
    (pokemon_df["HP"].between(*hp_range)) &
    (pokemon_df["Attack"].between(*attack_range)) &
    (pokemon_df["Defense"].between(*defense_range)) &
    (pokemon_df["Sp.Attack"].between(*spatk_range)) &
    (pokemon_df["Sp.Defense"].between(*spdef_range)) &
    (pokemon_df["Speed"].between(*speed_range))
]

if type1_filter:
    filtered_pokemon = filtered_pokemon[filtered_pokemon["Type 1"].isin(type1_filter)]
if type2_filter:
    filtered_pokemon = filtered_pokemon[filtered_pokemon["Type 2"].isin(type2_filter)]
if gen_filter:
    filtered_pokemon = filtered_pokemon[filtered_pokemon["Generation"].isin(gen_filter)]
if selected_pokemon != "All":
    filtered_pokemon = filtered_pokemon[filtered_pokemon["Name"] == selected_pokemon]

# Filter location data
filtered_locations = location_df.copy()

if selected_location != "All":
    filtered_locations = filtered_locations[filtered_locations["Area"] == selected_location]
if method_filter:
    filtered_locations = filtered_locations[filtered_locations["Method"].isin(method_filter)]

filtered_locations = filtered_locations[
    (filtered_locations["Min Level"] >= min_level) &
    (filtered_locations["Max Level"] <= max_level)
]

# Cross-reference Pokémon
filtered_locations = filtered_locations[filtered_locations["Pokémon"].isin(filtered_pokemon["Name"])]

# Display results
st.subheader("Filtered Pokémon")
st.dataframe(filtered_pokemon.sort_values("Number"))

st.subheader("Filtered Encounter Locations")
st.dataframe(filtered_locations.sort_values(["Area", "Method", "Pokémon"]))
