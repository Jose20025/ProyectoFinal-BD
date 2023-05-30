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
    DECLARE @ver varchar(10)
    set @ver = (select CheckOut from Estadias where CheckIn=@CheckIn and CodMascota=@CodMascota and NroHab=@NroHab)
    if @ver is NULL
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
    ELSE   
        print 'Ya se ha realizado este Checkout'
END