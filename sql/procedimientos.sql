--secuencia para ID de cliente
CREATE SEQUENCE SecIdCliente
    START WITH 19
    INCREMENT BY 1
    NO MAXVALUE;
GO;


--Procedimiento para registrar un cliente
alter procedure RegistrarCliente
    @Apellido varchar(20),
    @NroCuenta varchar(10),
    @Direccion varchar(40),
    @Telefono varchar(14),
    @Check bit out
AS 
BEGIN
    begin TRANSACTION
    if exists(select 1
    from Clientes
    where Apellido=@Apellido and NroCuenta=@NroCuenta and Telefono=@Telefono)   
        begin
        set @Check = 0
        select @Check
    end
    ELSE
        set @Check = 1
    DECLARE
        @DatoID int = next value for SecIdCliente,
        @pIdCliente char(5)

    IF @DatoID<100
            set @pIdCliente = CONCAT('C00', CONVERT(char(2),@DatoID))
        Else IF @DatoID<1000
            set @pIdCliente = CONCAT('C0', CONVERT(char(3),@DatoID))
        ELSE
            set @pIdCliente = CONCAT('C', CONVERT(char(4),@DatoID))

    SELECT @Check, @pIdCliente
    insert into Clientes
    values
        (@pIdCliente, @Apellido, @NroCuenta, @Direccion, @Telefono)

END
GO;

--Modificación de datos de un cliente
alter procedure ModificarCliente 
@IdCliente char (5),
@Campo varchar(15),
@NuevoValor varchar (20),
@Check bit out
AS
BEGIN
    begin TRANSACTION
    declare @SQL NVARCHAR(MAX)
    set @SQL = N'UPDATE Clientes set '+ QUOTENAME(@Campo)+' = @NuevoValor WHERE IdCliente = @IdCliente'
    exec sp_executesql @SQL, N'@IdCliente char(5), @NuevoValor varchar(20)',@IdCliente,@NuevoValor
    if exists (select 1 from Clientes where IdCliente=@IdCliente and (NroCuenta=@NuevoValor or Telefono=@NuevoValor))
        BEGIN
        set @Check = 1
        SELECT @Check
        END
    ELSE
        BEGIN
        set @Check = 0
        SELECT @Check
        END
END
GO;

--Eliminacion de cliente
create procedure EliminarCliente
    @IdCliente char (5),
    @Cuenta int,
    @Check bit out
AS
BEGIN
    begin TRANSACTION
    delete from Clientes where IdCliente = @IdCliente
    select @Cuenta = count(*)
    from Clientes
    where IdCliente=@IdCliente
    if (@Cuenta = 0)
        BEGIN
        set @Check = 1
        SELECT @Check
    END
    else
        BEGIN
        set @Check = 0
        SELECT @Check
    END
END
GO;

--Secuencia para Codigo de mascota
CREATE SEQUENCE SecCodMascota
    START WITH 28
    INCREMENT BY 1
    NO MAXVALUE;
GO;

--Procedimiento para registrar una mascota 
alter procedure RegistrarMascota
    @IdCliente varchar(20),
    @Alias varchar(20),
    @Especie varchar(40),
    @Raza varchar(14),
    @Color_pelo varchar (15),
    @FechaNac date,
    @Tamaño char(2),
    @Check bit out,
AS 
BEGIN
    begin TRANSACTION
    if exists (select 1
    from Mascotas
    where Alias=@Alias and Especie=@Especie and IdCliente=@IdCliente)
        BEGIN
        set @Check = 0
        select @Check
        rollback
    END
    else
        BEGIN
        set @Check = 1
        select @Check
        DECLARE
        @DatoCod int = next value for SecCodMascota,
        @pCodMascota char(5)
        IF @DatoCod<100
            set @pCodMascota = CONCAT('M00', CONVERT(char(2),@DatoCod))
        Else IF @DatoCod<1000
            set @pCodMascota = CONCAT('M0', CONVERT(char(3),@DatoCod))
        ELSE
            set @pCodMascota = CONCAT('M', CONVERT(char(4),@DatoCod))

        insert into Mascotas
        values
            (@pCodMascota, @IdCliente, @Alias, @Especie, @Raza, @Color_pelo, @FechaNac, @Tamaño)
        commit
    END
END
GO;


--Modificación de datos de una mascota
alter procedure ModificarMascota
    @CodMascota char (5),
    @Campo varchar(15),
    @NuevoValor varchar (20),
    @Check bit out
as 
BEGIN
    begin TRANSACTION
    declare @SQL NVARCHAR(MAX)
    set @SQL = N'UPDATE Mascotas set '+ QUOTENAME(@Campo)+' = @NuevoValor WHERE CodMascota = @CodMascota'
    exec sp_executesql @SQL, N'@CodMascota char(5), @NuevoValor varchar(20)',@CodMascota,@NuevoValor
    if exists (select 1
    from Mascotas
    where CodMascota=@CodMascota and (Color_pelo=@NuevoValor or Alias=@NuevoValor or Raza=@NuevoValor))
        BEGIN
        set @Check = 1
        SELECT @Check
    END
    else
        BEGIN
        set @Check = 0
        SELECT @Check
    END
END
GO;



--Eliminacion de mascota
create procedure EliminarMascota
    @CodMascota char (5),
    @Cuenta int,
    @Check bit out
AS
BEGIN
    begin TRANSACTION
    delete from Mascotas where CodMascota = @CodMascota
    select @Cuenta = count(*)
    from Mascotas
    where CodMascota=@CodMascota
    if @Cuenta = 0
        BEGIN
        set @Check = 1
        SELECT @Check
    end
    ELSE
        begin
        set @Check = 0
        SELECT @Check
    end
END
GO;

--Procedimiento de registro de una persona y su asignación al cliente
create procedure RegistrarPersona
    @CI varchar(10),
    @Nombre varchar (30),
    @IdCliente char(5),
    @Check bit out
AS
BEGIN
    begin TRANSACTION
    if exists (select 1
    from Personas
    where Ci = @CI)
        BEGIN
        set @Check = 0
        SELECT @Check
    END
    else
        BEGIN
        set @Check = 1
        SELECT @Check
        insert into Personas
        values
            (@CI, @Nombre)
        insert into Encargados
        values
            (@IdCliente, @CI)
    END
END 
GO;

--Eliminación de persona
create procedure EliminarPersona
    @CI varchar (10),
    @Cuenta int,
    @Check bit out
AS
BEGIN
    begin TRANSACTION
    delete from Personas where CI=@CI
    select @Cuenta = count(*)
    from Personas
    where CI=@CI
    if @Cuenta = 0
        BEGIN
        set @Check = 1
        SELECT @Check
    END
    ELSE
        BEGIN
        set @Check = 0
        SELECT @Check
    END
END
GO;
