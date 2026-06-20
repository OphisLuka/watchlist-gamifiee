"""
Watchlist gamifiee -- Films, Series, Mangas, Animes
------------------------------------------------------------------
Application Streamlit permettant de :
1. Ajouter des oeuvres a verifier (idee a explorer)
2. Les faire progresser dans un workflow a 4 statuts :
   A verifier -> A regarder -> Termine (ou Ecarte)
3. Gagner de l'experience (XP) et monter en rang de cinephile en
   terminant des oeuvres
4. Filtrer, trier et noter ses oeuvres, marquer des favoris

Lancement : streamlit run app.py
"""

import pandas as pd
import streamlit as st
import os
import uuid
from datetime import datetime

FICHIER_DONNEES = "watchlist.csv"
COLONNES = [
    "id", "titre", "type_oeuvre", "genre", "statut",
    "date_ajout", "date_terminee", "note", "favori", "commentaire"
]

STATUTS = ["A verifier", "A regarder", "Termine", "Ecarte"]
TYPES_OEUVRE = ["Film", "Serie", "Manga", "Anime", "Autre"]
GENRES = ["Action", "Aventure", "Comedie", "Drame", "Fantastique",
          "Horreur", "Romance", "Science-fiction", "Slice of life",
          "Thriller", "Documentaire", "Autre"]

# XP fixe attribue selon le type d'oeuvre, a la complétion
XP_PAR_TYPE = {
    "Film": 10,
    "Serie": 30,
    "Manga": 20,
    "Anime": 25,
    "Autre": 15,
}

# Paliers de rang (XP cumule necessaire pour atteindre le rang)
RANGS = [
    (0, "Spectateur occasionnel", "🍿"),
    (50, "Curieux culturel", "🎬"),
    (150, "Cinephile en herbe", "🎞️"),
    (300, "Cinephile confirme", "🏆"),
    (600, "Critique averti", "🌟"),
    (1000, "Encyclopedie vivante", "👑"),
    (1800, "Legende du visionnage", "💎"),
]

st.set_page_config(page_title="Watchlist", layout="wide", page_icon="🎬")


# ----------------------------------------------------------------------
# FONCTIONS UTILITAIRES : charger / sauvegarder les donnees
# ----------------------------------------------------------------------
def charger_donnees():
    if os.path.exists(FICHIER_DONNEES):
        # dtype=str force toutes les colonnes en texte au chargement, pour
        # éviter qu'une colonne vide au départ (ex: date_terminee) soit
        # devinée comme un nombre (float) par pandas, ce qui empêcherait
        # d'y écrire une vraie date plus tard.
        df = pd.read_csv(FICHIER_DONNEES, dtype=str)
        for col in COLONNES:
            if col not in df.columns:
                df[col] = None
        # Reconversion des colonnes qui doivent vraiment être numériques/booléennes
        if "note" in df.columns:
            df["note"] = pd.to_numeric(df["note"], errors="coerce")
        if "favori" in df.columns:
            df["favori"] = df["favori"].map({"True": True, "False": False, True: True, False: False}).fillna(False)
        return df
    return pd.DataFrame(columns=COLONNES)


def sauvegarder_donnees(df):
    df.to_csv(FICHIER_DONNEES, index=False)


def ajouter_oeuvre(titre, type_oeuvre, genre, commentaire):
    df = charger_donnees()
    nouvelle = pd.DataFrame([{
        "id": str(uuid.uuid4())[:8],
        "titre": titre,
        "type_oeuvre": type_oeuvre,
        "genre": genre,
        "statut": "A verifier",
        "date_ajout": datetime.now().strftime("%Y-%m-%d"),
        "date_terminee": "",
        "note": None,
        "favori": False,
        "commentaire": commentaire,
    }])
    df = pd.concat([df, nouvelle], ignore_index=True)
    sauvegarder_donnees(df)


def changer_statut(id_oeuvre, nouveau_statut):
    df = charger_donnees()
    df.loc[df["id"] == id_oeuvre, "statut"] = nouveau_statut
    if nouveau_statut == "Termine":
        df.loc[df["id"] == id_oeuvre, "date_terminee"] = datetime.now().strftime("%Y-%m-%d")
    sauvegarder_donnees(df)


def mettre_a_jour_note(id_oeuvre, note):
    df = charger_donnees()
    df.loc[df["id"] == id_oeuvre, "note"] = note
    sauvegarder_donnees(df)


def basculer_favori(id_oeuvre):
    df = charger_donnees()
    valeur_actuelle = df.loc[df["id"] == id_oeuvre, "favori"].values[0]
    df.loc[df["id"] == id_oeuvre, "favori"] = not bool(valeur_actuelle)
    sauvegarder_donnees(df)


