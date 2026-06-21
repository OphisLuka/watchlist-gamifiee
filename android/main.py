"""
Watchlist mobile (Kivy / Android) -- version simplifiee
------------------------------------------------------------------
Version mobile allegee de la Watchlist Streamlit : permet d'ajouter
une oeuvre (titre + type), de la voir dans une liste, de la marquer
comme "Terminee" ou de la supprimer. Les donnees sont sauvegardees
localement en JSON sur l'appareil, donc elles persistent entre les
sessions.

Cette version est volontairement simple : c'est la base qui doit
fonctionner de bout en bout (ajout -> sauvegarde -> rechargement)
avant d'ajouter des fonctionnalites plus avancees (XP, rangs, filtres)
comme dans la version Streamlit.
"""

import json
import os
import uuid

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.metrics import dp

FICHIER_DONNEES = "watchlist_mobile.json"
TYPES_OEUVRE = ["Film", "Serie", "Manga", "Anime", "Autre"]


# ----------------------------------------------------------------------
# FONCTIONS UTILITAIRES : charger / sauvegarder les donnees (JSON)
# ----------------------------------------------------------------------
def charger_donnees():
    """Lit le fichier JSON local et renvoie la liste des oeuvres (liste de dicts)."""
    if os.path.exists(FICHIER_DONNEES):
        with open(FICHIER_DONNEES, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def sauvegarder_donnees(liste_oeuvres):
    """Ecrit la liste des oeuvres dans le fichier JSON local."""
    with open(FICHIER_DONNEES, "w", encoding="utf-8") as f:
        json.dump(liste_oeuvres, f, ensure_ascii=False, indent=2)


def ajouter_oeuvre(titre, type_oeuvre):
    """Ajoute une nouvelle oeuvre avec le statut 'A regarder' par defaut."""
    liste_oeuvres = charger_donnees()
    liste_oeuvres.append({
        "id": str(uuid.uuid4())[:8],
        "titre": titre,
        "type_oeuvre": type_oeuvre,
        "statut": "A regarder",
    })
    sauvegarder_donnees(liste_oeuvres)
    return liste_oeuvres


def changer_statut(id_oeuvre, nouveau_statut):
    """Modifie le statut d'une oeuvre existante, identifiee par son id."""
    liste_oeuvres = charger_donnees()
    for oeuvre in liste_oeuvres:
        if oeuvre["id"] == id_oeuvre:
            oeuvre["statut"] = nouveau_statut
    sauvegarder_donnees(liste_oeuvres)
    return liste_oeuvres


def supprimer_oeuvre(id_oeuvre):
    """Retire une oeuvre de la liste, identifiee par son id."""
    liste_oeuvres = charger_donnees()
    liste_oeuvres = [o for o in liste_oeuvres if o["id"] != id_oeuvre]
    sauvegarder_donnees(liste_oeuvres)
    return liste_oeuvres


# ----------------------------------------------------------------------
# INTERFACE GRAPHIQUE (Kivy)
# ----------------------------------------------------------------------
class WatchlistApp(App):
    def build(self):
        self.title = "Watchlist"
        self.layout_principal = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))

        # --- Zone d'ajout (titre + type + bouton) ---
        zone_ajout = BoxLayout(orientation="vertical", size_hint=(1, None), height=dp(140), spacing=dp(6))

        self.champ_titre = TextInput(
            hint_text="Titre de l'oeuvre",
            multiline=False,
            size_hint=(1, None),
            height=dp(40),
        )
        self.champ_type = Spinner(
            text=TYPES_OEUVRE[0],
            values=TYPES_OEUVRE,
            size_hint=(1, None),
            height=dp(40),
        )
        bouton_ajouter = Button(text="Ajouter a la liste", size_hint=(1, None), height=dp(45))
        bouton_ajouter.bind(on_press=self.on_ajouter)

        zone_ajout.add_widget(self.champ_titre)
        zone_ajout.add_widget(self.champ_type)
        zone_ajout.add_widget(bouton_ajouter)

        self.layout_principal.add_widget(zone_ajout)

        # --- Liste scrollable des oeuvres ---
        self.zone_liste = GridLayout(cols=1, spacing=dp(6), size_hint_y=None)
        self.zone_liste.bind(minimum_height=self.zone_liste.setter("height"))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.zone_liste)
        self.layout_principal.add_widget(scroll)

        self.rafraichir_liste()
        return self.layout_principal

    def on_ajouter(self, instance):
        titre = self.champ_titre.text.strip()
        if not titre:
            self.afficher_popup("Le titre ne peut pas etre vide.")
            return
        ajouter_oeuvre(titre, self.champ_type.text)
        self.champ_titre.text = ""
        self.rafraichir_liste()

    def on_terminer(self, id_oeuvre):
        changer_statut(id_oeuvre, "Terminee")
        self.rafraichir_liste()

    def on_supprimer(self, id_oeuvre):
        supprimer_oeuvre(id_oeuvre)
        self.rafraichir_liste()

    def afficher_popup(self, message):
        popup = Popup(
            title="Info",
            content=Label(text=message),
            size_hint=(0.8, 0.3),
        )
        popup.open()

    def rafraichir_liste(self):
        """Reconstruit entierement la liste affichee a partir des donnees sauvegardees."""
        self.zone_liste.clear_widgets()
        liste_oeuvres = charger_donnees()

        if not liste_oeuvres:
            self.zone_liste.add_widget(
                Label(text="Ta watchlist est vide pour le moment.", size_hint_y=None, height=dp(40))
            )
            return

        # Affiche d'abord les "A regarder", puis les "Terminee"
        for statut in ["A regarder", "Terminee"]:
            oeuvres_du_statut = [o for o in liste_oeuvres if o["statut"] == statut]
            if not oeuvres_du_statut:
                continue

            entete = "📺 A regarder" if statut == "A regarder" else "🏁 Terminee"
            self.zone_liste.add_widget(
                Label(text=entete, bold=True, size_hint_y=None, height=dp(30), halign="left")
            )

            for oeuvre in oeuvres_du_statut:
                ligne = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50), spacing=dp(6))

                texte = f"{oeuvre['titre']} ({oeuvre['type_oeuvre']})"
                ligne.add_widget(Label(text=texte, size_hint=(0.5, 1), halign="left", valign="middle"))

                if statut == "A regarder":
                    bouton_fini = Button(text="Termine", size_hint=(0.25, 1))
                    bouton_fini.bind(on_press=lambda inst, id_o=oeuvre["id"]: self.on_terminer(id_o))
                    ligne.add_widget(bouton_fini)

                bouton_suppr = Button(text="Suppr.", size_hint=(0.25, 1))
                bouton_suppr.bind(on_press=lambda inst, id_o=oeuvre["id"]: self.on_supprimer(id_o))
                ligne.add_widget(bouton_suppr)

                self.zone_liste.add_widget(ligne)


if __name__ == "__main__":
    WatchlistApp().run()
