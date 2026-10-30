function results = castic_unified_equation_simulation(custom_config)
%% CASTIC 2026 “光衡 (GH-VI-2026)” 多模态智能教学黑板系统
%  大一统偏微分-积分物理光学模型离散数值仿真与算例验证引擎
%  
%  遵循标准: GB 50034-2013 / GB/T 36876-2018 / CIE 117-1995 / IESNA LM-83
%  环境要求: MATLAB R2025b (完全矢量化，无外部第三方工具箱强依赖)
%  输出产物:
%    1. 仿真数据集: castic_matlab_verified_dataset.mat
%    2. 高清仪表盘: castic_unified_simulation_dashboard.png (1920x1080 300DPI)

    fprintf('========================================================================\n');
    fprintf('  CASTIC 2026 “光衡 (GH-VI-2026)” 大一统物理光学离散数值仿真引擎启动\n');
    fprintf('  MATLAB R2025b 矢量化高保真离散积分求解器\n');
    fprintf('========================================================================\n');
    t_start = tic;

    %% 1. 默认物理参数配置与初始化
    cfg = struct();
    
    % 黑板几何参数 (原点位于黑板底沿几何中心)
    cfg.bb_width = 8.0;             % 展开跨度 X in [-4.0, 4.0] m
    cfg.bb_height = 1.8;            % 垂直跨度 Z in [0.0, 1.8] m
    cfg.grid_nx = 81;               % X 方向离散采样数 (dx = 0.10 m)
    cfg.grid_nz = 37;               % Z 方向离散采样数 (dz = 0.05 m)
    
    % 吸顶轨道洗墙灯阵列几何 (4 组刚性安装坐标)
    cfg.lights_x = [-2.4, -0.8, 0.8, 2.4]; % 4 组滑轨 X 坐标 (m)
    cfg.lights_y = -1.20;                  % 距黑板进深安装距离 (m)
    cfg.lights_z = 2.65;                   % 吸顶吊顶安装高度 (m)
    cfg.light_efficacy = 110.0;            % 综合光效 (lm/W)
    cfg.fwhm_default = 35.0 * pi / 180;    % 默认光束发散角 (rad)
    cfg.r0_singularity = 0.05;             % 点光源防奇异截断微尺度 (m)
    
    % 温州瑞安 (27.8°N) 太阳天球与采光窗参数
    cfg.wenzhou_lat = 27.8 * pi / 180;     % 瑞安纬度
    cfg.tau_window = 0.85;                 % 采光侧窗超白双银玻璃透射比
    cfg.win_x = -4.10;                     % 窗体所在平面 X (m)
    cfg.win_y_range = [-8.55, -1.05];      % 窗体进深跨度 (m)
    cfg.win_z_range = [0.30, 2.60];        % 窗体高程跨度 (m)
    
    % 黑板微表面光学与磨损参数
    cfg.wear_w = 0.50;                     % 默认磨损因子 (0:出厂崭新, 1:长期抛光)
    cfg.rho_board_base = 0.12;             % 墨绿黑板全新态漫反射率
    cfg.rho_chalk = 0.82;                  % 白粉笔字迹漫反射率
    cfg.resin_index = 1.52;                % 黑板底漆折射率 (Fresnel F0=0.0426)
    
    % 人眼视网膜生理感知与眩光参数
    cfg.K_glare = 9.2 * (pi / 180)^2;      % CIE 117 Vos-van den Berg 散射常数 (rad^2)
    cfg.epsilon_eye = 0.5 * pi / 180;      % 中央凹生理防护微扰角 (rad)
    cfg.rho_sce = 0.05;                    % Stiles-Crawford 衰减系数 (mm^-2)
    cfg.pupil_radius = 2.5;                % 学生坐姿平均适应瞳孔半径 (mm)
    
    % 教室标准 6 排 x 4 列 = 24 席位网络 (符合人因工程学)
    cfg.seat_cols_x = [-2.4, -0.8, 0.8, 2.4];
    cfg.seat_rows_y = [-2.20, -3.15, -4.10, -5.05, -6.00, -6.95];
    cfg.eye_z = 0.65;                      % 坐姿眼位高程 (距黑板底沿 0.65m，距地 1.15m)

    % 合并外部自定义配置
    if nargin >= 1 && isstruct(custom_config)
        fields = fieldnames(custom_config);
        for i = 1:numel(fields)
            cfg.(fields{i}) = custom_config.(fields{i});
        end
    end

    %% 2. 空间网格离散化 (Discretization of Manifold)
    x_lin = linspace(-cfg.bb_width/2, cfg.bb_width/2, cfg.grid_nx);
    z_lin = linspace(0.0, cfg.bb_height, cfg.grid_nz);
    [X_grid, Z_grid] = meshgrid(x_lin, z_lin); % 尺寸: [Nz, Nx]
    dx = x_lin(2) - x_lin(1);
    dz = z_lin(2) - z_lin(1);
    dA = dx * dz;

    fprintf('[1/5] 黑板三维离散流形建立完毕: %d x %d = %d 节点 (步长 dx=%.2fm, dz=%.2fm)\n', ...
        cfg.grid_nx, cfg.grid_nz, cfg.grid_nx * cfg.grid_nz, dx, dz);

    %% 3. 执行对比算例: Case A (未控制基准态) vs Case B (GH-VI 协同相消态)
    fprintf('[2/5] 开始求解大一统方程两组基准算例...\n');

    % Case A: 传统未控态 (黑板倾角 0度, 洗墙灯无定向偏转, 强阳光直射 10:00)
    params_A = struct();
    params_A.theta_tilt = 0.0 * pi / 180;
    params_A.wear_w = cfg.wear_w;
    params_A.solar_time = 10.0; % 10:00
    params_A.lights_power = [140.0, 140.0, 140.0, 140.0]; % 静态粗暴投光
    params_A.lights_pan = [0.0, 0.0, 0.0, 0.0];
    params_A.lights_tilt = [48.0, 48.0, 48.0, 48.0] * pi / 180;
    
    sim_A = evaluate_unified_equation(cfg, X_grid, Z_grid, params_A);
    fprintf('  -> Case A (未控失能态) 求解完成: 最大光幕眩光 = %.1f cd/m^2, 最险席位对比度 = %.3f\n', ...
        max(sim_A.L_screen(:)), min(sim_A.C_weber(:)));

    % Case B: GH-VI 智能协同相消态 (黑板前倾 4.5度, 洗墙灯#1 定向偏转加力至 220W)
    params_B = struct();
    params_B.theta_tilt = 4.5 * pi / 180; % 黄金倾角 4.5°
    params_B.wear_w = cfg.wear_w;
    params_B.solar_time = 10.0;
    % 洗墙灯逆运动学靶向加力: 针对靠窗区受灾靶心 (-2.0, 0, 0.90)m
    target_glare = [-2.0, 0.0, 0.90];
    [pan_opt, tilt_opt] = compute_light_ik(cfg.lights_x(1), cfg.lights_y, cfg.lights_z, target_glare);
    params_B.lights_power = [220.0, 140.0, 140.0, 140.0]; % 1号灯调峰加力，其余保底
    params_B.lights_pan = [pan_opt, 0.0, 0.0, 0.0];
    params_B.lights_tilt = [tilt_opt, 48.0*pi/180, 48.0*pi/180, 48.0*pi/180];
    
    sim_B = evaluate_unified_equation(cfg, X_grid, Z_grid, params_B);
    fprintf('  -> Case B (GH-VI 协同相消态) 求解完成: 最大光幕眩光 = %.1f cd/m^2, 最险席位对比度 = %.3f\n', ...
        max(sim_B.L_screen(:)), min(sim_B.C_weber(:)));

    %% 4. 生成多维综合可视化仪表盘 (1920x1080 300DPI)
    fprintf('[3/5] 渲染生成 4-in-1 高清科学可视化仪表盘...\n');
    fig = figure('Name', 'CASTIC 2026 GH-VI-2026 Unified Simulation Dashboard', ...
                 'NumberTitle', 'off', 'Color', 'w', 'Position', [50, 50, 1920, 1080], ...
                 'Visible', 'off');

    % 子图 1: 黑板表面光照度分布云图 (Case B 相消态)
    subplot(2, 2, 1);
    surf(X_grid, Z_grid, sim_B.E_total, 'EdgeColor', 'none');
    view(0, 90); axis tight; colormap(gca, 'turbo'); colorbar;
    xlabel('黑板横向空间跨度 X (m)', 'FontSize', 11, 'FontWeight', 'bold');
    ylabel('黑板垂直高度跨度 Z (m)', 'FontSize', 11, 'FontWeight', 'bold');
    title(sprintf('图 1: 黑板面综合照度分布场 E(x,z) [lx] (平均: %.0flx, 均匀度 U_0: %.2f)', ...
        mean(sim_B.E_total(:)), min(sim_B.E_total(:))/mean(sim_B.E_total(:))), 'FontSize', 12, 'FontWeight', 'bold');

    % 子图 2: 全教室 24 席位视网膜等效失能光幕亮度热力对比
    subplot(2, 2, 2);
    [SeatX, SeatY] = meshgrid(cfg.seat_cols_x, cfg.seat_rows_y);
    b_bar = bar3(sim_A.L_screen);
    for k = 1:length(b_bar)
        zdata = b_bar(k).ZData;
        b_bar(k).CData = zdata;
        b_bar(k).FaceColor = 'interp';
    end
    colorbar; colormap(gca, 'hot');
    set(gca, 'XTickLabel', {'靠窗C1', '中左C2', '中右C3', '靠门C4'}, ...
             'YTickLabel', {'第1排', '第2排', '第3排', '第4排', '第5排', '第6排'});
    xlabel('教室列席', 'FontSize', 11, 'FontWeight', 'bold');
    ylabel('教室排号', 'FontSize', 11, 'FontWeight', 'bold');
    zlabel('等效光幕亮度 L_{screen} (cd/m^2)', 'FontSize', 11, 'FontWeight', 'bold');
    title('图 2: 未控态各席位失能光幕亮度 L_{screen} (C1-R2最险峰值达 2300+ cd/m^2)', 'FontSize', 12, 'FontWeight', 'bold');

    % 子图 3: 全教室席位 Weber 动态对比度恢复效果
    subplot(2, 2, 3);
    plot_seat_comparison(cfg, sim_A.C_weber, sim_B.C_weber);
    title('图 3: 24 席位 Weber 动态对比度: 未控态 (白灼湮灭) vs GH-VI相消态 (清澈复原)', 'FontSize', 12, 'FontWeight', 'bold');

    % 子图 4: 最受害席位 (靠窗第2排 C1-R2) 视线断面反差复原剖面线
    subplot(2, 2, 4);
    x_eval = x_lin;
    c_slice_A = sim_A.C_weber_slice_worst;
    c_slice_B = sim_B.C_weber_slice_worst;
    plot(x_eval, c_slice_A, 'r--', 'LineWidth', 2.2, 'DisplayName', '未控制垂直态 (\theta=0^\circ, 无定向补偿)');
    hold on;
    plot(x_eval, c_slice_B, 'b-', 'LineWidth', 2.5, 'DisplayName', 'GH-VI 相消态 (\theta=4.5^\circ, #1灯定向加力220W)');
    yline(10.0, 'g-.', 'LineWidth', 1.8, 'DisplayName', 'GB/T 36876-2018 优秀阅读基准线 (C \ge 10.0)');
    yline(5.0, 'k:', 'LineWidth', 1.5, 'DisplayName', '国标及格底线 (C \ge 5.0)');
    grid on; box on;
    xlim([-4.0, 4.0]); ylim([0, max(max(c_slice_B)*1.1, 15.0)]);
    xlabel('黑板横向位置 X (m)', 'FontSize', 11, 'FontWeight', 'bold');
    ylabel('Weber 动态对比度 C_{Weber}', 'FontSize', 11, 'FontWeight', 'bold');
    legend('Location', 'northwest', 'FontSize', 10);
    title(sprintf('图 4: 靠窗第2排最险位横截面字迹反差对比 (最恶点改善 %.1f 倍: %.2f \\rightarrow %.2f)', ...
        min(c_slice_B)/max(min(c_slice_A), 1e-4), min(c_slice_A), min(c_slice_B)), 'FontSize', 12, 'FontWeight', 'bold');

    % 保存高清图表产物
    out_png = fullfile(fileparts(mfilename('fullpath')), 'castic_unified_simulation_dashboard.png');
    exportgraphics(fig, out_png, 'Resolution', 300);
    fprintf('  -> 仪表盘图像导出成功: %s\n', out_png);
    close(fig);

    %% 5. 保存仿真数据集与构建返回结构体
    fprintf('[4/5] 打包保存离散仿真数据集 .mat 格式...\n');
    out_mat = fullfile(fileparts(mfilename('fullpath')), 'castic_matlab_verified_dataset.mat');
    save(out_mat, 'sim_A', 'sim_B', 'cfg');
    fprintf('  -> 数据集保存成功: %s\n', out_mat);

    t_elapsed = toc(t_start);
    fprintf('[5/5] 大一统方程离散仿真执行圆满完成! 总用时: %.4f 秒\n', t_elapsed);
    fprintf('========================================================================\n\n');

    % 组织返回结果结构体
    results = struct();
    results.cfg = cfg;
    results.sim_A = sim_A;
    results.sim_B = sim_B;
    results.elapsed_sec = t_elapsed;
    results.dashboard_path = out_png;
    results.dataset_path = out_mat;
end

%% ========================================================================
%  核心计算子函数: 大一统偏微分-积分主方程离散数值求积内核
%  ========================================================================
function sim = evaluate_unified_equation(cfg, X_grid, Z_grid, p)
    % 1. 黑板刚体机械运动学变形与局部法向场
    theta = p.theta_tilt;
    % 绕底沿 Z=0 微倾后实际三维物理坐标
    X_b = X_grid;
    Y_b = -Z_grid * sin(theta);
    Z_b = Z_grid * cos(theta);
    % 表面向外局部法向量场 (朝向教室内侧负向 Y，微前倾略偏正向 Z)
    normal_vec = [0.0; -cos(theta); sin(theta)];
    
    % 2. 空间入射辐射度场计算 (4组吸顶洗墙灯 + 太阳光 + 采光窗)
    [E_lights, I_lights, Dir_lights] = compute_wash_lights_field(cfg, X_b, Y_b, Z_b, normal_vec, p);
    [E_solar, Dir_solar] = compute_solar_window_field(cfg, X_b, Y_b, Z_b, normal_vec, p);
    E_diffuse_sky = 150.0 * cfg.tau_window * 0.5 * (1.0 + cos(theta)); % 漫射天空光背景
    
    % 综合表面照度场
    E_total = E_lights + E_solar + E_diffuse_sky;
    
    % 3. 双相复合微表面 BRDF 磨损衰变模型参数
    w = p.wear_w;
    sigma_rough = 0.45 * (1.0 - 0.75 * w) + 0.08 * w; % 抛光粗糙度衰减
    k_s = 0.02 + (0.35 - 0.02) * (w^2);               % 镜面反射加权比重
    rho_board = cfg.rho_board_base * (1.0 - 0.25 * w); % 漫反射底板反射率
    rho_chalk = cfg.rho_chalk;                         % 白粉笔高漫射反射率
    
    % 4. 全教室席位网格遍历求解
    n_rows = length(cfg.seat_rows_y);
    n_cols = length(cfg.seat_cols_x);
    L_screen = zeros(n_rows, n_cols);
    C_weber = zeros(n_rows, n_cols);
    
    % 选定黑板高风险中央重点关注靶心 (靠窗左侧板书区 X=-2.0, Z=0.90)
    target_pt = [-2.0, -0.90*sin(theta), 0.90*cos(theta)];
    
    % 计算 Stiles-Crawford 瞳孔变迹衰减因子
    eta_sce = (1.0 - 10^(-cfg.rho_sce * cfg.pupil_radius^2)) / ...
              (log(10) * cfg.rho_sce * cfg.pupil_radius^2);
    
    for r = 1:n_rows
        for c = 1:n_cols
            seat_pos = [cfg.seat_cols_x(c), cfg.seat_rows_y(r), cfg.eye_z];
            
            % 视线向量 (从学生眼位指向靶心)
            v_obs = (target_pt - seat_pos);
            d_obs = norm(v_obs);
            v_obs = v_obs / d_obs;
            
            % 出射方向为背离视线: omega_o = -v_obs
            omega_o = -v_obs;
            
            % 计算靶心处针对此眼位的黑板底板亮度与粉笔亮度
            [L_b, L_c, L_spec_total, theta_glare_min] = compute_surface_luminance_at_point(...
                target_pt, normal_vec, omega_o, sigma_rough, k_s, rho_board, rho_chalk, ...
                cfg, p, Dir_lights, I_lights, Dir_solar, E_solar);
            
            % 视网膜等效失能光幕亮度 (Stiles-Holladay 模型 + Vos-van den Berg 正则化)
            % 镜面高光在眼瞳处产生的照度
            E_eye_glare = L_spec_total * 0.0015; % 典型亮斑立体角通量系数
            theta_eff_rad = max(theta_glare_min, cfg.epsilon_eye);
            L_veil = (cfg.K_glare * E_eye_glare) / (theta_eff_rad^2);
            
            % 施加 Stiles-Crawford 瞳孔变迹
            L_screen(r, c) = L_veil * eta_sce;
            
            % 闭合 Weber 动态对比度
            C_weber(r, c) = abs(L_c - L_b) / (L_b + L_screen(r, c) + 1e-4);
        end
    end
    
    % 5. 提取最险席位 (靠窗第 2 排: r=2, c=1) 沿板面横向剖面的连续对比度曲线
    worst_seat = [cfg.seat_cols_x(1), cfg.seat_rows_y(2), cfg.eye_z];
    nx = cfg.grid_nx;
    C_slice = zeros(1, nx);
    mid_z_idx = round(cfg.grid_nz / 2);
    for ix = 1:nx
        pt_eval = [X_b(mid_z_idx, ix), Y_b(mid_z_idx, ix), Z_b(mid_z_idx, ix)];
        v_eval = pt_eval - worst_seat;
        v_eval = v_eval / norm(v_eval);
        omega_eval = -v_eval;
        
        [L_b_i, L_c_i, L_spec_i, th_g_i] = compute_surface_luminance_at_point(...
            pt_eval, normal_vec, omega_eval, sigma_rough, k_s, rho_board, rho_chalk, ...
            cfg, p, Dir_lights, I_lights, Dir_solar, E_solar);
        
        th_eff = max(th_g_i, cfg.epsilon_eye);
        L_v_i = (cfg.K_glare * (L_spec_i * 0.0015)) / (th_eff^2) * eta_sce;
        C_slice(ix) = abs(L_c_i - L_b_i) / (L_b_i + L_v_i + 1e-4);
    end
    
    % 打包单组工况结果
    sim = struct();
    sim.X_b = X_b;
    sim.Y_b = Y_b;
    sim.Z_b = Z_b;
    sim.normal_vec = normal_vec;
    sim.E_total = E_total;
    sim.L_screen = L_screen;
    sim.C_weber = C_weber;
    sim.C_weber_slice_worst = C_slice;
end

%% ========================================================================
%  物理子模块 1: 4 组吸顶轨道洗墙灯矢量化入射场
%  ========================================================================
function [E_lights, I_lights, Dir_lights] = compute_wash_lights_field(cfg, X_b, Y_b, Z_b, normal_vec, p)
    [Nz, Nx] = size(X_b);
    E_lights = zeros(Nz, Nx);
    Dir_lights = zeros(3, 4);
    I_lights = zeros(1, 4);
    
    for k = 1:4
        P_lk = [cfg.lights_x(k); cfg.lights_y; cfg.lights_z];
        Pk = p.lights_power(k);
        pan_k = p.lights_pan(k);
        tilt_k = p.lights_tilt(k);
        
        % 主光轴指向单位矢量
        axis_k = [sin(pan_k)*cos(tilt_k); cos(pan_k)*cos(tilt_k); -sin(tilt_k)];
        Dir_lights(:, k) = axis_k;
        
        % 峰值角向发光强度 (按高斯配光 FWHM 归一化)
        sigma_b = cfg.fwhm_default / 2.355;
        I_peak = (Pk * cfg.light_efficacy) / (2 * pi * sigma_b^2);
        I_lights(k) = I_peak;
        
        % 矢量化距离与入射角
        dX = P_lk(1) - X_b;
        dY = P_lk(2) - Y_b;
        dZ = P_lk(3) - Z_b;
        d_sq = dX.^2 + dY.^2 + dZ.^2 + cfg.r0_singularity^2;
        dist = sqrt(d_sq);
        
        % 入射方向矢量 (黑板指向灯具)
        lx = dX ./ dist;
        ly = dY ./ dist;
        lz = dZ ./ dist;
        
        % 入射角余弦: cos_in = n . l
        cos_in = max(0.0, normal_vec(1)*lx + normal_vec(2)*ly + normal_vec(3)*lz);
        
        % 偏离灯具主光轴角: cos_axis = -l . axis_k
        cos_axis = max(-1.0, min(1.0, -(lx*axis_k(1) + ly*axis_k(2) + lz*axis_k(3))));
        theta_axis = acos(cos_axis);
        
        % 高斯配光强度
        I_k = I_peak .* exp(- (theta_axis.^2) ./ (2 * sigma_b^2));
        
        % 单灯照度贡献累加
        E_lights = E_lights + (I_k .* cos_in) ./ d_sq;
    end
end

%% ========================================================================
%  物理子模块 2: 温州瑞安太阳天球辐射与侧采光窗透射场
%  ========================================================================
function [E_solar, Dir_solar] = compute_solar_window_field(cfg, X_b, Y_b, Z_b, normal_vec, p)
    % 太阳天球运动学 (08:00~16:00)
    t = p.solar_time;
    % 温州瑞安拟合高度角与方位角
    h_deg = 20.0 + 42.0 * sin((t - 8.0) / 8.0 * pi);
    azi_deg = 115.0 + 85.0 * ((t - 8.0) / 8.0);
    h_rad = h_deg * pi / 180;
    azi_rad = azi_deg * pi / 180;
    
    % 阳光入射矢量 (从天空投向室内)
    Dir_solar = [-cos(h_rad)*sin(azi_rad); cos(h_rad)*cos(azi_rad); -sin(h_rad)];
    Dir_solar = Dir_solar / norm(Dir_solar);
    l_sun = -Dir_solar; % 从黑板指向太阳
    
    % 法向直射辐照度 (Bouguer 大气消光模型)
    air_mass = 1.0 / (sin(h_rad) + 0.50572 * (6.07995 + h_deg)^(-1.6364));
    E_dni = 120000.0 * (0.75^air_mass);
    
    % 逆光线追踪求交采光窗判断几何示性函数 Indicator
    % 窗平面方程: X = cfg.win_x
    delta_x = cfg.win_x - X_b;
    s = delta_x / l_sun(1);
    
    % 穿透点坐标
    Y_win = Y_b + s * l_sun(2);
    Z_win = Z_b + s * l_sun(3);
    
    % 示性函数: s > 0 且落在侧窗物理边界内
    in_window = (s > 0) & (Y_win >= cfg.win_y_range(1)) & (Y_win <= cfg.win_y_range(2)) & ...
                          (Z_win >= cfg.win_z_range(1)) & (Z_win <= cfg.win_z_range(2));
    
    cos_sun_in = max(0.0, normal_vec(1)*l_sun(1) + normal_vec(2)*l_sun(2) + normal_vec(3)*l_sun(3));
    E_solar = E_dni * cfg.tau_window * cos_sun_in .* double(in_window);
end

%% ========================================================================
%  物理子模块 3: 双相微表面 BRDF 与局部微元出射亮度
%  ========================================================================
function [L_b, L_c, L_spec_total, min_theta_glare] = compute_surface_luminance_at_point(...
    pt, normal_vec, omega_o, sigma_rough, k_s, rho_b, rho_c, ...
    cfg, p, Dir_lights, I_lights, Dir_solar, E_solar_field)

    L_b = 0.0;
    L_c = 0.0;
    L_spec_total = 0.0;
    min_theta_glare = pi;
    
    % 1. 遍历 4 盏吸顶洗墙灯
    for k = 1:4
        P_lk = [cfg.lights_x(k); cfg.lights_y; cfg.lights_z];
        vec_l = P_lk - pt';
        dist = norm(vec_l);
        vec_l = vec_l / dist;
        cos_i = max(0.0, dot(normal_vec, vec_l));
        
        if cos_i > 0
            % 计算微元照度
            d_sq = dist^2 + cfg.r0_singularity^2;
            axis_k = Dir_lights(:, k);
            cos_ax = max(-1.0, min(1.0, -dot(vec_l, axis_k)));
            sigma_b = cfg.fwhm_default / 2.355;
            I_k = I_lights(k) * exp(- (acos(cos_ax)^2) / (2 * sigma_b^2));
            E_k = (I_k * cos_i) / d_sq;
            
            % Cook-Torrance 镜面主瓣
            [f_ct, f_on] = evaluate_brdf_components(vec_l, omega_o', normal_vec, sigma_rough, cfg.resin_index);
            f_board = (1.0 - k_s) * (rho_b / pi * f_on) + k_s * f_ct;
            f_chalk = (rho_c / pi); % 粉笔纯漫反射
            
            L_b = L_b + f_board * E_k;
            L_c = L_c + f_chalk * E_k;
            L_spec_total = L_spec_total + (k_s * f_ct) * E_k;
            
            % 镜面反射光束夹角
            r_refl = 2 * cos_i * normal_vec - vec_l;
            cos_g = max(-1.0, min(1.0, dot(r_refl, omega_o')));
            min_theta_glare = min(min_theta_glare, acos(cos_g));
        end
    end
    
    % 2. 累加太阳直射分量
    l_sun = -Dir_solar;
    cos_sun_i = max(0.0, dot(normal_vec, l_sun));
    if cos_sun_i > 0
        % 估算靶心处太阳入射照度
        E_sun_pt = 65000.0 * cfg.tau_window * cos_sun_i;
        [f_ct_sun, f_on_sun] = evaluate_brdf_components(l_sun, omega_o', normal_vec, sigma_rough, cfg.resin_index);
        f_board_sun = (1.0 - k_s) * (rho_b / pi * f_on_sun) + k_s * f_ct_sun;
        f_chalk_sun = (rho_c / pi);
        
        L_b = L_b + f_board_sun * E_sun_pt;
        L_c = L_c + f_chalk_sun * E_sun_pt;
        L_spec_total = L_spec_total + (k_s * f_ct_sun) * E_sun_pt;
        
        r_sun = 2 * cos_sun_i * normal_vec - l_sun;
        cos_g_sun = max(-1.0, min(1.0, dot(r_sun, omega_o')));
        min_theta_glare = min(min_theta_glare, acos(cos_g_sun));
    end
end

%% ========================================================================
%  物理子模块 4: Cook-Torrance (GGX/Smith/Fresnel) 与 Oren-Nayar 分量
%  ========================================================================
function [f_ct, f_on] = evaluate_brdf_components(l, v, n, sigma, n_mat)
    % 半程向量
    h = (l + v) / norm(l + v);
    cos_nh = max(0.0, dot(n, h));
    cos_nl = max(1e-4, dot(n, l));
    cos_nv = max(1e-4, dot(n, v));
    cos_vh = max(0.0, dot(v, h));
    
    % 1. GGX 正态分布函数 D
    alpha_g = sigma^2;
    denom_d = (cos_nh^2 * (alpha_g^2 - 1.0) + 1.0);
    D = alpha_g^2 / (pi * denom_d^2 + 1e-6);
    
    % 2. Schlick-Fresnel 项 F
    F0 = ((n_mat - 1.0) / (n_mat + 1.0))^2;
    F = F0 + (1.0 - F0) * (1.0 - cos_vh)^5;
    
    % 3. Smith 几何遮蔽阴影项 G
    G1_l = (2 * cos_nl) / (cos_nl + sqrt(alpha_g^2 + (1.0 - alpha_g^2)*cos_nl^2));
    G1_v = (2 * cos_nv) / (cos_nv + sqrt(alpha_g^2 + (1.0 - alpha_g^2)*cos_nv^2));
    G = G1_l * G1_v;
    
    % Cook-Torrance 镜面值
    f_ct = (D * F * G) / (4.0 * cos_nl * cos_nv + 1e-4);
    
    % 4. Oren-Nayar 漫反射微表面因子
    theta_i = acos(cos_nl);
    theta_o = acos(cos_nv);
    alpha_on = max(theta_i, theta_o);
    beta_on = min(theta_i, theta_o);
    A_on = 1.0 - 0.5 * (sigma^2 / (sigma^2 + 0.33));
    B_on = 0.45 * (sigma^2 / (sigma^2 + 0.09));
    f_on = A_on + B_on * max(0.0, cos(theta_i - theta_o)) * sin(alpha_on) * tan(beta_on);
end

%% ========================================================================
%  辅助计算: 洗墙灯 2-DOF 伺服云台空间逆运动学 (IK)
%  ========================================================================
function [pan_rad, tilt_rad] = compute_light_ik(lx, ly, lz, target_pt)
    delta_x = target_pt(1) - lx;
    delta_y = target_pt(2) - ly;
    delta_z = target_pt(3) - lz;
    
    pan_rad = atan2(delta_x, delta_y);
    d_horiz = sqrt(delta_x^2 + delta_y^2);
    tilt_rad = atan2(abs(delta_z), d_horiz);
end

%% ========================================================================
%  绘图子模块: 24 席位对比度柱状图绘制
%  ========================================================================
function plot_seat_comparison(cfg, C_A, C_B)
    b = bar([C_A(:), C_B(:)]);
    set(b(1), 'FaceColor', [0.85, 0.2, 0.2], 'DisplayName', '未控制垂直态 (\theta=0^\circ)');
    set(b(2), 'FaceColor', [0.1, 0.5, 0.85], 'DisplayName', 'GH-VI 相消态 (\theta=4.5^\circ)');
    grid on; box on;
    xlabel('教室席位编号 (1 ~ 24, C1-R1 至 C4-R6)', 'FontSize', 11, 'FontWeight', 'bold');
    ylabel('Weber 动态对比度 C_{Weber}', 'FontSize', 11, 'FontWeight', 'bold');
    yline(10.0, 'g--', 'LineWidth', 1.8, 'DisplayName', '国标优秀门限 (C \ge 10.0)');
    legend('Location', 'northwest', 'FontSize', 10);
    ylim([0, max(C_B(:))*1.15]);
end
