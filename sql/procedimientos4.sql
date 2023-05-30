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
    print ''
    print '     MASCOTAS ATENDIDAS ENTRE: '+convert(varchar(10),@FechaInicial)+' y '+convert(varchar(10),@FechaFinal)
    print ''
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
        print '―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――'
        print '|  CHECK-IN     -     MASCOTA     -     DIAS     -     HABITACIÓN     -     CHECK-OUT     |'
        print '―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――'
        open CursorAtendidos
        fetch next from CursorAtendidos into @InAux,@OutAux,@Alias,@Especie,@Hab,@Dias
        while(@@FETCH_STATUS=0)
            BEGIN
            print   '  '+CONVERT(VARCHAR(10),@InAux) + REPLICATE(' ',10)+
                    @Alias + REPLICATE(' ',19 - LEN(@Alias)) +
                    CONVERT(CHAR(2), @Dias) + REPLICATE(' ',16)+
                    @Hab + REPLICATE(' ',15)
                    + CONVERT(VARCHAR(10), @OutAux);
            set @cantidad += 1
            fetch next from CursorAtendidos into @InAux,@OutAux,@Alias,@Especie,@Hab,@Dias
            END
        close CursorAtendidos
        deallocate CursorAtendidos
        print ''
        print ''
        print 'Habiendo atendido un total de '+convert(char(3),@cantidad)+'mascota(s) entre estas fechas'
        set @cantidad=0
        END
    ELSE    
        print 'No se ha registrado ningún huesped entre estas fechas'

    if exists (select 1 from Estadias where CheckOut is NULL)
        BEGIN
        print ''
        print ''
        print '         MASCOTAS HOSPEDADAS ACTUALMENTE'
        print ''
        print '――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――'
        print '|  CHECK-IN     -     MASCOTA     -     DIAS     -     HABITACIÓN    |'
        print '――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――'
        declare CursorHuespedes cursor for select * from HuespedesActuales
        open CursorHuespedes
        fetch next from CursorHuespedes into @InAux,@Alias,@Especie,@Hab,@Dias
        while(@@FETCH_STATUS=0)
            BEGIN 
            print   '  '+CONVERT(VARCHAR(10),@InAux) + REPLICATE(' ',10)+
                    @Alias + REPLICATE(' ',19 - LEN(@Alias)) +
                    CONVERT(CHAR(2), @Dias) + REPLICATE(' ',16)+
                    @Hab
            set @cantidad += 1
            fetch next from CursorHuespedes into @InAux,@Alias,@Especie,@Hab,@Dias
            END
        close CursorHuespedes
        deallocate CursorHuespedes
        print ''
        print ''
        print 'Teniendo en este momento un total de '+convert(char(3),@cantidad)+'mascota(s) hospedadas en el hotel'
        END	
    ELSE
        print 'Ningún huesped se encuentra actualmente hospedado'
END
GO

alter procedure ReporteAtendidos2
@FechaInicial date,
@FechaFinal date
AS
BEGIN
    DECLARE @PrintTable TABLE (PrintText NVARCHAR(MAX))
    DECLARE @PrintText NVARCHAR(MAX)
    set @PrintText ='' ;insert into @PrintTable values (@PrintText)    
    set @PrintText = '';insert into @PrintTable values (@PrintText)  
    set @PrintText = '     MASCOTAS ATENDIDAS ENTRE: '+convert(varchar(10),@FechaInicial)+' y '+convert(varchar(10),@FechaFinal);insert into @PrintTable values (@PrintText)  
    set @PrintText = '';insert into @PrintTable values (@PrintText)  
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
        set @PrintText = '―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――';insert into @PrintTable values (@PrintText)  
        set @PrintText = '|  CHECK-IN     -     MASCOTA     -     DIAS     -     HABITACIÓN     -     CHECK-OUT     |';insert into @PrintTable values (@PrintText)  
        set @PrintText = '―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――';insert into @PrintTable values (@PrintText)  
        open CursorAtendidos
        fetch next from CursorAtendidos into @InAux,@OutAux,@Alias,@Especie,@Hab,@Dias
        while(@@FETCH_STATUS=0)
            BEGIN
            set @PrintText =   '  '+CONVERT(VARCHAR(10),@InAux) + REPLICATE(' ',10)+
                    @Alias + REPLICATE(' ',19 - LEN(@Alias)) +
                    CONVERT(CHAR(2), @Dias) + REPLICATE(' ',16)+
                    @Hab + REPLICATE(' ',15)
                    + CONVERT(VARCHAR(10), @OutAux);
            insert into @PrintTable values (@PrintText)  
            set @cantidad += 1
            fetch next from CursorAtendidos into @InAux,@OutAux,@Alias,@Especie,@Hab,@Dias
            END
        close CursorAtendidos
        deallocate CursorAtendidos
        set @PrintText = '';insert into @PrintTable values (@PrintText)  
        set @PrintText = '';insert into @PrintTable values (@PrintText)  
        set @PrintText = 'Habiendo atendido un total de '+convert(char(3),@cantidad)+'mascota(s) entre estas fechas';insert into @PrintTable values (@PrintText)  
        set @cantidad=0
        END
    ELSE    
        set @PrintText = 'No se ha registrado ningún huesped entre estas fechas';insert into @PrintTable values (@PrintText)  

    if exists (select 1 from Estadias where CheckOut is NULL)
        BEGIN
        set @PrintText = '';insert into @PrintTable values (@PrintText)  
        set @PrintText = '';insert into @PrintTable values (@PrintText)  
        set @PrintText = '         MASCOTAS HOSPEDADAS ACTUALMENTE';insert into @PrintTable values (@PrintText)  
        set @PrintText = '';insert into @PrintTable values (@PrintText)  
        set @PrintText = '――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――';insert into @PrintTable values (@PrintText)  
        set @PrintText = '|  CHECK-IN     -     MASCOTA     -     DIAS     -     HABITACIÓN    |';insert into @PrintTable values (@PrintText)  
        set @PrintText = '――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――';insert into @PrintTable values (@PrintText)  
        declare CursorHuespedes cursor for select * from HuespedesActuales
        open CursorHuespedes
        fetch next from CursorHuespedes into @InAux,@Alias,@Especie,@Hab,@Dias
        while(@@FETCH_STATUS=0)
            BEGIN 
            set @PrintText =   '  '+CONVERT(VARCHAR(10),@InAux) + REPLICATE(' ',10)+
                    @Alias + REPLICATE(' ',19 - LEN(@Alias)) +
                    CONVERT(CHAR(2), @Dias) + REPLICATE(' ',16)+
                    @Hab
            insert into @PrintTable values (@PrintText)  
            set @cantidad += 1
            fetch next from CursorHuespedes into @InAux,@Alias,@Especie,@Hab,@Dias
            END
        close CursorHuespedes
        deallocate CursorHuespedes
        set @PrintText = '';insert into @PrintTable values (@PrintText)  
        set @PrintText = '';insert into @PrintTable values (@PrintText)  
        set @PrintText = 'Teniendo en este momento un total de '+convert(char(3),@cantidad)+'mascota(s) hospedadas en el hotel';insert into @PrintTable values (@PrintText)  
        END	
    ELSE
        set @PrintText = 'Ningún huesped se encuentra actualmente hospedado' ;insert into @PrintTable values (@PrintText)
    SELECT PrintText FROM @PrintTable
END

exec ReporteAtendidos2 '2022-12-15','2023-01-01'