"""

SM file Wiki Help: https://github-wiki-see.page/m/stepmania/stepmania/wiki/sm
"""
from utils import (
    get_measures,
    get_metadata,
    get_smfile_contents, 
    prompt_user,
    update_metadata,
    write_to_file
)

dir, difficulty, chart_type, measure_start, measure_end = prompt_user()
contents = get_smfile_contents(dir)
header, measures = get_measures(contents, difficulty, chart_type)
metadata = get_metadata(contents)
# recompute bpm and stop header tag information
metadata = update_metadata(metadata, measure_start, measure_end)
filename = f"{chart_type}-{difficulty}.sm"
write_to_file(filename, metadata, chart_type, header, measures, 
              measure_start, measure_end)
