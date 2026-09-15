import streamlit as st
# streamlit run streamlit_app.py


def main():

#>>>>>>>>>>>>>>>>>>>>> Streamlit page
    st.set_page_config(
        page_title="LVR compta",
        page_icon="🧾",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title('La Vilaine Compta ')

    st.header("Outil de Data Viz pour les comptes de l'association")

    st.markdown("""
    blablabla          
    """)


if __name__ == "__main__":
    main()