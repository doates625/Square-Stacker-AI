% Load CSV File
data = csvread('Log.csv');
game = data(:,1);
game_score = data(:,2);

% Windowed Statistics
win_len = 1000;
mean_score = zeros(size(game));
min_score = zeros(size(game));
max_score = zeros(size(game));
for g = 1:length(game)
    win = game_score(max(1, g - win_len + 1):g);
    mean_score(g) = mean(win);
    min_score(g) = min(win);
    max_score(g) = max(win);
end

% Plot Data
figure(1), clf

% Game Scores
subplot(2, 1, 1)
hold on, grid on
title('Game Scores')
xlabel('Game')
ylabel('Score')
plot(game, game_score, 'r-')

% Statistics Score
subplot(2, 1, 2)
hold on, grid on
title('Score Statistics')
xlabel('Game')
ylabel('Score')
plot(game, max_score, 'g-')
plot(game, mean_score, 'b-')
plot(game, min_score, 'r-')
legend('Max', 'Mean', 'Min')