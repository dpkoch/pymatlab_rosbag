function matlab = python2matlab(python)
%PYTHON2MATLAB Recursively convert python data types to matlab data types
    switch class(python)
        case class(py.dict)
            matlab = struct(python);
            names = fieldnames(matlab);
            for i=1:length(names)
                matlab.(names{i}) = python2matlab(matlab.(names{i}));
            end
        case class(py.list)
            raw = cell(python);
            try
                matlab = cellfun(@double, raw).';
            catch
                matlab = cellfun(@char, raw, 'UniformOutput', false).';
            end
        case class(py.str)
            matlab = char(python);
        otherwise
            if isnumeric(python) || islogical(python)
                matlab = python;
            else
                error('Encountered unsupported python type ''%s''', class(python))
            end
    end
end
