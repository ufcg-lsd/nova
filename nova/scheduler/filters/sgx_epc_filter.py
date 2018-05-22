from oslo_log import log as logging

from nova.scheduler import filters
from nova.scheduler.filters import utils

LOG = logging.getLogger(__name__)

class SgxEpcFilter(filters.BaseHostFilter):

    run_filter_once_per_request = True

    def host_passes(self, host_state, spec_obj):
        flavor_obj = spec_obj.flavor
        extra_specs = (flavor_obj.extra_specs
                     if 'extra_specs' in flavor_obj else {})

        epc_requested = extra_specs.get('sgx:epc_size')
        if epc_requested:
            free_epc = 90 - host_state.epc_used
            if free_epc > int(epc_requested):
                return True
        return False
