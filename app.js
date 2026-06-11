const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Bonjour DevOps 2026 !");
});

// Endpoint de health check (utilise par Render pour verifier que l'app est vivante).
app.get("/health", (req, res) => {
  res.status(200).json({ status: "ok" });
});

// Render fournit le port via la variable d'environnement PORT.
// On garde 3000 en repli pour le developpement local.
const PORT = process.env.PORT || 3000;

// On ne demarre le serveur que si le fichier est lance directement
// (pas pendant les tests, ou app est seulement importe).
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Serveur demarre sur le port ${PORT}`);
  });
}

module.exports = app;
