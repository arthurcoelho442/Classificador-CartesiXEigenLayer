%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                        PROGRAMA DE OTIMIZAÁ√O 
%                                                       Autores: Helder Rocha
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear
clc
tic;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%% Leitura de Dados%%%%%%%%%%%%%%%%%%%%%%%
L0=load('L0.csv');
L1=load('L1.csv');
L2=load('L2.csv');
L3=load('L3.csv');
L4=load('L4.csv');
L5=load('L5.csv');
L6=load('L6.csv');
L7=load('L7.csv');
L8=load('L8.csv');
L9=load('L9.csv');
L10=load('L10.csv');
L11=load('L11.csv');
L12=load('L12.csv');
L13=load('L13.csv');
L14=load('L14.csv');
L15=load('L15.csv');

figure 
plot(L0(1:1666,2))
title('Current Signal')
ylabel('Current Amplitude')
xlabel('time(ms)')
axis([0 1666 -10 10])
hold on
plot(L1(1:1666,2))
hold on
plot(L2(1:1666,2))
hold on
plot(L3(1:1666,2))
hold on
plot(L4(1:1666,2))
hold on
plot(L5(1:1666,2))
hold on
plot(L6(1:1666,2))
hold on
plot(L7(1:1666,2))
hold on
plot(L8(1:1666,2))
hold on
plot(L9(1:1666,2))
hold on
plot(L10(1:1666,2))
hold on
plot(L11(1:1666,2))
hold on
plot(L12(1:1666,2))
hold on
plot(L13(1:1666,2))
hold on
plot(L14(1:1666,2))
hold on
plot(L15(1:1666,2))
hold off
legend('Classe 1','Classe 2','Classe 3','Classe 4','Classe 5','Classe 6','Classe 7','Classe 8','Classe 9','Classe 10','Classe 11','Classe 12','Classe 13','Classe 14','Classe 15','Classe 16','Location','eastoutside')



 EntSaida = [L0];
%             Dados_L1
%             Dados_L2
%             Dados_L3
%             Dados_L4
%             Dados_L12
%             Dados_L13
%             Dados_L14
%             Dados_L23
%             Dados_L24
%             Dados_L34
%             Dados_L123
%             Dados_L124
%             Dados_L134
%             Dados_L234
%             Dados_L1234];
