const express = require("express");
const jwt = require("jsonwebtoken");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;
const SECRET_KEY = process.env.JWT_SECRET || "mysecretkey";

app.use(cors({
  origin: [/^http:\/\/localhost:\d+$/, /^http:\/\/127\.0\.0\.1:\d+$/],
  methods: ["GET", "POST", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization", "Token"]
}));
app.use(express.json());

app.get("/", (req, res) => {
  res.json({
    message: "Node JWT Service Running"
  });
});

app.post("/generate-token", (req, res) => {
  const payload = req.body && Object.keys(req.body).length > 0
    ? req.body
    : {
        userId: 1,
        username: "charan",
        role: "admin"
      };

  const token = jwt.sign(payload, SECRET_KEY, {
    expiresIn: "1h"
  });

  res.json({
    message: "Token generated successfully",
    token
  });
});

app.post("/verify-token", (req, res) => {
  const token = getTokenFromRequest(req);

  if (!token) {
    return res.status(400).json({
      message: "Token is required"
    });
  }

  try {
    const decoded = jwt.verify(token, SECRET_KEY);

    return res.json({
      message: "Token is valid",
      data: decoded
    });
  } catch (error) {
    return res.status(401).json({
      message: "Invalid or expired token"
    });
  }
});

app.get("/dashboard", (req, res) => {
  const token = getTokenFromRequest(req);

  if (!token) {
    return res.status(401).json({
      message: "Token required"
    });
  }

  try {
    const decoded = jwt.verify(token, SECRET_KEY);

    return res.json({
      message: "Welcome to Dashboard",
      user: decoded
    });
  } catch (error) {
    return res.status(401).json({
      message: "Invalid or expired token"
    });
  }
});

app.use((req, res) => {
  res.status(404).json({
    message: "Route not found"
  });
});

function getTokenFromRequest(req) {
  const authHeader = req.headers.authorization || "";
  if (authHeader.startsWith("Bearer ")) {
    return authHeader.slice(7);
  }

  return req.headers.token || req.body?.token || "";
}

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
