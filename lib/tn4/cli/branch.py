import os
import sys

from tn4.cli.base import CommandBase
from tn4.doctor.branch import BranchInfo, Branch


class BranchVlan(CommandBase):
    def __init__(self, args):
        self.netbox_url    = args.netbox_url
        self.netbox_token  = args.netbox_token
        self.flg_debug     = args.debug
        self.flg_use_cache = args.use_cache

        self.flg_add       = args.add
        self.flg_delete    = args.delete

        if self.flg_add:
            self.branch_info = BranchInfo(
                args.vlan_name, args.vrrp_group_id,
                args.cidr_prefix, args.vrrp_master_ip, args.vrrp_backup_ip, args.vrrp_vip,
                args.cidr_prefix6, args.vrrp_master_ip6, args.vrrp_backup_ip6, args.vrrp_vip6,
            )

        if self.flg_delete:
            self.branch_info = BranchInfo(args.vlan_name)


    def exec_add(self):
        with self.console.status(f"[green]Creating new branch [b]{self.branch.vlan_name}[/b]..."):

            i, n = 1, 9
            ok = self.branch.commit_branch_id()
            self.console.log(f"[yellow]Updated VLAN metadata [dim]({i} of {n})")

            # i += 1
            # ok = self.branch.add_branch_prefix()
            # self.console.log(f"[yellow]Added new prefix [dim]({i} of {n})")

            # i += 1
            # ok = self.branch.add_vrrp_ip_address()
            # self.console.log(f"[yellow]Added new IP address [dim]({i} of {n})")

            # i += 1
            # ok = self.branch.add_vrrp_and_bind_ip_address()
            # self.console.log(f"[yellow]Added new FHRP Group binding the IP addresses [dim]({i} of {n})")


    def exec_delete(self):
        pass


    def exec(self):
        ok = self.fetch_inventory(
            netbox_url=self.netbox_url, netbox_token=self.netbox_token,
            use_cache=self.flg_use_cache, debug=self.flg_debug, fetch_all=True
        )

        if not ok:
            return 100

        self.branch = Branch(self.ctx, self.nb.cli, self.branch_info)

        if self.branch.vlan_id is None:
            self.console.log(f"[red]VLAN [b]{self.branch.vlan_name}[/b] not found. Aborted.")
            return 100

        self.console.log(
            f"[yellow]Found VLAN [b]{self.branch.info.vlan_name}[/b] "
            f"[dim]VLAN ID: {self.branch.info.vlan_vid}, Branch ID: {self.branch.info.tn4_branch_id}"
        )

        if self.flg_add:
            return self.exec_add()

        if self.flg_delete:
            return self.exec_delete()