def supprimer_oeuvre(id_oeuvre):
    df = charger_donnees()
    df = df[df["id"] != id_oeuvre]
    sauvegarder_donnees(df)


# ----------------------------------------------------------------------
# SYSTEME XP / RANG
# ----------------------------------------------------------------------
def calculer_xp_total(df):
    terminees = df[df["statut"] == "Termine"]
    if terminees.empty:
        return 0
    return int(terminees["type_oeuvre"].map(XP_PAR_TYPE).fillna(15).sum())


def calculer_rang(xp_total):
    """Renvoie (nom_rang, emoji, xp_actuel_palier, xp_prochain_palier) selon l'XP total."""
    rang_actuel = RANGS[0]
    prochain_rang = None
    for i, (seuil, nom, emoji) in enumerate(RANGS):
        if xp_total >= seuil:
            rang_actuel = (seuil, nom, emoji)
            prochain_rang = RANGS[i + 1] if i + 1 < len(RANGS) else None
        else:
            break
    return rang_actuel, prochain_rang


# ----------------------------------------------------------------------
# BARRE LATERALE : ajout d'une oeuvre
# ----------------------------------------------------------------------
st.sidebar.header("➕ Ajouter une œuvre à vérifier")
with st.sidebar.form("formulaire_ajout", clear_on_submit=True):
    titre = st.text_input("Titre")
    type_oeuvre = st.selectbox("Type", TYPES_OEUVRE)
    genre = st.selectbox("Genre principal", GENRES)
    commentaire = st.text_area("Note / pourquoi ça t'intéresse (optionnel)", height=80)
    valider = st.form_submit_button("Ajouter à \"À vérifier\"")

    if valider:
        if not titre.strip():
            st.sidebar.error("Le titre ne peut pas être vide.")
        else:
            ajouter_oeuvre(titre.strip(), type_oeuvre, genre, commentaire.strip())
            st.sidebar.success(f"« {titre} » ajouté à vérifier !")

st.sidebar.markdown("---")
st.sidebar.caption(
    "Les données sont enregistrées localement dans 'watchlist.csv'. "
    "Rien n'est envoyé en ligne."
)

# ----------------------------------------------------------------------
# CONTENU PRINCIPAL : EN-TÊTE + XP/RANG
# ----------------------------------------------------------------------
st.title("🎬 Ma Watchlist")
st.caption("Films, séries, mangas, animés — organise ce que tu veux regarder, et progresse en rang de cinéphile.")

df = charger_donnees()
xp_total = calculer_xp_total(df)
(seuil_actuel, nom_rang, emoji_rang), prochain = calculer_rang(xp_total)

col_rang, col_xp = st.columns([1, 2])
with col_rang:
    st.metric("Rang actuel", f"{emoji_rang} {nom_rang}")
with col_xp:
    if prochain:
        seuil_prochain, nom_prochain, emoji_prochain = prochain
        xp_restant = seuil_prochain - xp_total
        progression = (xp_total - seuil_actuel) / (seuil_prochain - seuil_actuel)
        st.progress(min(max(progression, 0), 1.0),
                    text=f"{xp_total} XP — encore {xp_restant} XP avant {emoji_prochain} {nom_prochain}")
    else:
        st.progress(1.0, text=f"{xp_total} XP — rang maximum atteint !")

st.markdown("---")

