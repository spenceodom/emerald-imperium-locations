import streamlit as st
import pandas as pd

st.set_page_config(page_title="Emerald Imperium Locations", layout="wide")

# --- Global CSS Styles ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        /* background-color: #121212; */ /* Uncomment if not using Streamlit's dark theme & want a dark page */
        color: #E0E0E0; /* Default text color for better readability on dark backgrounds */
    }

    /* Style Streamlit's main block for consistency if needed */
    /* .main .block-container {
        background-color: #1a1a1a;
        border-radius: 10px;
        padding: 2rem;
    } */

    h1, h2, h3, h4, h5, h6 {
        color: #FAFAFA; /* Lighter headings for dark backgrounds */
    }
    
    /* Specific styling for the app title if default h1 is too much */
    .app-title { /* You would add class="app-title" to st.title if using custom class */
        /* color: #4CAF50; */ /* Example custom title color */
    }

    .pokemon-card {
        background-color: #1e1e1e;
        border: 1px solid #555; /* Slightly lighter border */
        padding: 20px; /* Increased padding for more space */
        border-radius: 12px; /* Slightly more rounded corners */
        margin-bottom: 20px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.3);
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        text-align: center; /* Center h4 and tag blocks container */
        display: flex; /* Use flex to manage height if needed, or for vertical centering */
        flex-direction: column; /* Stack h4 and tag blocks vertically */
        justify-content: space-between; /* Pushes content apart if card height is fixed/min-height */
        height: 100%; /* Make cards in a row take up the same height */
    }

    .pokemon-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px 0 rgba(0,0,0,0.4);
    }

    .pokemon-card h4 {
        margin-top: 0; /* Remove default top margin from h4 if it's the first child */
        margin-bottom: 15px; /* More space below name */
        font-size: 1.3em; /* Slightly larger name */
        color: #EAEAEA;
    }
    
    .tag-container { /* Container for individual tag blocks */
        /* No specific styles needed now unless further refinement */
    }

    .tag-block { /* The div that holds Area, Method, Level tags */
        display: flex;
        justify-content: space-between;
        flex-wrap: nowrap;
        gap: 6px;
        margin-bottom: 8px; /* Space between encounter lines */
        width: 100%;
    }

    .tag { /* Individual tags (Area, Method, Level) */
        display: inline-block;
        color: #fff;
        padding: 5px 12px; /* Increased padding in tags */
        border-radius: 15px; /* More rounded tags */
        margin: 2px; /* Reduced margin as gap in .tag-block handles spacing */
        font-size: 0.8em; /* Slightly smaller tag font for more content */
        text-shadow: 1px 1px 1px rgba(0,0,0,0.5); /* Text shadow for pop */
        white-space: nowrap; /* Prevent tags from breaking lines */
    }
    </style>
