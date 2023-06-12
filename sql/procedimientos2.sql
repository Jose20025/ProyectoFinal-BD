--Procedimiento de registro de peso
alter procedure RegistrarPeso
    @FechaPeso date,
    @CodMascota char(5),
    @Peso varchar(5),
    @Check bit out
as BEGIN
    begin TRANSACTION
    if exists (
    select 1
    from HistorialesPeso
    where FechaPeso = @FechaPeso
        and CodMascota = @CodMascota
) BEGIN
        set @Check = 0
        SELECT @Check
    end
else BEGIN
        set @Check = 1
        select @Check
        insert into HistorialesPeso
        values
            (@FechaPeso, @CodMascota, CAST(@Peso AS float))
    END
END
GO
--Modificar un registro de peso
alter procedure ModificarPeso
    @FechaPeso date,
    @CodMascota char (5),
    @NuevoPeso float,
    @Check bit out
AS BEGIN
    begin TRANSACTION
    DECLARE @SQL NVARCHAR(MAX);
    update HistorialesPeso
set Peso = @NuevoPeso
where CodMascota = @CodMascota
        and FechaPeso = @FechaPeso
    if exists (
        select 1
    from HistorialesPeso
    where FechaPeso = @FechaPeso
        and CodMascota = @CodMascota
        and Peso = @NuevoPeso
    ) BEGIN
        set @Check = 1
        SELECT @Check
    END
else BEGIN
        set @Check = 0
        SELECT @Check
    END
END
GO;
--Eliminar un registro de peso
alter procedure EliminarRegPeso
    @FechaPeso date,
    @CodMascota char (5),
    @Cuenta int,
    @Check bit out
AS BEGIN
    begin TRANSACTION
    delete from HistorialesPeso
where CodMascota = @CodMascota
        and FechaPeso = @FechaPeso
    select @Cuenta = count(*)
    from HistorialesPeso
    where FechaPeso = @FechaPeso
        and CodMascota = @CodMascota
    if @Cuenta = 0 BEGIN
        set @Check = 1
        SELECT @Check
    END
else BEGIN
        set @Check = 0
        SELECT @Check
    END
END
GO;
--procedimiento de registro de visita medica 
alter PROCEDURE RegistrarVisitaMedica
    @FechaConsulta date,
    @CodMascota char(5),
    @Situacion varchar(20),
    @DetalleMed varchar(40),
    @Check bit out
as BEGIN
    if exists (
    select 1
    from HistorialesMedicos
    where FechaConsulta = @FechaConsulta
        and CodMascota = @CodMascota
) BEGIN
        set @Check = 0
        SELECT @Check
    end
else BEGIN
        set @Check = 1
        select @Check
        insert into HistorialesMedicos
        values
            (
                @FechaConsulta,
                @CodMascota,
                @Situacion,
                @DetalleMed
    )
        commit
    END
END
GO;
--Modificar una visita medica
alter PROCEDURE ModificarVisitaMed
    @FechaConsulta DATE,
    @CodMascota CHAR(5),
    @Campo VARCHAR(20),
    @NuevoValor VARCHAR(40),
    @Check BIT OUT
AS BEGIN
    BEGIN TRANSACTION;
    DECLARE @SQL NVARCHAR(MAX);
    SET @SQL = N'UPDATE HistorialesMedicos SET ' + QUOTENAME(@Campo) + ' = @NuevoValor WHERE FechaConsulta = @FechaConsulta AND CodMascota = @CodMascota';
    EXEC sp_executesql @SQL,
N'@FechaConsulta DATE, @CodMascota CHAR(5), @NuevoValor VARCHAR(40)',
@FechaConsulta,
@CodMascota,
@NuevoValor;
    IF EXISTS (
    SELECT 1
    FROM HistorialesMedicos
    WHERE FechaConsulta = @FechaConsulta
        AND CodMascota = @CodMascota
        AND ' + QUOTENAME(@Campo) + ' = @NuevoValor
) BEGIN
        SET @Check = 1;
        SELECT @Check;
    END
ELSE BEGIN
        SET @Check = 0;
        SELECT @Check;
    END
END
GO;
--Eliminar una visita medica
alter procedure EliminarVisitaMed
    @FechaConsulta date,
    @CodMascota char(5),
    @Cuenta int,
    @Check bit out
AS BEGIN
    begin TRANSACTION
    delete from HistorialesMedicos
where FechaConsulta = @FechaConsulta
        and CodMascota = @CodMascota
    select @Cuenta = count (*)
    from HistorialesMedicos
    where FechaConsulta = @FechaConsulta
        and CodMascota = @CodMascota
    if @Cuenta = 0 BEGIN
        set @Check = 1
        SELECT @Check
    end
