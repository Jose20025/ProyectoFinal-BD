alter procedure BuscarMascota
    @Campo varchar (10),
    @Valor varchar (15)
AS  
BEGIN
    declare @SQL nvarchar(max)

    set @SQL = N'select CodMascota,Alias,Apellido,Especie,Color_pelo from Mascotas
                inner join Clientes on Clientes.IdCliente = Mascotas.IdCliente
                where' +QUOTENAME(@Campo)+'=@Valor'

    exec sp_executesql @SQL, N'@Valor varchar(15)',@Valor
end
exec BuscarMascota 'Alias','Tupac'

select Alias
from Mascotas

declare @p bit; 
set @p = 1
begin TRANSACTION
exec ModificarMascota 'M0001','Color_pelo','Verde',1

select *
from Mascotas	

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

ALTER procedure VerificarExistenciaCliente
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

alter procedure HistorialPeso
@CodMascota char (5)
AS
select CONCAT(convert(varchar(2),FORMAT(FechaPeso,'dd','es-BO')),' ',
              convert(varchar(10),FORMAT(FechaPeso,'MMMM','es-BO')),' ',
              convert(varchar(4),FORMAT(FechaPeso,'yyyy','es-BO'))
            ) as 'Fecha',
        CONCAT(convert(char(5),Peso),'kg') as 'Peso' 
        from HistorialesPeso where CodMascota = @CodMascota order by FechaPeso ASC
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
        from CalendariosVacunas where CodMascota = @CodMascota order by FechaVacuna ASC
go

alter procedure PesoReciente
@CodMascota char (5)
as
BEGIN
    select top 1 concat(convert(varchar(4),Peso),' kg'),FechaPeso from HistorialesPeso where CodMascota=@CodMascota order by FechaPeso desc
END
go

create procedure VacunaReciente
@CodMascota char (5)
as
BEGIN
    select top 1 TipoVacuna,FechaVacuna from CalendariosVacunas where CodMascota=@CodMascota order by FechaVacuna desc
END
go

create procedure SituacionReciente
@CodMascota char (5)
as
BEGIN
    select top 1 Situacion,FechaConsulta from HistorialesMedicos where CodMascota=@CodMascota order by FechaConsulta desc
END

select * from Vacunas
