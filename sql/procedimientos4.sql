--Vista para huespedes actuales
create view HuespedesActuales as
select CheckIn,Alias,Especie,Habitaciones.NroHab,Dias from Mascotas
inner join Estadias on Estadias.CodMascota = Mascotas.CodMascota
inner join Habitaciones on Habitaciones.NroHab = Estadias.NroHab
where CheckOut is NULL
GO

--Vista para huespedes atendidos
create view HuespedesAtendidos as
select CheckIn,CheckOut,Alias,Especie,Habitaciones.NroHab,Dias from Mascotas
inner join Estadias on Estadias.CodMascota = Mascotas.CodMascota
inner join Habitaciones on Habitaciones.NroHab = Estadias.NroHab
where CheckOut is not NULL
GO

alter procedure ReporteAtendidos
@FechaInicial date,
@FechaFinal date
AS
BEGIN
    declare @TablaTexto table (TextoPrint nvarchar(MAX)) 
    declare @TextoPrint NVARCHAR(max)
    set @TextoPrint += ''
    set @TextoPrint += '     MASCOTAS ATENDIDAS ENTRE: '+convert(varchar(10),@FechaInicial)+' y '+convert(varchar(10),@FechaFinal)
    set @TextoPrint += ''
    if exists (select 1 from Estadias where CheckIn >= @FechaInicial and CheckIn <=  @FechaFinal)
        BEGIN
        DECLARE CursorAtendidos cursor for select * from HuespedesAtendidos  
            where CheckIn BETWEEN @FechaInicial and @FechaFinal order by CheckIn
        DECLARE
        @InAux date,
        @OutAux date,
        @Alias varchar(20),
        @Especie varchar(15),
        @Hab char(2),
        @Dias int,
        @cantidad int = 0
        set @TextoPrint += '―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――'
        set @TextoPrint += '|  CHECK-IN     -     MASCOTA     -     DIAS     -     HABITACIÓN     -     CHECK-OUT     |'
        set @TextoPrint += '―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――'
        open CursorAtendidos
        fetch next from CursorAtendidos into @InAux,@OutAux,@Alias,@Especie,@Hab,@Dias
        while(@@FETCH_STATUS=0)
            BEGIN
            set @TextoPrint +=   '  '+CONVERT(VARCHAR(10),@InAux) + REPLICATE(' ',10)+
                    @Alias + REPLICATE(' ',19 - LEN(@Alias)) +
                    CONVERT(CHAR(2), @Dias) + REPLICATE(' ',16)+
                    @Hab + REPLICATE(' ',15)
                    + CONVERT(VARCHAR(10), @OutAux);
            set @cantidad += 1
            fetch next from CursorAtendidos into @InAux,@OutAux,@Alias,@Especie,@Hab,@Dias
            END
        close CursorAtendidos
        deallocate CursorAtendidos
        set @TextoPrint += ''
        set @TextoPrint += ''
        set @TextoPrint += 'Habiendo atendido un total de '+convert(char(3),@cantidad)+'mascota(s) entre estas fechas'
        set @cantidad=0
        END
    ELSE    
        set @TextoPrint += 'No se ha registrado ningún huesped entre estas fechas'

    if exists (select 1 from Estadias where CheckOut is NULL)
        BEGIN
        set @TextoPrint += ''
        set @TextoPrint += ''
        set @TextoPrint += '         MASCOTAS HOSPEDADAS ACTUALMENTE'
        set @TextoPrint += ''
        set @TextoPrint += '――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――'
        set @TextoPrint += '|  CHECK-IN     -     MASCOTA     -     DIAS     -     HABITACIÓN    |'
        set @TextoPrint += '――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――'
        declare CursorHuespedes cursor for select * from HuespedesActuales
        open CursorHuespedes
        fetch next from CursorHuespedes into @InAux,@Alias,@Especie,@Hab,@Dias
        while(@@FETCH_STATUS=0)
            BEGIN 
            set @TextoPrint +=   '  '+CONVERT(VARCHAR(10),@InAux) + REPLICATE(' ',10)+
                    @Alias + REPLICATE(' ',19 - LEN(@Alias)) +
                    CONVERT(CHAR(2), @Dias) + REPLICATE(' ',16)+
                    @Hab
            set @cantidad += 1
            fetch next from CursorHuespedes into @InAux,@Alias,@Especie,@Hab,@Dias
            END
        close CursorHuespedes
        deallocate CursorHuespedes
        set @TextoPrint += ''
        set @TextoPrint += ''
        set @TextoPrint += 'Teniendo en este momento un total de '+convert(char(3),@cantidad)+'mascota(s) hospedadas en el hotel'
        END	
    ELSE
        set @TextoPrint += 'Ningún huesped se encuentra actualmente hospedado'
    insert into @TablaTexto (TextoPrint) values (@TextoPrint)
    SELECT TextoPrint from @TablaTexto
END