else BEGIN
        set @Check = 0
        SELECT @Check
    end
END
GO;
--Procedimiento para registrar una vacunacion
alter PROCEDURE RegistrarVacunacion
    @FechaVacuna date,
    @CodMascota char (5),
    @TipoVacuna varchar(15),
    @Fabricante varchar (20),
    @Check bit out
as BEGIN
    begin TRANSACTION
    if exists (
    select 1
    from CalendariosVacunas
    where FechaVacuna = @FechaVacuna
        and CodMascota = @CodMascota
        and TipoVacuna = @TipoVacuna
) BEGIN
        set @Check = 0
        SELECT @Check
    end
ELSE BEGIN
        set @Check = 1
        select @Check
        insert into CalendariosVacunas
        values
            (
                @FechaVacuna,
                @CodMascota,
                @TipoVacuna,
                @Fabricante
    )
    END
END
GO;
--no existe la modificación de un campo de vacunación, puesto que todos los campos forman la PK
--de modo que si se registra una vacunacion errada, se procede con la eliminación del registro
--Eliminar una vacunacion
alter procedure EliminarVacunacion
    @FechaVacuna date,
    @CodMascota char (5),
    @TipoVacuna varchar(15),
    @Fabricante varchar (20),
    @Cuenta int,
    @Check bit out
AS BEGIN
    begin TRANSACTION
    delete from CalendariosVacunas
where FechaVacuna = @FechaVacuna
        and CodMascota = @CodMascota
        and TipoVacuna = @TipoVacuna
        and Fabricante = @Fabricante
    select @Cuenta = count(*)
    from CalendariosVacunas
    where FechaVacuna = @FechaVacuna
        and CodMascota = @CodMascota
        and TipoVacuna = @TipoVacuna
        and Fabricante = @Fabricante
    if @Cuenta = 0 BEGIN
        set @Check = 1
        SELECT @Check
    end
else begin
        set @Check = 0
        SELECT @Check
    end
END
GO;
--Registro de una estadía
alter procedure RegistrarEstadia
    @CheckIn date,
    @CodMascota char (5),
    @NroHab char (2),
    @Dias int,
    @Check bit out
AS BEGIN
    begin TRANSACTION
    if exists(
    select 1
    from Estadias
    where CheckIn = @CheckIn
        and CodMascota = @CodMascota
) begin
        set @Check = 0
        SELECT @Check
    end
else BEGIN
        declare @habcheck char(1)
        set @habcheck = (
        select Disponible
        from Habitaciones
        where NroHab = @NroHab
    )
        if @habcheck = 'D' BEGIN
            set @Check = 1
            SELECT @Check
            insert into Estadias
            values
                (@CheckIn, @CodMascota, @NroHab, NULL, @Dias)
            update Habitaciones
set Disponible = 'O'
where NroHab = @NroHab
        END
else
set @Check = 1
        SELECT @Check
    END
END
GO;
--Modificación de una estadía
alter PROCEDURE ModificarEstadia
    @CheckIn DATE,
    @CodMascota CHAR(5),
    @NroHab CHAR(2),
    @Campo VARCHAR(20),
    @NuevoValor VARCHAR(20),
    @Check BIT OUT
AS BEGIN
    BEGIN TRANSACTION;
    IF @Campo = 'NroHab' BEGIN
        UPDATE Habitaciones
SET Disponible = 'D'
WHERE NroHab = @NroHab;
        UPDATE Estadias
SET NroHab = @NuevoValor
WHERE CheckIn = @CheckIn
            AND CodMascota = @CodMascota
            AND NroHab = @NroHab;
        UPDATE Habitaciones
SET Disponible = 'O'
WHERE NroHab = @NuevoValor;
        IF EXISTS (
    SELECT 1
        FROM Estadias
        WHERE CheckIn = @CheckIn
            AND CodMascota = @CodMascota
            AND NroHab = @NuevoValor
) BEGIN
            SET @Check = 1;
            SELECT @Check;
        END
ELSE BEGIN
            SET @Check = 0;
            SELECT @Check;
        END;
    END
ELSE BEGIN
        DECLARE @SQL NVARCHAR(MAX);
        SET @SQL = N'UPDATE Estadias SET ' + QUOTENAME(@Campo) + ' = @NuevoValor WHERE CheckIn = @CheckIn AND CodMascota = @CodMascota AND NroHab = @NroHab';
        EXEC sp_executesql @SQL,
