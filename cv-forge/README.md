# CV-Forge

**Générateur de CV optimisé ATS** - Application desktop Python pour créer des CV 100% compatibles avec les systèmes de suivi des candidats (ATS).

## 🎯 Objectif

Créer une application desktop qui :
- Génère un CV 100% compatible ATS
- Structure proprement les sections
- Exporte en PDF et DOCX
- Évite les éléments problématiques (colonnes, icônes, images inutiles)
- Force une structure standardisée

## 🏗 Architecture

```
cv-forge/
│
├── main.py                 # Point d'entrée de l'application
├── requirements.txt        # Dépendances Python
├── ui/
│   ├── main_window.py      # Fenêtre principale avec onglets
│   └── forms.py            # Composants de formulaire
├── models/
│   └── resume.py           # Modèle de données Resume
├── exporters/
│   ├── docx_exporter.py    # Export Word (python-docx)
│   └── pdf_exporter.py     # Export PDF (reportlab)
├── data/
│   └── profiles.json       # Stockage des profils sauvegardés
└── assets/                 # Ressources (futur)
```

## 🚀 Installation

### Prérequis
- Python 3.11 ou supérieur

### Étapes

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Lancer l'application :
```bash
python main.py
```

## 📋 Structure ATS du CV

### 1. En-tête
Format texte simple :
```
PHILIBERT RAKOTO
+261 34 00 000 00 | phil@example.com
linkedin.com/in/philibert
```

### 2. Profil / Accroche
Court, direct, avec le titre exact du poste visé.

### 3. Formation
Format strict : `Diplôme – Établissement – Dates`

### 4. Certification
Format : `Nom – Organisme – Année`

### 5. Expériences Professionnelles
Format obligatoire :
```
Poste – Entreprise – Ville – MM/YYYY – MM/YYYY
• Description de la mission
• Réalisation concrète
```

### 6. Compétences
- **Compétences Techniques** : Angular, TypeScript, PHP, MySQL...
- **Compétences Comportementales** : Leadership, Travail en équipe...

## 💻 Fonctionnalités

- ✅ Interface utilisateur moderne avec CustomTkinter
- ✅ 5 onglets : Informations personnelles, Formation, Certifications, Expériences, Compétences
- ✅ Export PDF avec mise en page ATS-friendly
- ✅ Export DOCX compatible Word
- ✅ Sauvegarde et chargement de profils (JSON)
- ✅ Multi-profils supportés

## 🛠 Stack Technique

- **Python 3.11+**
- **CustomTkinter** - Interface utilisateur moderne
- **python-docx** - Génération de documents Word
- **reportlab** - Génération de PDF

## 📝 Utilisation

1. **Remplir les informations personnelles** : Nom, prénom, contact, LinkedIn, profil
2. **Ajouter les formations** : Diplômes, établissements, dates
3. **Ajouter les certifications** : Noms, organismes, années
4. **Ajouter les expériences** : Postes, entreprises, villes, dates, descriptions
5. **Saisir les compétences** : Techniques et comportementales
6. **Exporter** : PDF ou DOCX
7. **Sauvegarder** : Profil pour réutilisation future

## 🔮 Fonctionnalités Futures (v2)

- [ ] Analyse des mots-clés ATS
- [ ] Score de compatibilité avec une offre d'emploi
- [ ] Détection automatique des verbes d'action
- [ ] Export multi-modèles
- [ ] Version multilingue

## 📄 Licence

Projet open-source à but éducatif.

---

**CV-Forge** - Créé pour des CV machine-readables, scannables, efficaces.
