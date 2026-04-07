# Tests, Couverture & Qualite

[![CI](https://github.com/alexandreNoens/ynov-cicd-tp02/actions/workflows/ci.yml/badge.svg)](https://github.com/alexandreNoens/ynov-cicd-tp02/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](#prérequis)
[![FastAPI](https://img.shields.io/badge/FastAPI-modern-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Ruff](https://img.shields.io/badge/lint-ruff-46a2f1?logo=ruff)](https://docs.astral.sh/ruff)
[![Pytest](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest)](https://docs.pytest.org/)

Serie d'exercices progressifs + TP complet. Vous allez ecrire des tests unitaires, d'integration, configurer la couverture, le linting, et pratiquer le TDD.

## Prérequis

- Python 3.11+
- uv

## Démarrage

### 1) Installer le projet

```bash
make install
```

Crée l'environnement virtuel si besoin, génère le lock des dépendances avec hashes et installe les dépendances.

### 2) Initialiser la base de données (reset)

```bash
make install-db
```

Supprime et recrée la base SQLite, puis charge le schéma et les données de dev.

### 3) Lancer l'application

```bash
make serve
```

Lance l'API FastAPI en local avec rechargement automatique.

## Qualité

### Lancer les tests

```bash
make check
```

Exécute les tests avec pytest et affiche la couverture de code.

### Lancer le linter

```bash
make lint
```

Exécute le lint avec ruff.

### Corriger automatiquement les erreurs

```bash
make fix
```

Corrige automatiquement les erreurs de style avec ruff.