N'@CheckIn DATE, @CodMascota CHAR(5), @NuevoValor VARCHAR(20)',
@CheckIn,
@CodMascota,
@NuevoValor;
        IF EXISTS (
    SELECT 1
        FROM Estadias
        WHERE CheckIn = @CheckIn
            AND CodMascota = @CodMascota
            AND NroHab = @NroHab
            AND ' + QUOTENAME(@Campo) + ' = @NuevoValor
) BEGIN
            SET @Check = 1;
            SELECT @Check;
        END
ELSE BEGIN
            SET @Check = 0;
            SELECT @Check;
        END;
    END;
END
GO;
--Eliminar una estadía
alter procedure EliminarEstadia
    @CheckIn date,
    @CodMascota char (5),
    @NroHab char (2),
    @Cuenta int,
    @Check bit out
AS BEGIN
    begin TRANSACTION
    delete from Estadias
where CheckIn = @CheckIn
        and CodMascota = @CodMascota
        and NroHab = @NroHab
    SELECT @Cuenta = count(*)
    from Estadias
    where CheckIn = @CheckIn
        and CodMascota = @CodMascota
        and NroHab = @NroHab
    if @Cuenta = 0 BEGIN
        set @Check = 1
        SELECT @Check
    end
else begin
        set @Check = 0
        SELECT @Check
    end
END
GO;
create view TamañoMascotas
as
    select CodMascota,
        Tamaño
    from Mascotas
GO;
select *
from TamañoMascotas
declare CursorTamaños cursor for
select *
from TamañoMascotas
GO;
create view ServiciosEsp
as
    select IdServicio,
        Precio
    from Servicios
    where IdServicio = 'S04'
        or IdServicio = 'S05'
GO;
select *
from ServiciosEsp
declare CursorServiciosEsp cursor for
select *
from ServiciosEsp
GO;
--Procedimiento para registrar un requerimiento de un servicio en la estadía
alter procedure RegistrarRequerimiento
    @CodMascota char (5),
    @IdServicio char(3),
    @CheckIn date,
    @Cantidad int,
    @NroHab char (2),
    @Dias int,
    @Check bit out
AS BEGIN
    begin TRANSACTION
    if exists (
    select 1
    from Requerimientos
    where IdServicio = @IdServicio
        and CheckIn = @CheckIn
        and CodMascota = @CodMascota
        and NroHab = @NroHab
) begin
        set @Check = 0
        SELECT @Check
    end
else --los demás servicios que se pueden realizar varias veces y se cobran de acuerdo al tamaño, cantidad de veces
BEGIN
        DECLARE @Tamaño
        char
        (2),
    @Cargo money,
    @Factor float,
    @Precio money
        set @Check = 1
        SELECT @Check
        set @Tamaño
        =
        (
        select Tamaño
        from Mascotas
        where CodMascota = @CodMascota
    )
        set @Precio = (
        select Precio
        from Servicios
        where IdServicio = @IdServicio
    )
        if @Tamaño = 'S'
        set @Factor = 1
        if @Tamaño = 'M'
        set @Factor = 1.15
        if @Tamaño = 'G'
        set @Factor = 1.30
        if @Tamaño = 'XG'
        set @Factor = 1.40
        set @Cargo = @Cantidad * @Precio * @Factor
        insert into Requerimientos
        values
            (
                @IdServicio,
                @CheckIn,
                @CodMascota,
                @NroHab,
                @Cantidad,
                @Cargo
    )
        --son servicios especiales y no tienen cantidad, se cobra por la cantidad de dias
        if @IdServicio = 'S04'
            or @IdServicio = 'S05' BEGIN
            set @Cargo = (
        select Precio
            from Servicios
            where IdServicio = @IdServicio
    )
            set @Cargo * = @Dias
            insert into Requerimientos
            values
                (
                    @IdServicio,
                    @CheckIn,
                    @CodMascota,
                    @NroHab,
                    NULL,
                    @Cargo
    )
        END
        --servicios que pueden llegar a realizarse hasta una vez por estadía
        if @IdServicio = 'S02' BEGIN
            set @Cargo = (
        select Precio
            from Servicios
            where IdServicio = @IdServicio
    )
            insert into Requerimientos
            values
                (
                    @IdServicio,
                    @CheckIn,
                    @CodMascota,
                    @NroHab,
                    1,
                    @Cargo
    )
        END
