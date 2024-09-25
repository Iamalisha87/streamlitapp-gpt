import streamlit as st
import openai
from googletrans import Translator

# Set up OpenAI API key (replace with your key)
openai.api_key = 'your-openai-key'

# Create translator instance for regional language support
translator = Translator()

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Campus Event Campaigner", page_icon="📅", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://www.spjimr.org/wp-content/uploads/2023/08/220428-SPJIMR-Positive-Identity-CMYK.png")  # Add your organization logo here
    st.title("Event Campaign Generator")
    st.markdown("Create impactful campaign invitations for your club events.")
    st.markdown("---")
    st.subheader("Navigation")
    st.markdown("""
    - 📄 Generate Campaign
    - 🌐 Translate to Regional Language
    - 🎨 Generate Images
    """)
    st.markdown("---")
    st.info("Use this tool to quickly create professional campaigns and translate them into regional languages!")

# --- PAGE HEADER ---
st.title("📅 Campus Event Campaigner")
st.markdown("**Generate professional and attractive invitation campaigns for your college events!**")

# --- INPUT FORM ---
st.subheader("Input Event Details")

# Create columns for a structured layout
col1, col2 = st.columns(2)

with col1:
    club_name = st.text_input("Name of the Club", placeholder="E.g., Marketing Club")
    event_name = st.text_input("Name of the Event", placeholder="E.g., Marketing Strategy Workshop")
    event_date = st.date_input("Event Date")
    event_venue = st.text_input("Venue", placeholder="E.g., Auditorium, Main Campus")
    target_audience = st.text_input("Target Audience", placeholder="E.g., MBA Students, Marketing Enthusiasts")

with col2:
    club_brief = st.text_area("Brief about the Club", placeholder="Describe your club in a few lines.")
    event_description = st.text_area("Event Description", placeholder="Provide a brief about the event, its goals, and key highlights.")
    chief_guest = st.text_input("Name of the Chief Guest", placeholder="E.g., John Doe")
    chief_guest_designation = st.text_input("Designation of the Chief Guest", placeholder="E.g., CEO of ABC Corp.")

# --- TONE AND OPTIONAL NOTES ---
st.subheader("Additional Options")
col3, col4 = st.columns(2)

with col3:
    tone = st.selectbox("Select the Tone of the Campaign", ["Informative", "Exciting", "Formal", "Friendly", "Inspirational"])
    regional_language = st.selectbox("Translate to Regional Language", ["None", "Hindi", "Marathi", "Tamil", "Bengali"])

with col4:
    additional_notes = st.text_area("Additional Notes (Optional)", placeholder="Any specific instructions or notes to include?")
    generate_image = st.checkbox("Generate GenAI Picture for the Event")

# --- GENERATE CAMPAIGN FUNCTION ---
def generate_campaign(club_name, club_brief, event_name, event_description, chief_guest, chief_guest_designation, event_date, event_venue, target_audience, tone, additional_notes):
    prompt = f"""
    Create an event invitation for a college club.

    Club Name: {club_name}
    Brief: {club_brief}
    Event: {event_name}
    Description: {event_description}
    Chief Guest: {chief_guest}, {chief_guest_designation}
    Date: {event_date}
    Venue: {event_venue}
    Target Audience: {target_audience}
    Tone: {tone}
    Additional Notes: {additional_notes}

    Write an attractive and engaging campaign statement.
    """
    response = openai.Completion.create(
        engine="text-davinci-003",  # Or another GPT model
        prompt=prompt,
        max_tokens=300
    )
    return response.choices[0].text.strip()

# --- GENERATE IMAGE FUNCTION ---
def generate_event_image(event_name, event_description):
    dalle_prompt = f"Create a promotional image for an event called {event_name}. The event is about {event_description}."
    # Placeholder for image generation using DALL·E API
    return "https://via.placeholder.com/300.png?text=GenAI+Image+Here"

# --- TRANSLATION FUNCTION ---
def translate_text(text, language):
    translation = translator.translate(text, dest=language.lower())
    return translation.text

# --- GENERATE CAMPAIGN BUTTON ---
if st.button("Generate Campaign"):
    campaign = generate_campaign(club_name, club_brief, event_name, event_description, chief_guest, chief_guest_designation, event_date, event_venue, target_audience, tone, additional_notes)
    
    # Display the generated campaign
    st.subheader("Generated Campaign")
    st.write(campaign)

    # Optionally translate to regional language
    if regional_language != "None":
        translation = translate_text(campaign, regional_language)
        st.subheader(f"Translated Campaign ({regional_language})")
        st.write(translation)

    # Optionally generate and display an image
    if generate_image:
        image_url = generate_event_image(event_name, event_description)
        st.image(image_url, caption="Generated Event Image")

# --- FOOTER ---
st.markdown("---")
st.markdown("© 2024 SPJIMR Campus Event Campaigner")
