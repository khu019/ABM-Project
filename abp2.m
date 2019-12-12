clear;
clc;
raw = readtable('data2.csv');
hunt_season = table2array(raw(:,3));
init_hunt = table2array(raw(:,2));
avg_wel = table2array(raw(:,5));
raw1 = [init_hunt hunt_season avg_wel];
data1 = raw1(1:100,:);
data2 = raw1(101:200,:);
data3 = raw1(201:300,:);
data4 = raw1(301:400,:);
data5 = raw1(401:500,:);
% for init_hunt = 5
x = 1:10;
data1_avg = [];
for i = 1 : 10
    trans = mean(data1(-9+10*i:10*i,:),1);
    data1_avg = [data1_avg trans(3)];
end

data2_avg = [];
for i = 1 : 10
    trans = mean(data2(-9+10*i:10*i,:),1);
    data2_avg = [data2_avg trans(3)];
end
data3_avg = [];
for i = 1 : 10
    trans = mean(data3(-9+10*i:10*i,:),1);
    data3_avg = [data3_avg trans(3)];
end
data4_avg = [];
for i = 1 : 10
    trans = mean(data4(-9+10*i:10*i,:),1);
    data4_avg = [data4_avg trans(3)];
end
data5_avg = [];
for i = 1 : 10
    trans = mean(data5(-9+10*i:10*i,:),1);
    data5_avg = [data5_avg trans(3)];
end
avg_result = [data1_avg;data2_avg;data3_avg;data4_avg;data5_avg];
figure(1)
for i = 1 : 5
scatter(x,avg_result(i,:))
hold on
end
xlabel('hunting season end')
ylabel('average welfare')
title('best policy based on average welfare')
legend('hunt =5','hunter = 10','hunter = 15','hunter = 20','hunter = 25','location','southwest')
hold off

% what about total welfare
total_result = [data1_avg*5;data2_avg*10;data3_avg*15;data4_avg*20;data5_avg*25];
figure(2)
for i = 1 : 5
scatter(x,total_result(i,:))
hold on
end
xlabel('hunting season end')
ylabel('total welfare')
title('best policy based on total welfare')
legend('hunt =5','hunter = 10','hunter = 15','hunter = 20','hunter = 25','location','southwest')
hold off

