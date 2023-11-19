import numpy as np
def market_whole_payment(da_mp, da_se, rt_mp, mgo, set_point, ra, e_allowed, op_gen, rt_op, xsof):
    # da_mp : 하루전 에너지 가격. 거래시간은 총 24개. 원/kWh.
    # da_se : 하루전 에너지 계획량. MWh.
    # rt_mp : 실시간 에너지 가격. 거래시간 각 구간별 거래단위 변화 없다고 가정하고, 거래시간 총 24개로 구성. 원/kWh.
    # mgo : 거래 시간별 계량값 (== 실제 발전한 량). MWh.
    # set_point : 전력거래소의 급전지시량. da_se 와 같을 수도, 다를 수도 있음.
    # ra : 거래시간별 변경 공급가능용량. MWh.
    # e_allowed : 거래시간별 허용오차. MWh. 설비용량 x 0.08.
    # rt_op : 실시간 시장 입찰 구간별 (MW) 입찰가격. 원/kWh. 실시간입찰은 기본적으로 하루전시장입찰가와 같음.
    # xsof : 공급가능용량 초과 급전지시 여부. 1 이면 초과 급전지시, 그렇지 않을 경우 0.

    if (len(da_mp) != 24 or len(da_se) != 24 or len(rt_mp) != 24
            or len(mgo) != 24 or len(set_point) != 24 or len(ra) != 24
            or len(e_allowed) != 24) :
        raise Exception('잘못된 입력입니다. 모든 입력은 24시간 단위로 존재해야 합니다.')

    row_lens_op_gen = [len(row) for row in op_gen]
    row_lens_rt_op = [len(row) for row in rt_op]

    if (len(row_lens_op_gen) != 24 or
            len(row_lens_rt_op) != 24):
        raise Exception('잘못된 입력입니다. 입찰용량 및 입찰가격은 24시간 단위로 존재해야 합니다.')

    for row_len in row_lens_op_gen:
        if row_len != 10:
            raise Exception('잘못된 입력입니다. 입찰용량 구간은 10개 입니다.')

    for row_len in row_lens_rt_op:
        if row_len != 10:
            raise Exception('잘못된 입력입니다. 실시간입찰가 구간은 입찰용량 구간과 같은 10개 입니다.')

    if xsof != 0 and xsof != 1:
        raise Exception('잘못된 입력입니다. 초과급전여부를 뜻하는 XSOF 는 0 또는 1입니다.')

    np_da_mp = np.array(da_mp)
    np_da_se = np.array(da_se)
    np_rt_mp = np.array(rt_mp)
    np_mgo = np.array(mgo)
    np_set_point = np.array(set_point)
    np_ra = np.array(ra)
    np_e_allowed = np.array(e_allowed)

    # 중간에 사용되는 변경값들
    np_ra_with_e_allowed = np_ra + np_e_allowed
    np_set_point_with_e_allowed = np_set_point + np_e_allowed

    # SCMWG : 변동비보전정산금지급영역에 대한 변동비(원) 계산
    # 각 거래시간 별 offered_price 및 적분 구간을 적용한 scmwg 계산
    if xsof == 0:
        scmwg_upper_bound = np.minimum.reduce([np_mgo, np_ra_with_e_allowed, np_set_point_with_e_allowed])
    else:
        scmwg_upper_bound = np_mgo

    scmwg_array = []
    for ub_index, value in enumerate(scmwg_upper_bound):
        dynamic_cost_sum = 0
        last_in_capa = 0
        for op_gen_index, in_capa in enumerate(op_gen[ub_index]):
            if in_capa < value:
                dynamic_cost_sum = dynamic_cost_sum + in_capa * rt_op[ub_index][op_gen_index]
                last_in_capa = in_capa
            else:
                dynamic_cost_sum = dynamic_cost_sum + (value - last_in_capa) * rt_op[ub_index][op_gen_index]
        scmwg_array.append(dynamic_cost_sum)

    # MPMWG : 변동비보전정산금지급영역에 대한 에너지정산금(원) 계산
    mpmwg_array = np_da_se * np_da_mp * 1000 + np_rt_mp * (scmwg_upper_bound - da_se) * 1000

    return max(np.sum(np.array(scmwg_array) - mpmwg_array), 0)