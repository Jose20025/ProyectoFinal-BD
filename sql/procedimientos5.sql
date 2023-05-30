alter procedure BuscarMascota
@Campo varchar,
@Valor varchar (15)
AS  
BEGIN
    select * from Mascotas where @Campo=@Valor
end
exec BuscarMascota 'Alias','Tupac'

select Alias from Mascotas

declare @p bit; 
set @p = 1
begin TRANSACTION
exec ModificarMascota 'M0001','Color_pelo','Verde',1

select * from Mascotas	

--hay que modficarlo de acuerdo a lo que se deberia mostrar cuando se busca una