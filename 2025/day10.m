fid = fopen(fullfile(fileparts(mfilename('fullpath')), 'factory.txt'), 'r');
content = fscanf(fid, '%c');
fclose(fid);

lines = strsplit(strtrim(content), newline);
overall_total=0;

for i = 1:length(lines)
    line = lines{i};
    parts = strsplit(line);
    
    % Parse objective sums from last part
    objective_str = parts{end};
    objective_str = objective_str(2:end-1); % remove parentheses
    objective_sums = str2num(objective_str);
    
    buttons = parts(2:end-1);
    
    % Convert buttons into vectors
    button_vectors = [];
    for j = 1:length(buttons)
        button = buttons{j};
        button = button(2:end-1); % remove parentheses
        indices = str2num(button);
        
        vector = zeros(1, length(objective_sums));
        for idx = indices
            vector(idx+1) = 1; % MATLAB uses 1-indexing
        end
        button_vectors = [button_vectors; vector];
    end
    
    A = button_vectors';
    b = objective_sums';
    
    % Try integer linear programming: find integer x >= 0 such that A*x = b
    % Minimize sum(x) subject to A*x = b, x >= 0, x integer
    f = ones(size(A, 2), 1);
    lb = zeros(size(A, 2), 1);  % Lower bound: x >= 0
    
    % intlinprog requires: A_ineq, b_ineq, A_eq, b_eq, lb, ub, intcon
    intcon = 1:size(A, 2);  % All variables are integers
    [x, fval, exitflag, output] = intlinprog(f, intcon, [], [], A, b, lb, []);
    
    % Debug info
    fprintf('Exit flag: %d\n', exitflag);
    if ~isempty(x)
        fprintf('Solution found: ');
        disp(x');
        fprintf('A*x = '); disp((A*x)');
        fprintf('b = '); disp(b');
    else
        fprintf('No solution returned by intlinprog\n');
    end
    
    % Verify solution is correct
    % if ~isempty(x) && all(x >= 0)
        total = sum(x);
        overall_total = overall_total + total;
        fprintf('Solution vector: ');
        disp(x');
        fprintf('Sum of elements in solution vector: %d\n', int32(total));
    % else
        % fprintf('No valid non-negative integer solution found\n');
    % end

end