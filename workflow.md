# 🔄 Workflow Complet de Vérification — Niyya Verify

## 📋 Vue d'Ensemble

```
PHOTO REÇUE (1 image)
    │
    ├─→ Étape 0 : Vérification Metadata (Rule-based)
    │
    ├─→ Étape 1 : IA #1 — Anti-Spoofing / Liveness
    │
    ├─→ Étape 2 : IA #2 — Gender Classification
    │
    └─→ DÉCISION FINALE
```

---

## 📊 Détail des Étapes

### Étape 0 — Vérification Metadata *(Rule-based, PAS IA)*

| | |
| :--- | :--- |
| **Objectif** | Vérifier que la photo provient bien d'une caméra |
| **Technologie** | Lecture des données EXIF |
| **Vérifications** | • Marque et modèle de la caméra<br>• Date et heure de capture<br>• Logiciel utilisé (détection screenshot) |
| **❌ Si suspect** | → **REJET IMMÉDIAT** |
| **✅ Si valide** | → Continuer vers **IA #1** |

---

### Étape 1 — IA #1 : Anti-Spoofing / Liveness

| | |
| :--- | :--- |
| **Objectif** | Détecter une vraie personne vs une fausse image |
| **Technologie** | CNN Anti-Spoofing (TensorFlow/PyTorch) |
| **Vérifications** | • Texture de peau vs écran/papier<br>• Motifs Moiré (photo d'écran)<br>• Estimation de profondeur 3D |
| **❌ Si `is_live = false`** | → **REJET** (spoofing détecté) |
| **✅ Si `is_live = true`** | → Continuer vers **IA #2** |

---

### Étape 2 — IA #2 : Gender Classification

| | |
| :--- | :--- |
| **Objectif** | Classifier le genre de la personne |
| **Technologie** | CNN Classification (TensorFlow/PyTorch) |
| **Vérifications** | • Traits faciaux féminins/masculins<br>• Structure du visage<br>• Score de confiance |
| **❌ Si `gender = male`** | → **REJET** (non éligible) |
| **❌ Si `confidence < seuil`** | → **REVUE MANUELLE** |
| **✅ Si `gender = female` + confiance OK** | → **APPROUVÉ** |

---

## 🎯 Décision Finale

| Statut | Condition | Action |
| :--- | :--- | :--- |
| ✅ **APPROUVÉ** | Liveness OK + Femme + Confiance élevée | Accès autorisé à la plateforme |
| ❌ **REJETÉ** | Spoofing détecté OU Homme | Accès refusé |
| ⏳ **REVUE MANUELLE** | Confiance IA trop faible | Validation par modératrice humaine |

---

## ⚡ Performance

| Métrique | Valeur |
| :--- | :--- |
| **Temps total** | 2 à 5 secondes |
| **Étape 0 (Metadata)** | < 100 ms |
| **Étape 1 (Liveness)** | 1 à 3 secondes |
| **Étape 2 (Gender)** | 1 à 2 secondes |
| **Images stockées** | Aucune (Zero Storage) |

---

## 🧠 Résumé des Technologies

| Étape | Type | Technologie |
| :--- | :--- | :--- |
| **0** | Rule-based | EXIF Parsing (PIL) |
| **1** | Intelligence Artificielle | CNN Anti-Spoofing |
| **2** | Intelligence Artificielle | CNN Gender Classification |

---

## 📁 Architecture des Services

```
niyya-verify/
├── app/
│   ├── main.py              # Orchestration des 3 étapes
│   ├── services/
│   │   ├── metadata.py      # Étape 0
│   │   ├── liveness.py      # Étape 1 (IA #1)
│   │   └── gender.py        # Étape 2 (IA #2)
├── models/
│   ├── liveness/            # Modèle Anti-Spoofing
│   └── gender/              # Modèle Gender Classification
└── tests/
    ├── test_liveness.py
    └── test_gender.py
```