create database FinalVeterinaria
use FinalVeterinaria

create table Clientes(
	IdCliente char(5),
	Apellido varchar (20) not null,
	NroCuenta varchar (10) not null,
	Direccion varchar (40) not null,
	Telefono varchar (14) not null,
	constraint PK_Cli primary key (IdCliente)
);

create table Mascotas(
	CodMascota char(5),
	IdCliente char(5),
	Alias varchar (20) not null,
	Especie varchar (20) not null,
	Raza varchar (20) not null,
	Color_pelo varchar(15) not null,
	FechaNac date not null,
	Tamaño char (2) not null,
	constraint PK_Masc primary key (CodMascota),
	constraint FK_CliMasc foreign key (IdCliente) references Clientes
);

create table Personas(
	CI varchar (10),
	Nombre varchar (30) not null,
	constraint PK_Pers primary key (CI)
);

create table Encargados(
	IdCliente char(5),
	CI varchar (10),
	constraint PK_Enc primary key (IdCliente,CI),
	constraint FK_CliEnc foreign key (IdCliente) references Clientes,
	constraint FK_PersEnc foreign key (CI) references Personas
);

create table HistorialesPeso(
	FechaPeso date,
	CodMascota char(5),
	Peso float not null,
	constraint PK_Peso primary key (CodMascota,FechaPeso),
	constraint FK_MascPeso foreign key (CodMascota) references Mascotas
);

create table HistorialesMedicos(
	FechaConsulta date,
	CodMascota char(5),
	Enfermedad varchar (20),
	constraint PK_Med primary key (CodMascota,FechaConsulta),
	constraint FK_MascMed foreign key (CodMascota) references Mascotas
);

create table CalendariosVacunas(
	FechaVacuna date,
	CodMascota char (5),
	TipoVac varchar (20), 
	constraint PK_Vac primary key (CodMascota,FechaVacuna,TipoVac),
	constraint FK_MascVac foreign key (CodMascota) references Mascotas,
);

create table Estadias(
	CheckIn date,
	CodMascota char(5),
	CheckOut date default null,
	Dias int not null,
	constraint PK_Estad primary key (CodMascota,CheckIn),
	constraint FK_MascEstad foreign key (CodMascota) references Mascotas
);

create table Necesidades(
	CheckIn date,
	CodMascota char(5),
	TipoNec varchar (15),
	CantNec int default 0,
	constraint PK_NecEsp primary key (CodMascota,CheckIn,TipoNec),
	constraint FK_FechaNec foreign key (CodMascota,CheckIn) references Estadias
);

create table Extras(
	CheckIn date,
	CodMascota char(5),
	TipoExtra varchar (15),
	CantExtra int default 1,
	Cargo money not null,
	constraint PK_Extra primary key (CodMascota,CheckIn,TipoExtra),
	constraint FK_FechaExtra foreign key (CodMascota,CheckIn) references Estadias
);