clear;
close all;
clc;
raw = readtable('data1.csv');
raw = table2array(raw(:,[2,4]));

avg = zeros(20,1);
wel = raw(:,2);
for i = 1:20
    avg(i) = mean(wel(-99+100*i:100*i));
end
avg = avg';

fail_count = zeros(20,1);
for i = 1:20
    fail_count(i) = sum(wel(-99+100*i:100*i) <0);
end

x = 5:5:100;
figure(1)
scatter(x,avg,'r')
xlabel('initial hunter')
ylabel('average welfare')
title('policy for initial hunter (based on avg-wel)')

to_wel = x.*avg;
figure(2)
scatter(x,to_wel,'p')
xlabel('initial hunter')
ylabel('total welfare')
title('policy for initial hunter (based on total welfare)')

figure(3)
scatter(x,fail_count,'bl')
xlabel('initial hunter')
ylabel('fail count')
title('policy for initial hunter (based on whether overhunting)')

wel1 = [];
for i = 1:20
    wel1 = [wel1 wel(-99+100*i:i*100)];
end
figure(4)
for j = 1:20
    for i = 1:100
    scatter(j*5,wel1(i,j))
    hold on
    end
end
hold off
title('whole avg-wel result distribution')
xlabel('initial hunter')
ylabel('average welfare')



