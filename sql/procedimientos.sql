--secuencia para ID de cliente
CREATE SEQUENCE SecIdCliente
    START WITH 19
    INCREMENT BY 1
    NO MAXVALUE;
GO;

--Procedimiento para registrar un cliente
create procedure RegistrarCliente  
@Apellido varchar(20), 
@NroCuenta varchar(10), 
@Direccion varchar(40), 
@Telefono varchar(14)
AS 
BEGIN
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

--Secuencia para Codigo de mascota
CREATE SEQUENCE SecCodMascota
    START WITH 28
    INCREMENT BY 1
    NO MAXVALUE;
GO;

--Procedimiento para registrar una mascota
create procedure RegistrarMascota  
@IdCliente varchar(20), 
@Alias varchar(10), 
@Especie varchar(40), 
@Raza varchar(14),
@Color_pelo varchar (15),
@FechaNac date,
@Tamaño char(2)
AS 
BEGIN
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
GO;

--Procedimiento de registro de una persona y su asignación al cliente
create procedure RegistrarPersona
@CI varchar(10),
@Nombre varchar (30),
@IdCliente char(5) 
AS
insert into Personas values (@CI,@Nombre)
insert into Encargados values (@IdCliente,@CI)
GO;
