# TP 1 DevOps — Application Express déployée sur Render

[![CI](https://github.com/AnthonyFerron/tp1-devops/actions/workflows/main.yml/badge.svg)](https://github.com/AnthonyFerron/tp1-devops/actions/workflows/main.yml)

Petite application web **Node.js / Express** illustrant une chaîne **CI/CD** complète :

```
Code → GitHub → GitHub Actions (CI + tests) → Build → Render → Production
```

🌐 **Application en ligne :** https://tp1-devops-6vgr.onrender.com

## 🚀 Fonctionnalités

| Route      | Description                                  |
| ---------- | -------------------------------------------- |
| `GET /`        | Renvoie le message « Bonjour DevOps 2026 ! » |
| `GET /health`  | Health check — renvoie `{ "status": "ok" }`  |

## 🧱 Stack

- **Node.js 20** + **Express**
- **Jest** + **Supertest** pour les tests
- **GitHub Actions** pour l'intégration continue
- **Render** pour le déploiement continu (auto-deploy sur `push`)

## 💻 Lancer en local

```bash
npm install      # installer les dépendances
npm start        # démarrer le serveur (http://localhost:3000)
npm test         # exécuter les tests
```

## ⚙️ Intégration continue (GitHub Actions)

À chaque `push` ou *pull request*, le workflow [`.github/workflows/main.yml`](.github/workflows/main.yml) :

1. récupère le code (`actions/checkout`) ;
2. installe Node 20 avec cache npm (`actions/setup-node`) ;
3. installe les dépendances de façon reproductible (`npm ci`) ;
4. exécute les tests (`npm test`).

Un test en échec fait échouer la CI et signale le problème avant la mise en production.

## ☁️ Déploiement (Render — Infrastructure as Code)

Le service est décrit dans [`render.yaml`](render.yaml) (build `npm ci`, start `node app.js`,
health check `/health`, `autoDeploy: true`). Render redéploie automatiquement à chaque
commit poussé sur `main`.
