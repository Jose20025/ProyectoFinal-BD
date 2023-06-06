alter procedure BuscarMascota
    @Campo varchar (10),
    @Valor varchar (15)
AS  
BEGIN
    declare @SQL nvarchar(max)

    set @SQL = N'select distinct Mascotas.CodMascota,Alias,Apellido,Especie,Color_pelo from Mascotas
                inner join Clientes on Clientes.IdCliente = Mascotas.IdCliente
                inner join HistorialesPeso on HistorialesPeso.CodMascota = Mascotas.CodMascota
                where' +QUOTENAME(@Campo)+'=@Valor'

    exec sp_executesql @SQL, N'@Valor varchar(15)',@Valor
end
go

create procedure BuscarHuespedes
    @Campo varchar (10),
    @Valor varchar (15)
AS
BEGIN
    declare @SQL nvarchar(max)

    set @SQL = N'select distinct Mascotas.CodMascota,Alias,Apellido,Especie,Color_pelo from Mascotas
                inner join Clientes on Clientes.IdCliente = Mascotas.IdCliente
                inner join Estadias on Estadias.CodMascota = Mascotas.CodMascota
                where' +QUOTENAME(@Campo)+'=@Valor'

    exec sp_executesql @SQL, N'@Valor varchar(15)',@Valor
end

--hay que modficarlo de acuerdo a lo que se deberia mostrar cuando se busca una
go
alter procedure InfoMascota
    @CodMascota char(5)
AS
begin
    select Alias, Color_pelo, Raza, Tamaño, Apellido, Clientes.IdCliente, Especie, CodMascota
    from Mascotas
        inner join Clientes on Clientes.IdCliente = Mascotas.IdCliente
    where CodMascota = @CodMascota
end
go

alter procedure VerificarExistenciaCliente
    @IdCliente char(5),
    @Check bit out
AS
begin
    if exists (select 1
    from Clientes
    where IdCliente = @IdCliente)
        BEGIN
        set @Check = 1
        select @Check
    END
    else
        BEGIN
        set @Check = 0
        select @Check
    END
END
GO

create procedure HistorialPeso
    @CodMascota char (5)
AS
select CONCAT(convert(varchar(2),FORMAT(FechaPeso,'dd','es-BO')),' ',
              convert(varchar(10),FORMAT(FechaPeso,'MMMM','es-BO')),' ',
              convert(varchar(4),FORMAT(FechaPeso,'yyyy','es-BO'))
            ) as 'Fecha',
    CONCAT(convert(char(5),Peso),'kg') as 'Peso'
from HistorialesPeso
where CodMascota = @CodMascota
order by FechaPeso ASC
go

create procedure HistorialVacunacion
    @CodMascota char (5)
AS
select CONCAT(convert(varchar(2),FORMAT(FechaVacuna,'dd','es-BO')),' ',
              convert(varchar(10),FORMAT(FechaVacuna,'MMMM','es-BO')),' ',
              convert(varchar(4),FORMAT(FechaVacuna,'yyyy','es-BO'))
            ) as 'Fecha',
    TipoVacuna as 'Vacuna',
    Fabricante
from CalendariosVacunas
where CodMascota = @CodMascota
order by FechaVacuna ASC
go

create procedure PesoReciente
    @CodMascota char (5)
as
BEGIN
    select top 1
        concat(convert(varchar(4),Peso),' kg'), FechaPeso
    from HistorialesPeso
    where CodMascota=@CodMascota
    order by FechaPeso desc
END
go

create procedure VacunaReciente
    @CodMascota char (5)
as
BEGIN
    select top 1
        TipoVacuna, FechaVacuna
    from CalendariosVacunas
    where CodMascota=@CodMascota
    order by FechaVacuna desc
END
go

create procedure SituacionReciente
    @CodMascota char (5)
as
BEGIN
    select top 1
        Situacion, FechaConsulta
    from HistorialesMedicos
    where CodMascota=@CodMascota
    order by FechaConsulta desc
END
GO

create procedure ObtenerEstadiasActuales
as
select Mascotas.CodMascota, Alias, Especie, CheckIn, NroHab, Dias
from Estadias
    inner join Mascotas on Mascotas.CodMascota = Estadias.CodMascota
where CheckOut is NULL
go

create procedure ServiciosSolicitados
    @CodMascota char (5),
    @CheckIn date,
    @NroHab char(2)
as
select TipoServ, Cantidad
from Requerimientos
    inner join Servicios on Servicios.IdServicio = Requerimientos.IdServicio
where CodMascota=@CodMascota and CheckIn=@CheckIn and NroHab=@NroHab
go

create procedure HabDisponibles
AS
select NroHab
from Habitaciones
where Disponible= 'D'
order by try_cast(NroHab as int), NroHab desc