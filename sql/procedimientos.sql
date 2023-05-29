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
    if exists(select 1 from Clientes
                where Apellido=@Apellido and NroCuenta=@NroCuenta and Telefono=@Telefono)   
        set @Check = 0
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
        
        insert into Clientes values (@pIdCliente,@Apellido,@NroCuenta,@Direccion,@Telefono)
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
    update Clientes set @Campo = @NuevoValor where IdCliente = @IdCliente
    if exists (select 1 from Clientes where IdCliente=@IdCliente and @Campo=@NuevoValor)
        set @Check = 1
    ELSE
        set @Check = 0
END
GO;

--Eliminacion de cliente
alter procedure EliminarCliente
@IdCliente char (5),
@Cuenta int,
@Check bit out
AS
BEGIN
    begin TRANSACTION
    delete from Clientes where IdCliente = @IdCliente
    select @Cuenta = count(*) from Clientes where IdCliente=@IdCliente
    if (@Cuenta = 0)
        set @Check = 1
    else
        set @Check = 0
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
@Check bit out
AS 
BEGIN
    begin TRANSACTION
    if exists (select 1 from Mascotas 
                where Alias=@Alias and Especie=@Especie and IdCliente=@IdCliente)
        set @Check = 0
    else
        BEGIN
        set @Check = 1
        DECLARE
        @DatoCod int = next value for SecCodMascota,
        @pCodMascota char(5)
        
        IF @DatoCod<100
            set @pCodMascota = CONCAT('M00', CONVERT(char(2),@DatoCod))
        Else IF @DatoCod<1000
            set @pCodMascota = CONCAT('M0', CONVERT(char(3),@DatoCod))
        ELSE
            set @pCodMascota = CONCAT('M', CONVERT(char(4),@DatoCod))
        
        insert into Mascotas values (@pCodMascota,@IdCliente,@Alias,@Especie,@Raza,@Color_pelo,@FechaNac,@Tamaño)
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
    update Mascotas set @Campo = @NuevoValor where CodMascota = @CodMascota
    if exists (select 1 from Mascotas where CodMascota=@CodMascota and @Campo=@NuevoValor)
        set @Check = 1
    else
        set @Check = 0
END
GO;

--Eliminacion de mascota
alter procedure EliminarMascota
@CodMascota char (5),
@Cuenta int,
@Check bit out
AS
BEGIN
    begin TRANSACTION
    delete from Mascotas where CodMascota = @CodMascota
    select @Cuenta = count(*) from Mascotas where CodMascota=@CodMascota 
    if @Cuenta = 0
        set @Check = 1
    ELSE
        set @Check = 0
END
GO;

--Procedimiento de registro de una persona y su asignación al cliente
alter procedure RegistrarPersona
@CI varchar(10),
@Nombre varchar (30),
@IdCliente char(5),
@Check bit out
AS
BEGIN
    begin TRANSACTION
    if exists (select 1 from Personas where Ci = @CI)
        set @Check = 0
    else
        BEGIN
        set @Check = 1
        insert into Personas values (@CI,@Nombre)
        insert into Encargados values (@IdCliente,@CI)
        END
END 
GO;

--Modificación de una Persona
alter procedure ModfiicarPersona
@CI varchar (10),
@NuevoNombre varchar (30),
@Check bit out
AS
BEGIN
    begin TRANSACTION 
    update Personas set Nombre = @NuevoNombre where CI = @CI
    if exists (select 1 from Personas where CI=@CI and Nombre=@NuevoNombre)
        set @Check = 1
    else
        set @Check = 0
END
GO;

--Eliminación de persona
alter procedure EliminarPersona
@CI varchar (10),
@Cuenta int,
@Check bit out
AS 
BEGIN  
    begin TRANSACTION
    delete from Personas where CI=@CI 
    select @Cuenta = count(*) from Personas where CI=@CI
    if @Cuenta = 0
        set @Check = 1
    ELSE
        set @Check = 0
END
GO;