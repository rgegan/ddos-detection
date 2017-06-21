"""Features:
    No. of TCP/UDP/ICMP/etc. pkts per destination ip
    No. of TCP/UDP/ICMP/etc. bytes per destination ip
    TCP SYN ratio per destination ip
"""
from nfreader import FIELDS

# Field column index.
idx_sa = FIELDS.index('sa')
idx_da = FIELDS.index('da')
idx_ipkt = FIELDS.index('ipkt')
idx_ibyt = FIELDS.index('ibyt')
idx_pr = FIELDS.index('pr')
idx_flg = FIELDS.index('flg')

def get_pr_pkts(records, protocol):
    """No. of pkts of a particular protocol toward dst_ip."""
    # A dictionary
    # key: dst_ip
    # values: No. of TCP/UDP/ICMP/etc. pkts toward dst_ip captured within this time interval.
    results = {}
    for record in records:
        da, ipkt, pr = record[idx_da], record[idx_ipkt], record[idx_pr]
        if not da in results:
            results[da] = 0
        if pr == protocol:
            # Remove amplification of 1:1000 sampling.
            results[da] += ipkt / 1000
    return results

def get_pr_byts(records, protocol):
    """No. of bytes of a particular protocol toward dst_ip."""
    # A dictionary
    # key: dst_ip
    # values: No. of TCP/UDP/ICMP/etc/ bytes toward dst_ip captured within this time interval.
    results = {}
    for record in records:
        da, ibyt, pr = record[idx_da], record[idx_ibyt], record[idx_pr]
        if not da in results:
            results[da] = 0
        if pr == protocol:
            results[da] += ibyt / 1000
    return results

def get_tcp_syn_ratio(records):
    """TCP SYN ratio."""
    # A dictionary
    # key: dst_ip
    # values: TCP SYN ratio per destination ip.
    tmp_results = {}
    for record in records:
        da, ipkt, pr, flg = record[idx_da], record[idx_ipkt], record[idx_pr], record[idx_flg]
        if not da in results:
            tmp_results[da] = {}
            tmp_results[da]['TCP'] = 0
            tmp_results[da]['TCP-SYN'] = 0
        if pr == "TCP":
            tmp_results[da]['TCP'] += ipkt / 1000
        if flg == '....S.':
            tmp_results[da]['TCP-SYN'] += ipkt / 1000
    
    results = {}
    for da in tmp_results:
        if tmp_results[da]['TCP'] == 0:
            results[da] = 0
        else:
            results[da] = tmp_results[da]['TCP-SYN'] / tmp_results[da]['TCP']
    return results


