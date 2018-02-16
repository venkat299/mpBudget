def get_sanc():
    return """ select * from unit_dscd_ers limit 100
    """

def get_desg_summ():
    return """ select gcd, cadre,discp,d5,desig,dscd,grade,ifnull(sum(tot),0) tot, ifnull(sum(req),0) req, ifnull(sum(san),0) san from unit_dscd_ers group by dscd order by discp,d5, gcd
    """

def get_desg_area_unit_summ():
    return """ select gdesig, gcd,name, area,unit, discp,d5,desig,dscd,grade,ifnull(sum(tot),0) tot, ifnull(sum(req),0) req, ifnull(sum(san),0) san from unit_dscd_ers where dscd like ? group by area,unit order by discp,d5, gcd
    """

def get_area_unit_summ():
    return """ select area,unit,name,type,ifnull(sum(tot),0) tot, ifnull(sum(req),0) req, ifnull(sum(san),0) san from unit_dscd_ers group by area, unit order by discp,d5, gcd
    """

def get_total_footer():
    return """ select area,unit,name,type,ifnull(sum(tot),0) tot, ifnull(sum(req),0) req, ifnull(sum(san),0) san from unit_dscd_ers 
    """

def get_sanc_filter(filter=None):

    # qs =  """ select type,area,unit,name,d5,discp,dscd,desig,grade,sum(tot) tot, sum(req) req,sum(san) san, remark, unit||dscd as id from unit_dscd_ers 
    # where insert_condition
    # """
    qs =  """ select  *, unit||dscd as id from unit_dscd_ers 
    where insert_condition
    """
    if filter is not None:
        qs = qs.replace('insert_condition', filter)

    return qs


def get_sanc_filter_footer(filter=None):

    qs =  """ select count(*) count_record, sum(tot) tot, sum(req) req, sum(san) san from (select * from unit_dscd_ers 
    where insert_condition )
    """
    if filter is not None:
        qs = qs.replace('insert_condition', filter)

    return qs