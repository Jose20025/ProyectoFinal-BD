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

select Alias from Mascotas

declare @p bit; 
set @p = 1
begin TRANSACTION
exec ModificarMascota 'M0001','Color_pelo','Verde',1

select * from Mascotas	

--hay que modficarlo de acuerdo a lo que se deberia mostrar cuando se busca una
go
alter procedure InfoMascota
@CodMascota char(5)
AS
begin
select Alias,Color_pelo,Raza,Tamaño,Apellido,Clientes.IdCliente,Especie,CodMascota from Mascotas
inner join Clientes on Clientes.IdCliente = Mascotas.IdCliente
where CodMascota = @CodMascota
end


select * from Mascotas

GO

select Alias,Color_pelo,Raza,Tamaño,Apellido,Clientes.IdCliente,Especie,CodMascota from Mascotas
inner join Clientes on Clientes.IdCliente = Mascotas.IdCliente
where CodMascota = @CodMascota