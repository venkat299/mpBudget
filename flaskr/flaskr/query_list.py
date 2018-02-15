def get_sanc():
    return """ select * from unit_dscd_ers limit 100
    """

def get_sanc_filter(filter=None):

    qs =  """ select *, unit||dscd as id from unit_dscd_ers 
    where insert_condition
    """
    if filter is not None:
        qs = qs.replace('insert_condition', filter)

    return qs


def get_sanc_filter_footer(filter=None):

    qs =  """ select count(*) count_record, sum(tot) sum_tot, sum(req) sum_req, sum(san) sum_san from (select * from unit_dscd_ers 
    where insert_condition )
    """
    if filter is not None:
        qs = qs.replace('insert_condition', filter)

    return qs