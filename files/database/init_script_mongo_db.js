use sensorial-db;

/*=====================================*/
/* ELIMINACION DE DOCUMENTOS */
/*=====================================*/
db.dashboards.drop();
db.samples.drop();
db.sensors.drop();
db.sessions.drop();
db.usuarios.drop();

/*=====================================*/
/* CREACION DE DOCUMENTOS */
/*=====================================*/
db.createCollection("dashboards");
db.createCollection("samples");
db.createCollection("sensors");
db.createCollection("sessions");
db.createCollection("usuarios");

/*=====================================*/
/* CARGA DE DATOS */
/*=====================================*/


/*USUARIOS*/
/*pass = asd*/
db.usuarios.insertMany([
  {
    ultimo_login: new Date(),
    fecha_creacion: new Date(),
    mail: "Enzope32@gmail.com",
    nombre: "Enzo Perez",
    rol: "admin",
    password: "asd",
  },
  {
    ultimo_login: new Date(),
    fecha_creacion: new Date(),
    mail: "user@gmail.com",
    nombre: "usuario",
    rol: "user",
    password: "asd",
  }
]);

/*SENSORES*/
db.sensors.insertMany([
  {
    nombre: "Almacen 3",
    tipo: "3"
  },
  {
    nombre: "Almacen 2",
    tipo: "3"
  },
  {
    nombre: "Almacen 1",
    tipo: "3"
  },
  {
    nombre: "Deposito 3",
    tipo: "1"
  },
  {
    nombre: "Deposito 2",
    tipo: "1"
  },
  {
    nombre: "Taller 2",
    tipo: "0"
  },
  {
    nombre: "Taller 1",
    tipo: "0"
  }
]);

/*TABLEROS*/
db.dashboards.insertMany([
  {
    _id: ObjectId("6117156fc8dc5f250aa610ed"),
    fecha_creacion: new Date(),
    nombre: "Tablero 1",
    descripcion: "es de prueba",
    reportes: [{
      destinatarios: ["Enzope32@gmail.com", "user@gmail.com"],
      _id: ObjectId("611726a9f1955d326178ab78"),
      nombre: "asd",
      descripcion: "asd",
      dia: "Martes",
      horario: "03:23"
    }],
    objetivos: [],
    indicadores: [{
      sensors: [db.sensors.findOne({ "nombre": "Deposito 3" })._id.valueOf(), db.sensors.findOne({ "nombre": "Deposito 2" })._id.valueOf()],
      _id: ObjectId("611840086fa7e70c878ef734"),
      name: "prod multiple",
      type: "produccion",
      limitInferior: "2323"
    }]
  },
  {
    _id: ObjectId("6118401a6fa7e70c878ef73a"),
    fecha_creacion: new Date(),
    nombre: "Tablero 2",
    descripcion: "asd",
    reportes: [],
    objetivos: [],
    indicadores: [{
      sensors: [db.sensors.findOne({ "nombre": "Almacen 1" })._id.valueOf()],
      _id: ObjectId("611840626fa7e70c878ef754"),
      name: "calidad del aire",
      type: "calidad_del_aire",
      limitInferior: "33"
    }]
  }
]);

/*MUESTRAS*/
db.samples.insertMany([
  {
    valor: "12",
    id_sensor: db.sensors.findOne({ "nombre": "Almacen 1" })._id.valueOf(),
    tipo_sensor: "calidad_del_aire",
    unidad: "grados_centigrados",
    fecha: new Date()
  },
  {
    valor: "35",
    id_sensor: db.sensors.findOne({ "nombre": "Almacen 1" })._id.valueOf(),
    tipo_sensor: "calidad_del_aire",
    unidad: "grados_centigrados",
    fecha: new Date()
  },
  {
    valor: "37",
    id_sensor: db.sensors.findOne({ "nombre": "Almacen 1" })._id.valueOf(),
    tipo_sensor: "calidad_del_aire",
    unidad: "grados_centigrados",
    fecha: new Date()
  },
  {
    valor: "16",
    id_sensor: db.sensors.findOne({ "nombre": "Almacen 1" })._id.valueOf(),
    tipo_sensor: "calidad_del_aire",
    unidad: "grados_centigrados",
    fecha: new Date()
  }

])
