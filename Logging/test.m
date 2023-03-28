A = {3;2};
A{end +1} = 3;
disp(A);
disp(A{1});
disp(A{1}+A{1});


filename = 'LLD.csv';
% Read the CSV as a table 
t = readtable(filename);
% Add a new column to the end of the table
numOfColumn = size(t, 2);
newCol = num2cell(d1(1:end,7));
% Your new column 
t.(numOfColumn+1) = newCol; 
% Change column name if needed 
t.Properties.VariableNames{numOfColumn+1} = 'newCol'; 
% Write to CSV file 
writetable(t, 'new.csv')