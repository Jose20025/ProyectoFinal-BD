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

--Modificar un registro de peso
create procedure ModificarPeso
@FechaPeso date,
@CodMascota char (5),
@NuevoPeso float
AS
BEGIN
    update HistorialesPeso set Peso = @NuevoPeso 
    where CodMascota = @CodMascota and FechaPeso = @FechaPeso  
END
GO;

--Eliminar un registro de peso
create procedure EliminarRegPeso
@FechaPeso date,
@CodMascota char (5)
AS
BEGIN
    delete from HistorialesPeso 
    where CodMascota = @CodMascota and FechaPeso = @FechaPeso 
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

--Modificar una visita medica
create procedure ModificarVisitaMed
@FechaConsulta date,
@CodMascota char(5),
@Campo varchar (20),
@NuevoValor varchar (40)
AS
BEGIN
    update HistorialesMedicos set @Campo = @NuevoValor
    where FechaConsulta = @FechaConsulta and CodMascota = @CodMascota
END
GO;

--Eliminar una visita medica
create procedure EliminarVisitaMed
@FechaConsulta date,
@CodMascota char(5)
AS
BEGIN
    delete from HistorialesMedicos where FechaConsulta = @FechaConsulta and CodMascota = @CodMascota
END
GO; 

--Procedimiento para registrar una vacunacion
create PROCEDURE RegistrarVacunacion
@FechaVacuna date,
@CodMascota char (5),
@TipoVacuna varchar(15),
@Fabricante varchar (20)
as 
BEGIN
    insert into CalendariosVacunas values (@FechaVacuna,@CodMascota,@TipoVacuna,@Fabricante)
END
GO;

--no existe la modificación de un campo de vacunación, puesto que todos los campos forman la PK
--de modo que si se registra una vacunacion errada, se procede con la eliminación del registro

--Eliminar una vacunacion
create procedure EliminarVacunacion
@FechaVacuna date,
@CodMascota char (5),
@TipoVacuna varchar(15),
@Fabricante varchar (20)
AS
BEGIN
    delete from CalendariosVacunas
    where FechaVacuna=@FechaVacuna and CodMascota=@CodMascota and TipoVacuna=@TipoVacuna and Fabricante=@Fabricante
END
GO;

--Registro de una estadía
create procedure RegistrarEstadia
@CheckIn date,
@CodMascota char (5),
@NroHab char (2),
@Dias int
AS
BEGIN
    insert into Estadias values (@CheckIn,@CodMascota,@NroHab,NULL,@Dias)
    update Habitaciones set Disponible = 'O' where NroHab = @NroHab
END
GO;

--Modificación de una estadía
create procedure ModificarEstadia
@CheckIn date,
@CodMascota char (5),
@NroHab char (2),
@Campo varchar (20),
@NuevoValor varchar (20)
as
BEGIN
    if @Campo = 'NroHab'
        BEGIN
        update Habitaciones set Disponible = 'D' where NroHab = @NroHab
        update Estadias set NroHab = @NuevoValor 
        where CheckIn = @CheckIn and CodMascota=@CodMascota and NroHab=@NroHab 
        update Habitaciones set Disponible = 'O' where NroHab=@NuevoValor
        END 
    else 
        update Estadias set @Campo = @NuevoValor
        where CheckIn = @CheckIn and CodMascota=@CodMascota and NroHab=@NroHab
END
GO;

--Eliminar una estadía
create procedure EliminarEstadia
@CheckIn date,
@CodMascota char (5),
@NroHab char (2)
AS
BEGIN
    delete from Estadias
    where CheckIn = @CheckIn and CodMascota=@CodMascota and NroHab=@NroHab
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
GO;

--Modificacion de requerimiento
create procedure ModificarRequerimiento
@IdServicio char (3),
@CheckIn date,
@CodMascota char (5),
@NroHab char (2),
@Campo varchar (10),
@NuevoValor int
AS
BEGIN
    if @IdServicio='S01' or @IdServicio='S03' or @IdServicio ='S06'
        if @Campo = 'Cantidad'
            BEGIN
                DECLARE
                @Tamaño char (2),
                @Cargo money,
                @Factor float,
                @Precio money
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
                set @Cargo = @NuevoValor * @Precio * @Factor
                update Requerimientos set Cantidad=@NuevoValor, Cargo=@Cargo
                where IdServicio=@IdServicio and CheckIn=@CheckIn and CodMascota=@CodMascota and NroHab=@NroHab
            END
END
GO;

--Eliminación de requerimiento en la estadía
create procedure EliminarRequerimiento
@IdServicio char (3),
@CheckIn date,
@CodMascota char (5),
@NroHab char (2)
AS
BEGIN
    delete from Requerimientos
    where IdServicio=@IdServicio and CheckIn=@CheckIn and CodMascota=@CodMascota and NroHab=@NroHab
END
GO;

--Adicion de vacunas de nuevos proveedores
create procedure AgregarVacuna
@TipoVacuna varchar(15),
@Fabricante varchar(20),
@Precio money
AS
BEGIN
    insert into Vacunas values (@TipoVacuna,@Fabricante,@Precio)
END
GO;

--Eliminar vacuna
create procedure EliminarVacuna
@TipoVacuna varchar(15),
@Fabricante varchar (20)
AS
BEGIN
    delete from Vacunas where TipoVacuna=@TipoVacuna and Fabricante=@Fabricante
END

select * from Servicios

select * from Servicios 
insert into Mascotas values ('M0077','C0001','Test','Felino','Bombay','Negro','2020/01/15','G')
insert into Estadias values ('2023-05-06','M0077','01',NULL,7)
select * from Estadias
exec RegistrarRequerimiento 'M0077','S03','2023-05-06',4,'01',7
select * from Requerimientos








    
    
    
        



















