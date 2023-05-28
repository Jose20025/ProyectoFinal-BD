create view ConsumosEstadia as 
select Mascotas.CodMascota,Estadias.CheckIn, TipoServ,Cantidad,Cargo from Servicios
inner join Requerimientos on Requerimientos.IdServicio = Servicios.IdServicio
inner join Estadias on Estadias.CheckIn=Requerimientos.CheckIn and Estadias.CodMascota=Requerimientos.CodMascota
inner join Mascotas on Mascotas.CodMascota=Estadias.CodMascota
GO;

select * from ConsumosEstadia order by CodMascota,CheckIn
GO;

create procedure CheckOutHuesped
@CheckIn date,
@CheckOut date,
@CodMascota char(5),
@NroHab char (2)
AS
BEGIN
    declare CursorConsumos cursor for select CheckIn,CodMascota,TipoServ,Cantidad,Cargo from ConsumosEstadia
    update Estadias set CheckOut=@CheckOut                                  --se coloca la fecha
    where CheckIn=@CheckIn and CodMascota=@CodMascota and NroHab=@NroHab
    update Habitaciones set Disponible = 'D' where NroHab=@NroHab           --la habitación esta disponible
    DECLARE
    @CheckAux date,
    @CodAux char (5),
    @TipoServAux varchar (20),
    @Cantidad int,
    @Cargo money,
    @Sumador money = 0,
    @Alias varchar (20) = (select Alias from Mascotas where CodMascota = @CodMascota),
    @PrecioHotel money = (select Dias from Estadias where CheckIn=@CheckIn and CodMascota=@CodMascota and NroHab=@NroHab) * 60,
    @Dias char (2) = (select Dias from Estadias where CheckIn=@CheckIn and CodMascota=@CodMascota and NroHab=@NroHab)
    print 'La mascota '+@Alias+ ' a fecha de hoy, '+CONVERT(varchar (10), @CheckOut)+ ' realiza su Check Out de nuestro hotel.' 
    print ''
    print 'Por la estadía de '+@Dias+ 'dias en el hotel se genera un total de: Bs. '+convert(varchar(10),@PrecioHotel)
    print ''
    if Exists (select 1 from Requerimientos where CheckIn = @CheckIn and CodMascota=@CodMascota and NroHab=  @NroHab)
        BEGIN
        print 'Ademas, Habiendo solicitado los siguientes servicios';
        print ''
        print '―――――――――――――――――――――――――――――――――――――――――――――――――'
        print '|  SERVICIO     -     CANTIDAD     -     CARGO  |'
        print '―――――――――――――――――――――――――――――――――――――――――――――――――'
        print ''
        open CursorConsumos
        fetch next from CursorConsumos into @CheckAux,@CodAux,@TipoServAux,@Cantidad,@Cargo
        while(@@FETCH_STATUS=0)
            BEGIN
            if (@CheckAux = @CheckIn and @CodAux = @CodMascota)
                BEGIN
                if @Cantidad is NULL
                    SET @Cantidad = 1
                PRINT '  ' + @TipoServAux + REPLICATE(' ', 22 - LEN(@TipoServAux))
                        + ' ' + CONVERT(VARCHAR(18), @Cantidad) + REPLICATE(' ', 15 - LEN(CONVERT(VARCHAR(20), @Cantidad)))
                        + ' ' + CONVERT(VARCHAR(10), @Cargo) + REPLICATE(' ', 10 - LEN(CONVERT(VARCHAR(10), @Cargo)));
                set @Sumador += @Cargo
                END
            fetch next from CursorConsumos into @CheckAux,@CodAux,@TipoServAux,@Cantidad,@Cargo
            END 
        close CursorConsumos    
        DEALLOCATE CursorConsumos
        END
    ELSE
        print'No habiendo solicitado ningún servicio adicional'
        print''
    print' '
    print'Generándose un total de Bs. '+convert(varchar(10),(@PrecioHotel+@Sumador))+' por la estadía en el hotel'
    print''
    print'Atte. Hotel Happy Fox'
END

select * from Servicios

exec RegistrarMascota 'C0001','Gato-Test','Felino','Rara','Morado','2023-05-25','M'
exec RegistrarMascota 'C0001','Gato-Test2','Felino','Rara','Verde','2023-05-25','M'
select * from Mascotas

exec RegistrarEstadia '2023-05-26','M0029','01',3

exec RegistrarRequerimiento 'M0029','S01','2023-05-26',2,'01',2
exec RegistrarRequerimiento 'M0029','S02','2023-05-26',17,'01',2 --aunque ponemos 17 cortes de uñas, el procedimiento registra solo 1
exec RegistrarRequerimiento 'M0029','S03','2023-05-26',4,'01',2
exec RegistrarRequerimiento 'M0029','S04','2023-05-26',285,'01',2 --aunque ponemos 285 alimentaciones especiales, se pone null la cantidad porque es un servicio especial y se cobra por dia
exec RegistrarRequerimiento 'M0029','S05','2023-05-26',128,'01',2 -- igual con este
exec RegistrarRequerimiento 'M0029','S06','2023-05-26',3,'01',2

select * from Requerimientos

select * from Estadias

select * from Habitaciones -- solo la 1 estaria ocupada

exec CheckOutHuesped '2023-05-26','2023-05-27','M0029','01'