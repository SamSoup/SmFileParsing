from utils import (
    get_measures,
    get_metadata,
    get_smfile_contents, 
    prompt_user,
    write_to_file
)

dir, difficulty, chart_type, measure_start, measure_end = prompt_user()
contents = get_smfile_contents(dir)
header, measures = get_measures(contents, difficulty, chart_type)
metadata = get_metadata(contents, chart_type)

filename = f"{chart_type}-{difficulty}.sm"
write_to_file(filename, metadata, chart_type, header, measures, 
              measure_start, measure_end)