""", unsafe_allow_html=True)


# Load datasets
@st.cache_data
def load_data():
    pokemon_df = pd.read_csv("Emerald Imperium Pokemon Data - Pokemon data.csv")
    location_df = pd.read_csv("Emerald Imperium Pokemon Data - Location data.csv")

    def determine_generation(num):
        if num <= 151: return 1
        elif num <= 251: return 2
        elif num <= 386: return 3
        elif num <= 493: return 4
        elif num <= 649: return 5
        elif num <= 721: return 6
        elif num <= 809: return 7
        elif num <= 898: return 8
        else: return 9
    pokemon_df["Generation"] = pokemon_df["Number"].apply(determine_generation)
    return pokemon_df, location_df

pokemon_df, location_df = load_data()
pokemon_df = pokemon_df[~pokemon_df["Form"].str.lower().str.contains("mega", na=False)]

level_cap_data = {
    "No Cap": 101, "Pre Roxanne (Cap 15)": 15, "Pre May (Rustboro) (Cap 20)": 20,
    "Pre Brawley (Cap 25)": 25, "Pre Ocean Museum (Cap 30)": 30, "Pre May (Route 110) (Cap 32)": 32,
    "Pre Wattson (Cap 34)": 34, "Pre Maxie (Mt Chimney) (Cap 44)": 44, "Pre Flannery (Cap 47)": 47,
    "Pre Trick House (Cap 56)": 56, "Pre Norman (Cap 59)": 59, "Pre May (Route 119) (Cap 64)": 64,
    "Pre Winona (Cap 68)": 68, "Pre Dawn (Lilycove) (Cap 71)": 71, "Pre Aqua Boss (Cap 74)": 74,
    "Pre Tate and Liza (Cap 76)": 76, "Pre Archie (Cap 80)": 80, "Pre Juan (Cap 82)": 82,
    "Pre Wally (Victory Road) (Cap 84)": 84, "Pre Elite Four (Cap 85)": 85,
}

st.title("Emerald Imperium Pokémon Locations")
# st.markdown("<br>", unsafe_allow_html=True) # Optional: More space below title

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
    selected_level_cap_key = st.selectbox("Level Cap", list(level_cap_data.keys()))
    current_level_cap = level_cap_data[selected_level_cap_key]

# --- Divider between filters and results ---
st.divider()

filtered_locations = location_df.copy()
if selected_location != "All":
    filtered_locations = filtered_locations[filtered_locations["Area"] == selected_location]
if method_filter:
    filtered_locations = filtered_locations[filtered_locations["Method"].str.strip().isin([m.strip() for m in method_filter])]
filtered_locations = filtered_locations[(filtered_locations["Min Level"] >= min_level) & (filtered_locations["Max Level"] <= max_level)]
filtered_locations = filtered_locations[filtered_locations["Max Level"] <= current_level_cap]

normalized_location_names = filtered_locations["Pokémon"].str.strip().str.lower().unique()

filtered_pokemon = pokemon_df.copy()
if type1_filter:
    filtered_pokemon = filtered_pokemon[filtered_pokemon["Type 1"].isin(type1_filter)]
if type2_filter:
    filtered_pokemon = filtered_pokemon[filtered_pokemon["Type 2"].isin(type2_filter)]
if gen_filter:
    filtered_pokemon = filtered_pokemon[filtered_pokemon["Generation"].isin(gen_filter)]
if selected_pokemon != "All":
    filtered_pokemon = filtered_pokemon[filtered_pokemon["Name"] == selected_pokemon]

filtered_pokemon = (
    filtered_pokemon
    .assign(Form=filtered_pokemon["Form"].fillna("").str.strip())
    .drop_duplicates(subset=["Name", "Form"])
)
filtered_pokemon = filtered_pokemon[filtered_pokemon["Name"].str.strip().str.lower().isin(normalized_location_names)]

st.subheader("Filtered Pokémon and Encounter Locations")

method_colors = {
    "Grass": "#4CAF50", "Old Rod": "#FFD700", "Good Rod": "#20B2AA", "Super Rod": "#9370DB",
    "Surfing": "#1E90FF", "Cave": "#D2B48C", "Dungeon": "#B22222", "Gift": "#FF69B4", "Egg": "#FFC0CB"
    # Added Gift and Egg examples, adjust as needed
}

# --- Updated Tag Rendering Function ---
def render_tag_html(content, color):
    # Uses the 'tag' class from the global CSS
    return f"<span class='tag' style='background:{color};'>{content}</span>"

def render_gray_tag_html(content):
    return render_tag_html(content, '#555') # Using a specific gray for these tags

if filtered_pokemon.empty:
    # --- Updated No Results Message ---
    st.info("No Pokémon match your current filter criteria. Try adjusting your selections!")
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

                tag_html_blocks = []
                for _, loc in locs.iterrows():
                    area_tag = render_gray_tag_html(loc['Area'])
                    method_tag = render_tag_html(loc['Method'], method_colors.get(loc['Method'], '#888')) # Default color if method not in dict
                    level_tag = render_gray_tag_html(f"Lvl {int(loc['Min Level'])}–{int(loc['Max Level'])}") # Shortened "Level"
                    
                    # Uses the 'tag-block' class from global CSS for alignment
                    block = f"<div class='tag-block'>{area_tag}{method_tag}{level_tag}</div>"
                    tag_html_blocks.append(block)

                # --- Updated Bubble Content to use CSS classes ---
                bubble_content = f"""
                <div class='pokemon-card'>
                    <h4>{row['Name']}</h4>
                    <div class='tag-container'>
                        {''.join(tag_html_blocks)}
                    </div>
                </div>
                """
                st.markdown(bubble_content, unsafe_allow_html=True)
