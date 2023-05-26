--Procedimiento de registro de peso
create procedure RegistrarPeso
@FechaPeso date,
@CodMascota char(5),
@Peso float
as 
BEGIN
    insert into HistorialesPeso values (@FechaPeso,@CodMascota,@Peso)
END
GO;

--procedimiento de registro de visita medica
create PROCEDURE RegistrarVisitaMedica 
@FechaConsulta date,
@CodMascota char(5),
@Situacion varchar(20),
@DetalleMed varchar(40)
as 
BEGIN
    insert into HistorialesMedicos values (@FechaConsulta,@CodMascota,@Situacion,@DetalleMed)
END
GO;

--Procedimiento para registrar una vacunacion
create PROCEDURE RegistrarVacuna
@FechaVacuna date,
@CodMascota char (5),
@TipoVac varchar(20)
as 
BEGIN
    insert into CalendariosVacunas values (@FechaVacuna,@CodMascota,@TipoVac)
END
GO;

create procedure RegistrarEstadia
@CheckIn date,
@CodMascota char (5),
@NroHab char (2),
@Dias int
AS
BEGIN
    insert into Estadias values (@CheckIn,@CodMascota,@NroHab,NULL,@Dias)
END
GO;

create view TamañoMascotas as
select CodMascota, Tamaño from Mascotas
GO;

select * from TamañoMascotas
declare CursorTamaños cursor for select * from TamañoMascotas 
GO;

create view ServiciosEsp as 
select IdServicio, Precio from Servicios
where IdServicio = 'S04' or IdServicio = 'S05'
GO; 

select * from ServiciosEsp
declare CursorServiciosEsp cursor for select * from ServiciosEsp 
GO;

--Procedimiento para registrar un requerimiento de un servicio en la estadía
create procedure RegistrarRequerimiento 
@CodMascota char (5), 
@IdServicio char(3),
@CheckIn date, 
@Cantidad int,
@NroHab char (2),
@Dias int
AS
BEGIN 
    DECLARE
    @Tamaño char (2),
    @Cargo money,
	@Factor float,
    @Precio money
    --son servicios especiales y no tienen cantidad, se cobra por la cantidad de dias
    if @IdServicio = 'S04' or @IdServicio = 'S05'
        BEGIN
        set @Cargo = (select Precio from Servicios where IdServicio = @IdServicio)
        set @Cargo *= @Dias
        insert into Requerimientos values (@IdServicio,@CheckIn,@CodMascota,@NroHab,NULL,@Cargo)
        END
    --servicios que pueden llegar a realizarse hasta una vez por estadía
    if @IdServicio = 'S02'
        BEGIN
        set @Cargo = (select Precio from Servicios where IdServicio = @IdServicio)
        insert into Requerimientos values (@IdServicio,@CheckIn,@CodMascota,@NroHab,1,@Cargo)
        END
    else
    --los demás servicios que se pueden realizar varias veces y se cobran de acuerdo al tamaño, cantidad de veces
        BEGIN
        set @Tamaño = (select Tamaño from Mascotas where CodMascota = @CodMascota)
        set @Precio = (select Precio from Servicios where IdServicio = @IdServicio)
        if @Tamaño = 'S'
            set @Factor = 1
        if @Tamaño = 'M'
            set @Factor = 1.15
        if @Tamaño = 'G'
            set @Factor = 1.30
        if @Tamaño = 'XG'
            set @Factor = 1.40
        set @Cargo = @Cantidad * @Precio * @Factor
        insert into Requerimientos values (@IdServicio,@CheckIn,@CodMascota,@NroHab,@Cantidad,@Cargo)
        END
END  

select * from Servicios
insert into Mascotas values ('M0077','C0001','Test','Felino','Bombay','Negro','2020/01/15','G')
insert into Estadias values ('2023-05-06','M0077','01',NULL,7)
select * from Estadias
exec RegistrarRequerimiento 'M0077','S03','2023-05-06',4,'01',7
select * from Requerimientos








    
    
    
        



















