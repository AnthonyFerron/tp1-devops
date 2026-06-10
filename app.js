const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Bonjour DevOps !");
});

// Render fournit le port via la variable d'environnement PORT.
// On garde 3000 en repli pour le développement local.
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Serveur démarré sur le port ${PORT}`);
});
