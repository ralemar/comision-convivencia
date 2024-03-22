from . import settings as S
from . import io
from datetime import timedelta
import shutil

def make_report_dirs(notification_date):

    formatted_date = notification_date.strftime("%y%m%d")
    general_reports_dir_path = S.OUTPUTS_PATH / formatted_date
    if general_reports_dir_path.exists():
        shutil.rmtree(general_reports_dir_path)
    # Careful, this line could trigger an error if an old file is open.
    general_reports_dir_path.mkdir(parents=True, exist_ok=True)
    tardy_reports_dir_path = general_reports_dir_path / S.TARDIES_SUBDIR
    tardy_reports_dir_path.mkdir(parents=True, exist_ok=True)
    colors_reports_dir_path = general_reports_dir_path / S.COLORS_SUBDIR
    colors_reports_dir_path.mkdir(parents=True, exist_ok=True)


def copy_temporal_files():

    # Copy template files into tmp folder
    src_filepath = S.NOTIFICATION_PATH / "template.typ"
    tmp_filepath = S.TMP_PATH / "template.typ"
    tmp_filepath.write_text(src_filepath.read_text())
    src_filepath = S.NOTIFICATION_PATH / "logo.jpg"
    tmp_filepath = S.TMP_PATH / "logo.jpg"
    tmp_filepath.write_bytes(src_filepath.read_bytes())


def load_data():

    # Load all the data
    dfs = io.load_all_dfs()
    all_dates = io.read_all_dates()
    checkpoint = io.read_checkpoint()
    proceeding_dates = io.read_proceeding_dates()

    notification_date = all_dates[checkpoint] + timedelta(days=1)

    # Create the folders as needed
    make_report_dirs(notification_date)

    # Copy required temp files
    copy_temporal_files()

    return dfs, all_dates, checkpoint, proceeding_dates