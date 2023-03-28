clear
fid = fopen('LLD.csv', 'w');
T = readtable("GPS_Brücke.csv");
%disp(T)
lat_table = T(:,"Var3");
lon_table = T(:,"Var4");

lat_arr = table2array(lat_table);
lon_arr = table2array(lon_table);

%lat = 20.0;
%lon = 60.0;

real_lat = 53.8630077;
real_lon = 10.7042175;

distance_list = {};
%disp(size(lat_arr))
fprintf(fid, '%f,%f,%f\n', real_lat, real_lon, 0.00001);
distavg = 0;
for i = 1:size(lat_arr)
    lat = lat_arr(i);
    lon = lon_arr(i);
    %lat = 53.85612505525895;
    %lon = 10.606448905595343;
    theta = lon - real_lon;
    

    distance = 60 * 1.1515 * rad2deg(acos((sin(deg2rad(lat)) * sin(deg2rad(real_lat))) + (cos(deg2rad(lat)) * cos(deg2rad(real_lat)) * cos(deg2rad(theta)))));
    distance = distance * 1609.344;
    %distance_list = [distance_list, distance];
    %disp(distance);
    fprintf(fid, '%.10f,%.10f,%.10f\n', lat, lon, distance); 
    distavg = (distavg + distance);
end
disp(distavg);
disp(length(lat_arr));
distavg = distavg ./ length(lat_arr);
disp('distavg');
disp(distavg);

LLD = readtable("LLD.csv");
%disp(LLD);
lat_t = LLD(:,"Var1");
lon_t = LLD(:,"Var2");
dist_table = LLD(:,"Var3");
lat_a = table2array(lat_t);
lon_a = table2array(lon_t);
dist_arr = table2array(dist_table);
%plot(dist_arr);



fclose(fid);
%disp(distance_list{1});
dist_tab = array2table(distance_list);

labels = {'Standort'};
figure
geoscatter(lat_a, lon_a, dist_arr)
hold on
geoscatter(lat_a(1), lon_a(1), 'MarkerFaceColor', 'r', 'MarkerEdgeColor', 'r')
hold off
legend(labels)


%geoscatter(lat_a, lon_a, dist_arr);
%geo.ColorVariable = 'VAR3';
%geo.MarkerFaceColor = "auto";



