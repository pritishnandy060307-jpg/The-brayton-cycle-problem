%% BRAYTON CYCLE PARAMETRIC STUDY
% Varies compressor efficiency, turbine efficiency and combustor
% pressure ratio within the specified limits.

clc;
clear;
close all;

%% GIVEN DATA
T1 = 15 + 273.15;       % Compressor inlet temperature [K]
T3 = 1100 + 273.15;     % Turbine inlet / maximum cycle temperature [K]

P1 = 0.1;               % Compressor inlet pressure [MPa]
P2 = 1.0;               % Compressor outlet pressure [MPa]

gamma = 1.4;

% Compressor pressure ratio
rp_c = P2/P1;

%% PARAMETER RANGES
% All values include the requested endpoints.
eta_c = linspace(0.40, 0.95, 31);   % Compressor efficiency
eta_t = linspace(0.40, 0.95, 31);   % Turbine efficiency
pi_cc = linspace(0.60, 0.99, 31);   % Combustor pressure ratio

%% CREATE 3-D GRID
[EC, ET, PCC] = meshgrid(eta_c, eta_t, pi_cc);

%% ISENTROPIC COMPRESSOR EXIT TEMPERATURE
T2s = T1 * rp_c^((gamma-1)/gamma);

%% CALCULATE CYCLE THERMAL EFFICIENCY
eta_cycle = zeros(size(EC));

for k = 1:length(pi_cc)
    for j = 1:length(eta_t)
        for i = 1:length(eta_c)

            ec  = EC(k,j,i);
            et  = ET(k,j,i);
            pcc = PCC(k,j,i);

            % Actual compressor exit temperature
            T2 = T1 + (T2s - T1)/ec;

            % Pressure after combustor
            P3 = pcc * P2;

            % Turbine expands from P3 to P4 = P1
            turbine_pressure_ratio = P3/P1;

            % Isentropic turbine exit temperature
            T4s = T3 * (1/turbine_pressure_ratio)^((gamma-1)/gamma);

            % Actual turbine exit temperature
            T4 = T3 - et*(T3 - T4s);

            % Specific work terms (cp cancels)
            Wc = T2 - T1;
            Wt = T3 - T4;
            Wnet = Wt - Wc;

            % Heat added (cp cancels)
            Qin = T3 - T2;

            % Thermal efficiency
            eta_cycle(k,j,i) = Wnet/Qin;
        end
    end
end

eta_percent = eta_cycle * 100;

%% VERIFY LIMITS
fprintf('Compressor efficiency: %.2f to %.2f\n', min(eta_c), max(eta_c));
fprintf('Turbine efficiency:    %.2f to %.2f\n', min(eta_t), max(eta_t));
fprintf('Combustor pressure ratio: %.2f to %.2f\n', min(pi_cc), max(pi_cc));
fprintf('Total data points: %d\n', numel(eta_cycle));
fprintf('Minimum cycle efficiency: %.2f %%\n', min(eta_percent(:)));
fprintf('Maximum cycle efficiency: %.2f %%\n', max(eta_percent(:)));

%% 3-D SCATTER PLOT
figure('Color','w');

scatter3(EC(:), ET(:), PCC(:), 12, eta_percent(:), 'filled');

xlabel('\eta_c  (Compressor Efficiency)', ...
    'FontSize', 12, 'FontWeight', 'bold');

ylabel('\eta_t  (Turbine Efficiency)', ...
    'FontSize', 12, 'FontWeight', 'bold');

zlabel('\pi_{cc}  (Combustor Pressure Ratio)', ...
    'FontSize', 12, 'FontWeight', 'bold');

title('Brayton Cycle Efficiency: 3-D Parameter Study', ...
    'FontSize', 14, 'FontWeight', 'bold');

xlim([0.40 0.95]);
ylim([0.40 0.95]);
zlim([0.60 0.99]);

cb = colorbar;
cb.Label.String = 'Thermal Efficiency (%)';
cb.Label.FontSize = 11;

grid on;
box on;
colormap turbo;
view(45,30);
set(gca, 'FontSize', 11, 'LineWidth', 1);

%% SAVE FIGURE
if ~exist('plots','dir')
    mkdir('plots');
end

exportgraphics(gcf, 'plots/3D_parameter_study.png', 'Resolution', 300);
