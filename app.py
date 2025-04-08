import streamlit as st
import pandas as pd

st.set_page_config(page_title="Emerald Imperium Locations", layout="wide")

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

st.title("Emerald Imperium Pokémon Locations")

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

# Filter location data first to use in filtering Pokémon
filtered_locations = location_df.copy()

if selected_location != "All":
    filtered_locations = filtered_locations[filtered_locations["Area"] == selected_location]
if method_filter:
    filtered_locations = filtered_locations[
        filtered_locations["Method"].str.strip().isin([m.strip() for m in method_filter])
    ]

filtered_locations = filtered_locations[
    (filtered_locations["Min Level"] >= min_level) &
    (filtered_locations["Max Level"] <= max_level)
]

# Normalize name for filtering
normalized_location_names = filtered_locations["Pokémon"].str.strip().str.lower().unique()

# Filter Pokémon data
filtered_pokemon = pokemon_df.copy()

if type1_filter:
    filtered_pokemon = filtered_pokemon[filtered_pokemon["Type 1"].isin(type1_filter)]
if type2_filter:
    filtered_pokemon = filtered_pokemon[filtered_pokemon["Type 2"].isin(type2_filter)]
if gen_filter:
    filtered_pokemon = filtered_pokemon[filtered_pokemon["Generation"].isin(gen_filter)]
if selected_pokemon != "All":
    filtered_pokemon = filtered_pokemon[filtered_pokemon["Name"] == selected_pokemon]

# Remove duplicate Pokémon entries by Name + Form
filtered_pokemon = (
    filtered_pokemon
    .assign(Form=filtered_pokemon["Form"].fillna("").str.strip())
    .drop_duplicates(subset=["Name", "Form"])
)

# Now cross-reference only Pokémon that exist in the filtered location data
filtered_pokemon = filtered_pokemon[
    filtered_pokemon["Name"].str.strip().str.lower().isin(normalized_location_names)
]


# Display results
st.subheader("Filtered Pokémon and Encounter Locations")

# Tag color mapping
method_colors = {
    "Grass": "#4CAF50",
    "Old Rod": "#FFD700",
    "Good Rod": "#20B2AA",
    "Super Rod": "#9370DB",
    "Surfing": "#1E90FF",
    "Cave": "#D2B48C",
    "Dungeon": "#B22222"
}

def render_tag(content, color):
    return f"<span style='display:inline-block; background:{color}; color:#fff; padding:3px 10px; border-radius:10px; margin:4px; font-size:0.85em;'>{content}</span>"

def render_gray_tag(content):
    return render_tag(content, '#555')

if filtered_pokemon.empty:
    st.write("No Pokémon match your filters.")
else:
    num_columns = 3
    chunks = [filtered_pokemon.iloc[i:i + num_columns] for i in range(0, len(filtered_pokemon), num_columns)]

    for chunk in chunks:
        cols = st.columns(len(chunk))
        for idx, (i, row) in enumerate(chunk.iterrows()):
            with cols[idx]:
                locs = filtered_locations[
                    filtered_locations["Pokémon"].str.strip().str.lower() == row["Name"].strip().lower()
                ]

                tag_blocks = []
                for _, loc in locs.iterrows():
                    area_tag = render_gray_tag(loc['Area'])
                    method_tag = render_tag(loc['Method'], method_colors.get(loc['Method'], '#888'))
                    level_tag = render_gray_tag(f"Level {int(loc['Min Level'])}–{int(loc['Max Level'])}")
                    block = f"<div style='display:flex; flex-wrap:wrap; gap:6px; margin-bottom:6px;'>{area_tag}{method_tag}{level_tag}</div>"
                    tag_blocks.append(block)

                bubble_content = f"""
                <div style='background-color:#1e1e1e; border:1px solid #444; padding:15px; border-radius:10px; margin-bottom:20px;'>
                    <h4 style='margin-bottom:10px;'>{row['Name']}</h4>
                    {''.join(tag_blocks)}
                </div>
                """
                st.markdown(bubble_content, unsafe_allow_html=True)
