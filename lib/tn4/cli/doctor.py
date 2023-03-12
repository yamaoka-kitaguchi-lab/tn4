from pprint import pprint
from datetime import datetime
import time
import os

from tn4.cli.base import CommandBase
from tn4.doctor.diagnose import Diagnose


class Doctor(CommandBase):
    def __init__(self, args):
        self.netbox_url   = args.netbox_url
        self.netbox_token = args.netbox_token

        self.flg_diagnosis_only = args.diagnosis_only
        self.flg_force_repair   = args.force_repair
        self.flg_use_cache      = args.use_cache
        self.flg_debug          = args.debug

        n = datetime.now()
        ts = n.strftime("%Y-%m-%d@%H-%M-%S")
        self.snapshot_basedir = f"{self.workdir_path}/project/snapshots/config.{ts}"


    def exec(self):
        ok = self.fetch_inventory(
            netbox_url=self.netbox_url, netbox_token=self.netbox_token,
            use_cache=self.flg_use_cache, debug=self.flg_debug
        )

        if not ok:
            return 100

        diag = Diagnose(self.ctx)

        with self.console.status(f"[green]Scanning NetBox and checking consistency..."):
            diag.check_tag_to_tag_consistency()
            self.console.log(f"[yellow]Checked inter-tag consistency")

        if self.flg_diagnosis_only:
            return 0

        return 0