# ----------------------------------------------------------------------
# FILTRES
# ----------------------------------------------------------------------
with st.expander("🔍 Filtres et tri", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filtre_type = st.multiselect("Type", TYPES_OEUVRE)
    with col2:
        filtre_genre = st.multiselect("Genre", GENRES)
    with col3:
        filtre_favori = st.checkbox("Favoris uniquement")
    with col4:
        tri = st.selectbox("Trier par", ["Date d'ajout (récent)", "Date d'ajout (ancien)", "Titre (A-Z)", "Note (meilleure)"])

# ----------------------------------------------------------------------
# AFFICHAGE D'UNE CATEGORIE (fonction reutilisable)
# ----------------------------------------------------------------------
def appliquer_filtres_et_tri(sous_df):
    if filtre_type:
        sous_df = sous_df[sous_df["type_oeuvre"].isin(filtre_type)]
    if filtre_genre:
        sous_df = sous_df[sous_df["genre"].isin(filtre_genre)]
    if filtre_favori:
        sous_df = sous_df[sous_df["favori"] == True]

    if tri == "Date d'ajout (récent)":
        sous_df = sous_df.sort_values("date_ajout", ascending=False)
    elif tri == "Date d'ajout (ancien)":
        sous_df = sous_df.sort_values("date_ajout", ascending=True)
    elif tri == "Titre (A-Z)":
        sous_df = sous_df.sort_values("titre")
    elif tri == "Note (meilleure)":
        sous_df = sous_df.sort_values("note", ascending=False, na_position="last")
    return sous_df


def afficher_carte(row):
    favori_icone = "⭐" if row["favori"] else "☆"
    titre_affiche = f"{favori_icone} **{row['titre']}** · {row['type_oeuvre']} · {row['genre']}"
    with st.container(border=True):
        col_info, col_actions = st.columns([3, 2])
        with col_info:
            st.markdown(titre_affiche)
            if row.get("commentaire"):
                st.caption(row["commentaire"])
            if row["statut"] == "Termine" and pd.notna(row.get("note")):
                st.caption(f"Note : {'⭐' * int(row['note'])} ({int(row['note'])}/5)")

        with col_actions:
            sous_col1, sous_col2, sous_col3 = st.columns(3)

            if row["statut"] == "A verifier":
                if sous_col1.button("✅ Intéressant", key=f"valide_{row['id']}", help="Passer à « À regarder »"):
                    changer_statut(row["id"], "A regarder")
                    st.rerun()
                if sous_col2.button("🗑️ Écarter", key=f"ecarte_{row['id']}"):
                    changer_statut(row["id"], "Ecarte")
                    st.rerun()

            elif row["statut"] == "A regarder":
                if sous_col1.button("🏁 Terminé", key=f"fini_{row['id']}"):
                    changer_statut(row["id"], "Termine")
                    st.rerun()
                if sous_col2.button("↩️ À vérifier", key=f"retour_{row['id']}"):
                    changer_statut(row["id"], "A verifier")
                    st.rerun()

            elif row["statut"] == "Termine":
                fav_label = "💔 Retirer" if row["favori"] else "⭐ Favori"
                if sous_col1.button(fav_label, key=f"fav_{row['id']}"):
                    basculer_favori(row["id"])
                    st.rerun()

            elif row["statut"] == "Ecarte":
                if sous_col1.button("↩️ Réessayer", key=f"reessaye_{row['id']}"):
                    changer_statut(row["id"], "A verifier")
                    st.rerun()

            if sous_col3.button("❌ Supprimer", key=f"suppr_{row['id']}"):
                supprimer_oeuvre(row["id"])
                st.rerun()

        if row["statut"] == "Termine" and not pd.notna(row.get("note")):
            note_donnee = st.feedback("stars", key=f"note_{row['id']}")
            if note_donnee is not None:
                mettre_a_jour_note(row["id"], note_donnee + 1)
                st.rerun()


# ----------------------------------------------------------------------
# ONGLETS PAR STATUT
# ----------------------------------------------------------------------
if df.empty:
    st.info("Ta watchlist est vide pour le moment. Ajoute ta première œuvre dans le menu de gauche !")
else:
    onglet_verifier, onglet_regarder, onglet_termine, onglet_ecarte = st.tabs([
        f"🔎 À vérifier ({len(df[df['statut'] == 'A verifier'])})",
        f"📺 À regarder ({len(df[df['statut'] == 'A regarder'])})",
        f"🏁 Terminé ({len(df[df['statut'] == 'Termine'])})",
        f"🗑️ Écarté ({len(df[df['statut'] == 'Ecarte'])})",
    ])

    with onglet_verifier:
        sous_df = appliquer_filtres_et_tri(df[df["statut"] == "A verifier"])
        if sous_df.empty:
            st.caption("Rien à vérifier pour le moment.")
        for _, row in sous_df.iterrows():
            afficher_carte(row)

    with onglet_regarder:
        sous_df = appliquer_filtres_et_tri(df[df["statut"] == "A regarder"])
        if sous_df.empty:
            st.caption("Rien en attente de visionnage pour le moment.")
        for _, row in sous_df.iterrows():
            afficher_carte(row)

    with onglet_termine:
        sous_df = appliquer_filtres_et_tri(df[df["statut"] == "Termine"])
        if sous_df.empty:
            st.caption("Tu n'as encore rien terminé — ça viendra !")
        for _, row in sous_df.iterrows():
            afficher_carte(row)

        if not sous_df.empty:
            st.markdown("---")
            st.subheader("📊 Répartition de ce que tu as terminé")
            col_a, col_b = st.columns(2)
            with col_a:
                st.caption("Par type d'œuvre")
                st.bar_chart(sous_df["type_oeuvre"].value_counts())
            with col_b:
                st.caption("Par genre")
                st.bar_chart(sous_df["genre"].value_counts())

    with onglet_ecarte:
        sous_df = appliquer_filtres_et_tri(df[df["statut"] == "Ecarte"])
        if sous_df.empty:
            st.caption("Rien d'écarté pour le moment.")
        for _, row in sous_df.iterrows():
            afficher_carte(row)

st.markdown("---")
st.caption(
    "💡 XP gagnés à la complétion d'une œuvre : "
    + " · ".join(f"{t} = {xp} XP" for t, xp in XP_PAR_TYPE.items())
)
