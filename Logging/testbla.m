x = namessep(:,"x");
y = namessep(:,"y");
z = namessep(:,"z");
xarr = table2array(x);
yarr = table2array(y);
zarr = table2array(z);
scatter3(xarr, yarr, zarr)