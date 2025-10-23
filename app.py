import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ====== PAGE CONFIG ======
st.set_page_config(page_title="Certificate Generator", page_icon="🎓", layout="wide")

st.markdown(
    """
    <style>
    /* Make layout responsive */
    [data-testid="stAppViewContainer"] {
        padding: 1rem;
    }
    img {
        max-width: 100%;
        height: auto;
    }
    .stTextInput, .stDownloadButton, .stButton {
        width: 100% !important;
    }
    @media (max-width: 768px) {
        h1, h2, h3, h4 {
            font-size: 1.2rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎓 Online Certificate Generator")
st.caption("Made by **Tanvir Even** | Works on both PC and Mobile 📱💻")

# ====== PASSWORD-PROTECTED ADMIN SECTION ======
ADMIN_PASSWORD = "12345"  # change this password

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "template" not in st.session_state:
    st.session_state.template = None
if "font_file" not in st.session_state:
    st.session_state.font_file = None
if "font_size" not in st.session_state:
    st.session_state.font_size = 60
if "font_color" not in st.session_state:
    st.session_state.font_color = "#000000"

with st.sidebar:
    st.header("⚙️ Admin Panel")
    if not st.session_state.authenticated:
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("Login"):
            if password == ADMIN_PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Logged in successfully!")
            else:
                st.error("❌ Incorrect password!")
    else:
        st.success("🔐 Admin Access Granted")

        template_file = st.file_uploader("Upload Certificate Template", type=["jpg", "jpeg", "png"])
        if template_file:
            st.session_state.template = Image.open(template_file)
            st.success("✅ Template uploaded successfully and saved!")

        font_file = st.file_uploader("Upload Font (.ttf)", type=["ttf"])
        if font_file:
            st.session_state.font_file = font_file
            st.success("✅ Font uploaded successfully!")

        st.session_state.font_size = st.slider("Font Size", 20, 200, st.session_state.font_size)
        st.session_state.font_color = st.color_picker("Font Color", st.session_state.font_color)
        st.write("Position fixed: X=590, Y=470")

        if st.button("🗑️ Remove Uploaded Template"):
            st.session_state.template = None
            st.warning("Template removed!")

        st.markdown("---")
        st.write("👨‍💻 Developed by **Tanvir Even**")
        if st.button("Logout"):
            st.session_state.authenticated = False

# ====== USER SECTION ======
if st.session_state.template:
    st.subheader("✏️ Generate Your Certificate")
    user_name = st.text_input("Enter Your Full Name")

    if st.button("✨ Generate Certificate"):
        if user_name.strip() == "":
            st.warning("Please enter your name!")
        else:
            # Use stored template
            cert = st.session_state.template.copy()
            draw = ImageDraw.Draw(cert)

            # Load font
            if st.session_state.font_file:
                font = ImageFont.truetype(st.session_state.font_file, st.session_state.font_size)
            else:
                try:
                    font = ImageFont.truetype("arial.ttf", st.session_state.font_size)
                except:
                    font = ImageFont.load_default()

            # Position name
            x_pos, y_pos = 590, 470
            draw.text((x_pos, y_pos), user_name, font=font, fill=st.session_state.font_color)

            # Preview
            st.image(cert, caption=f"Preview for {user_name}", use_container_width=True)

            # Convert to PDF
            pdf_bytes = io.BytesIO()
            cert_rgb = cert.convert("RGB")
            cert_rgb.save(pdf_bytes, format="PDF")
            pdf_bytes.seek(0)

            # Download button
            st.download_button(
                label="📥 Download Certificate (PDF)",
                data=pdf_bytes,
                file_name=f"{user_name}_certificate.pdf",
                mime="application/pdf"
            )
else:
    st.warning("⚠️ No certificate template uploaded yet. Admin must upload one first.")
