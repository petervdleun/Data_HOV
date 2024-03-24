import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize session state
if 'match_data' not in st.session_state:
    st.session_state['match_data'] = pd.DataFrame(columns=["Speler", "Actie"])

# Define the list of player names and actions
player_names = ["Broekie", "Cas", "Clusky", "Floep", "Frans", "Jordi", "Kennard", "Melle", "Noah", "Stevert", "Tony", "Twan",
                "Van Zon", "William", "Wytze", "Youri"]
actions = ["Succesvolle Pass", "Onsuccesvolle Pass", "Schot Assist", "Schot", "Balverovering", "Onderschepping", "Overtreding"]

def main():
    st.title("HOV/DJSCR 7 - CVV Zwervers 5")

    # Sidebar with tabs
    tab = st.sidebar.radio("Tabs", ["Input", "Output", "Visualisatie"])

    if tab == "Input":
        input_tab()
    elif tab == "Output":
        output_tab()
    elif tab == "Visualisatie":
        visualization_tab()

def input_tab():
    # Data input section
    col1, col2, col3 = st.columns([2, 2, 2])  # Split the screen into three columns

    with col1:
        # Data input section
        selected_player = st.radio("Speler", player_names)

    with col2:
        # Data input section
        selected_action = st.radio("Actie", actions)

        if st.button("Invoer", type='primary'):
            # Save data to the session state
            save_match_data(selected_player, selected_action)
            st.success("Data submitted successfully!")

def output_tab():
    edited_data = st.data_editor(st.session_state['match_data'], num_rows="dynamic")
    
    if edited_data is not None:
        st.session_state['match_data'] = edited_data
    
    csv = convert_df(st.session_state['match_data'])

    st.download_button(
    "Download CSV", csv, "wedstrijd_data.csv", "text/csv", key='download-csv'
    )

def visualization_tab():
    # Select action for visualization
    selected_action = st.selectbox("Actie", actions)

    # Filter data for selected action
    filtered_data = st.session_state['match_data'][st.session_state['match_data']['Actie'] == selected_action]

    # Group data by player and count occurrences
    player_counts = filtered_data['Speler'].value_counts()

    # Sort players by count
    sorted_players = player_counts.sort_values(ascending=False)

    # Create a DataFrame for visualization and drop the index
    df_vis = pd.DataFrame({"Speler": sorted_players.index, "Aantal": sorted_players.values}).reset_index(drop=True)

    # Color scale for highlighting counts
    cm = sns.color_palette("crest", as_cmap=True)

    # Highlight counts in the table
    st.dataframe(df_vis.style.background_gradient(cmap=cm, subset=["Aantal"]))

def save_match_data(player, action):
    # Create a new DataFrame by concatenating the existing one with the new data
    new_data = pd.DataFrame({"Speler": [player], "Actie": [action]})
    st.session_state['match_data'] = pd.concat([st.session_state['match_data'], new_data], ignore_index=True)

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')



if __name__ == "__main__":
    main()
