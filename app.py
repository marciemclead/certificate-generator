import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ====== PAGE CONFIG ======
st.set_page_config(page_title="Certificate Generator", page_icon="🎓", layout="wide")

# ====== CUSTOM STYLING FOR RESPONSIVENESS ======
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {padding: 1rem;}
    .stTextInput, .stButton, .stDownloadButton {width: 100% !important;}
    img {max-width: 100%; height: auto;}
    @media (max-width: 768px) {h1, h2, h3 {font-size: 1.2rem !important;}}
    </style>
""", unsafe_allow_html=True)

# ====== TITLE ======
st.title("🎓 Online Certificate Generator")
st.caption("Made by **Tanvir Even** | Mobile & PC Compatible")

# ====== ADMIN CONFIGURATION ======
ADMIN_PASSWORD = "12345"  # Change this password
NAME_X, NAME_Y = 930, 730  # Fixed text position

# ====== SESSION STATE SETUP ======
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "template_bytes" not in st.session_state:
    st.session_state.template_bytes = None
if "font_file" not in st.session_state:
    st.session_state.font_file = None
if "font_size" not in st.session_state:
    st.session_state.font_size = 280
if "font_color" not in st.session_state:
    st.session_state.font_color = "#000000"

# ====== SIDEBAR (ADMIN PANEL) ======
with st.sidebar:
    st.header("⚙️ Admin Panel")

    if not st.session_state.authenticated:
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("🔓 Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Logged in successfully!")
            else:
                st.error("❌ Incorrect password!")
    else:
        st.success("🔐 Admin Access Granted")

        uploaded_template = st.file_uploader("Upload Certificate Template", type=["jpg", "jpeg", "png"])
        if uploaded_template:
            st.session_state.template_bytes = uploaded_template.read()
            st.success("✅ Template uploaded and saved!")

        font_file = st.file_uploader("Upload Font (.ttf)", type=["ttf"])
        if font_file:
            st.session_state.font_file = font_file
            st.success("✅ Font uploaded!")

        st.session_state.font_size = st.slider("Font Size", 20, 200, st.session_state.font_size)
        st.session_state.font_color = st.color_picker("Font Color", st.session_state.font_color)

        if st.button("🗑️ Remove Uploaded Template"):
            st.session_state.template_bytes = None
            st.warning("❌ Template removed!")

        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.info("Logged out successfully!")

        st.markdown("---")
        st.caption("👨‍💻 Developed by **Tanvir Even**")

# ====== USER SECTION ======
if st.session_state.template_bytes:
    st.subheader("✏️ Generate Your Certificate")
    user_name = st.text_input("Enter Your Full Name")

    if st.button("✨ Generate Certificate"):
        if not user_name.strip():
            st.warning("Please enter your name!")
        else:
            # Load template from session
            template = Image.open(io.BytesIO(st.session_state.template_bytes))
            cert = template.copy()
            draw = ImageDraw.Draw(cert)

            # Load font properly
            if st.session_state.font_file:
                font = ImageFont.truetype(st.session_state.font_file, st.session_state.font_size)
            else:
                try:
                    font = ImageFont.truetype("arial.ttf", st.session_state.font_size)
                except:
                    font = ImageFont.load_default()

            # Draw the text
            draw.text((NAME_X, NAME_Y), user_name, font=font, fill=st.session_state.font_color)

            # Convert to PDF
            pdf_bytes = io.BytesIO()
            cert_rgb = cert.convert("RGB")
            cert_rgb.save(pdf_bytes, format="PDF")
            pdf_bytes.seek(0)

            # Show the certificate preview (AFTER name entered)
            st.image(cert, caption=f"Certificate for {user_name}", use_container_width=True)

            # Download button
            st.download_button(
                label="📥 Download Certificate (PDF)",
                data=pdf_bytes,
                file_name=f"{user_name}_certificate.pdf",
                mime="application/pdf"
            )
else:
    st.warning("⚠️ No certificate uploaded yet. Please ask the admin to upload one.")


