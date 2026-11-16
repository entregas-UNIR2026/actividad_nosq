// Autenticarse como root (creado por docker-compose)
db = db.getSiblingDB('admin');
db.auth("admin", "admin123");

// Cambiar a la base de datos de la app
db = db.getSiblingDB('tienda');

// ✅ DEFENSA (RBAC): Crear usuario con privilegios mínimos solo para esta DB
db.createUser({
  user: "admin",
  pwd: "admin123",
  roles: [{ role: "readWrite", db: "tienda" }]
});

// Insertar datos de prueba
db.usuarios.insertMany([
  { username: "alice", password: "password123", role: "user" },
  { username: "bob", password: "securepass", role: "admin" }
]);
db.pedidos.insertMany([
  { producto: "Laptop", cantidad: 2 },
  { producto: "Teclado", cantidad: 5 }
]);
