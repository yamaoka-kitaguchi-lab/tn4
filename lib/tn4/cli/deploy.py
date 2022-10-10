from tn4.cli.base import CommandBase


class Deploy(CommandBase):
    def __init__(self, args):
        self.flg_use_cache        = args.use_cache
        self.flg_test             = args.test
        self.flg_dryrun           = args.dryrun
        self.flg_debug            = args.debug
        self.custom_template_path = args.template
        self.fetch_inventory_opt = [
            args.hosts, args.no_hosts, args.areas, args.no_areas, args.roles, args.no_roles,
            args.vendors, args.no_vendors, args.tags, args.no_tags, args.use_cache, args.test,
        ]


    def exec(self):
        return 0
