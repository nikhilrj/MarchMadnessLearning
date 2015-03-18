%% 

M = csvread('output_matlab.csv',1,0);
inp = normc(M(:, 2:end));
out = M(:, 1);
%% 

split = 3500;
train_inp = inp(1:split, :);
train_out = out(1:split, :);

test_inp = inp(split:end, :);
test_out = out(split:end, :);

%% 

LogRes = mnrfit(train_inp, categorical(train_out));
result = test_inp*LogRes(2:end, :) + LogRes(1);
