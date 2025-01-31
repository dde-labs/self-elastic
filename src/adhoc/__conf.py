from dataclasses import dataclass, field
from datetime import datetime
from zoneinfo import ZoneInfo


FRAMEWORK_SCD1_COLS: tuple[str, ...] = (
    'start_dt',
    'end_dt',
    'delete_f',
    'prcs_nm',
    'prcs_ld_id',
    'asat_dt',
    'updt_prcs_nm',
    'updt_prcs_ld_id',
    'updt_asat_dt',
)
DEFAULT_DT: datetime = datetime(1990, 1, 1, tzinfo=ZoneInfo('UTC'))


@dataclass(frozen=True)
class Metadata:
    source: str
    index_nm: str
    asat_dt: str
    prcess_nm: str
    limit_rows: int = field(default=750)
    limit_workers: int = field(default=1)
    limit_slice_rows: int = field(default=250)

    @property
    def asat_dt_dash(self) -> str:
        return self.asat_dt_datetime.strftime('%Y-%m-%d')

    @property
    def asat_dt_datetime(self) -> datetime:
        return datetime.strptime(self.asat_dt, '%Y%m%d')