else --los demás servicios que se pueden realizar varias veces y se cobran de acuerdo al tamaño, cantidad de veces
BEGIN
            set @Tamaño
            =
            (
        select Tamaño
            from Mascotas
            where CodMascota = @CodMascota
    )
            set @Precio = (
        select Precio
            from Servicios
            where IdServicio = @IdServicio
    )
            if @Tamaño = 'S'
            set @Factor = 1
            if @Tamaño = 'M'
            set @Factor = 1.15
            if @Tamaño = 'G'
            set @Factor = 1.30
            if @Tamaño = 'XG'
            set @Factor = 1.40
            set @Cargo = @Cantidad * @Precio * @Factor
            insert into Requerimientos
            values
                (
                    @IdServicio,
                    @CheckIn,
                    @CodMascota,
                    @NroHab,
                    @Cantidad,
                    @Cargo
    )
        END
    END
END
GO;
exec RegistrarRequerimiento 'M0030',
'S01',
'2023-05-25',
3,
'01',
3,
0
select *
from Requerimientos
GO
--Modificacion de requerimiento
alter procedure ModificarRequerimiento
    @IdServicio char (3),
    @CheckIn date,
    @CodMascota char (5),
    @NroHab char (2),
    @Campo varchar (10),
    @NuevoValor int,
    @Check bit out
AS BEGIN
    begin TRANSACTION
    if @IdServicio = 'S01'
        or @IdServicio = 'S03'
        or @IdServicio = 'S06' if @Campo = 'Cantidad' BEGIN
        DECLARE @Tamaño
        char
        (2),
    @Cargo money,
    @Factor float,
    @Precio money
        set @Tamaño
        =
        (
        select Tamaño
        from Mascotas
        where CodMascota = @CodMascota
    )
        set @Precio = (
        select Precio
        from Servicios
        where IdServicio = @IdServicio
    )
        if @Tamaño = 'S'
        set @Factor = 1
        if @Tamaño = 'M'
        set @Factor = 1.15
        if @Tamaño = 'G'
        set @Factor = 1.30
        if @Tamaño = 'XG'
        set @Factor = 1.40
        set @Cargo = @NuevoValor * @Precio * @Factor
        update Requerimientos
set Cantidad = @NuevoValor,
    Cargo = @Cargo
where IdServicio = @IdServicio
            and CheckIn = @CheckIn
            and CodMascota = @CodMascota
            and NroHab = @NroHab
    END
    if exists (
    select 1
    from Requerimientos
    where IdServicio = @IdServicio
        and CheckIn = @CheckIn
        and CodMascota = @CodMascota
        and NroHab = @NroHab
        and Cantidad = @NuevoValor
) begin
        set @Check = 1
        SELECT @Check
    end
else begin
        set @Check = 0
        SELECT @Check
    end
END
GO;
--Eliminación de requerimiento en la estadía
alter procedure EliminarRequerimiento
    @IdServicio char(3),
    @CheckIn date,
    @CodMascota char(5),
    @NroHab char(2),
    @Check bit out
AS BEGIN
    declare @Cuenta int
    begin TRANSACTION
    delete from Requerimientos
where IdServicio = @IdServicio
        and CheckIn = @CheckIn
        and CodMascota = @CodMascota
        and NroHab = @NroHab
    select @Cuenta = count(*)
    from Requerimientos
    where IdServicio = @IdServicio
        and CheckIn = @CheckIn
        and CodMascota = @CodMascota
        and NroHab = @NroHab
    if @Cuenta = 0 begin
        set @Check = 1
        SELECT @Check
    end
ELSE begin
        set @Check = 0
        SELECT @Check
    end
END
GO;
--Adicion de vacunas de nuevos proveedores
alter procedure AgregarVacuna
    @TipoVacuna varchar(15),
    @Fabricante varchar(20),
    @Precio money,
    @Check bit out
AS BEGIN
    begin TRANSACTION
    if exists (
    select 1
    from Vacunas
    where TipoVacuna = @TipoVacuna
        and Fabricante = @Fabricante
) begin
        set @Check = 0
        SELECT @Check
    end
else BEGIN
        set @Check = 1
        SELECT @Check
        insert into Vacunas
        values
            (@TipoVacuna, @Fabricante, @Precio)
    END
END
GO;
--Eliminar vacuna
alter procedure EliminarVacuna
    @TipoVacuna varchar(15),
    @Fabricante varchar (20),
    @Cuenta int,
    @Check bit out
AS BEGIN
    begin TRANSACTION
    delete from Vacunas
where TipoVacuna = @TipoVacuna
        and Fabricante = @Fabricante
    select @Cuenta = count (*)
    from Vacunas
    where TipoVacuna = @TipoVacuna
        and Fabricante = @Fabricante
    if @Cuenta = 0 begin
        set @Check = 1
        SELECT @Check
    end
ELSE begin
        set @Check = 0
        SELECT @Check
    end
END