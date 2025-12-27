% Find the largest rectangle that fits inside a polygon
% with at least two opposite corners on the perimeter

clear all; close all; clc;

% Read the tiles data
filename = 'tiles.txt';
data = readtable(filename, 'FileType', 'text', 'ReadVariableNames', false);

% Extract x and y coordinates
x_poly = table2array(data(:,1));
y_poly = table2array(data(:,2));

% Function to check if a point is inside or on the polygon perimeter
function inside = pointInsidePolygon(px, py, x_poly, y_poly)
    % Ray casting algorithm
    inside = false;
    n = length(x_poly);
    
    for i = 1:n
        x1 = x_poly(i);
        y1 = y_poly(i);
        x2 = x_poly(mod(i, n) + 1);
        y2 = y_poly(mod(i, n) + 1);
        
        % Ensure y1 <= y2
        if y1 > y2
            temp_x = x1; temp_y = y1;
            x1 = x2; y1 = y2;
            x2 = temp_x; y2 = temp_y;
        end
        
        % Check if point is on a horizontal edge
        if (py == y1 || py == y2) && (min(x1, x2) <= px && px <= max(x1, x2))
            inside = true;
            return;
        end
        
        % Check if ray crosses the edge
        if (py > y1) ~= (py > y2)
            intersection_x = (x2 - x1) * (py - y1) / (y2 - y1) + x1;
            if intersection_x >= px
                inside = ~inside;
            end
        end
    end
end

% Find the largest rectangle
n_points = length(x_poly);
biggest_area = 0;
best_rect = [];

% Try all pairs of points
for i = 1:n_points
    for j = i+1:n_points
        % Two opposite corners of the rectangle
        x1 = x_poly(i);
        y1 = y_poly(i);
        x2 = x_poly(j);
        y2 = y_poly(j);
        
        % The other two corners (axis-aligned rectangle)
        x3 = x1;
        y3 = y2;
        x4 = x2;
        y4 = y1;
        
        % Calculate rectangle area
        width = abs(x2 - x1) + 1;
        height = abs(y2 - y1) + 1;
        area = width * height;
        
        % Check if the other two corners are inside or on the polygon
        inside_3 = pointInsidePolygon(x3, y3, x_poly, y_poly);
        inside_4 = pointInsidePolygon(x4, y4, x_poly, y_poly);
        
        if inside_3 && inside_4 && area > biggest_area
            biggest_area = area;
            best_rect = [x1 y1 x2 y2 x3 y3 x4 y4];
        end
    end
end

fprintf('Largest rectangle area: %d\n', biggest_area);

if ~isempty(best_rect)
    x1 = best_rect(1); y1 = best_rect(2);
    x2 = best_rect(3); y2 = best_rect(4);
    x3 = best_rect(5); y3 = best_rect(6);
    x4 = best_rect(7); y4 = best_rect(8);
    
    fprintf('Rectangle corners:\n');
    fprintf('  Corner 1: (%.0f, %.0f)\n', x1, y1);
    fprintf('  Corner 2: (%.0f, %.0f)\n', x2, y2);
    fprintf('  Corner 3: (%.0f, %.0f)\n', x3, y3);
    fprintf('  Corner 4: (%.0f, %.0f)\n', x4, y4);
end

% Create figure
figure('Position', [100, 100, 1200, 900]);

% Plot the polygon
plot(x_poly, y_poly, 'b-', 'LineWidth', 2);
hold on;

% Fill the polygon
fill(x_poly, y_poly, 'cyan', 'FaceAlpha', 0.2, 'EdgeColor', 'blue', 'LineWidth', 2);

% Plot vertices
plot(x_poly, y_poly, 'ro', 'MarkerSize', 4, 'MarkerFaceColor', 'r');

% Plot the best rectangle if found
if ~isempty(best_rect)
    rect_x = [x1 x2 x4 x3 x1];
    rect_y = [y1 y2 y4 y3 y1];
    plot(rect_x, rect_y, 'g-', 'LineWidth', 3, 'DisplayName', sprintf('Best Rectangle (Area: %d)', biggest_area));
    fill(rect_x, rect_y, 'green', 'FaceAlpha', 0.1, 'EdgeColor', 'green', 'LineWidth', 2);
    
    % Mark rectangle corners
    plot([x1 x2 x3 x4], [y1 y2 y3 y4], 'gs', 'MarkerSize', 8, 'MarkerFaceColor', 'g');
end

xlabel('X Coordinate', 'FontSize', 12);
ylabel('Y Coordinate', 'FontSize', 12);
title('Largest Rectangle Inside Polygon', 'FontSize', 14, 'FontWeight', 'bold');
grid on;
legend('Polygon', 'Polygon Fill', 'Vertices', 'Location', 'best');
axis equal;