import numpy as np
def metered_energy_payment(da_mp, da_se, rt_mp, mgo):
    # da_mp : 하루전 에너지 가격. 거래시간은 총 24개. 원/kWh.
    # da_se : 하루전 에너지 계획량. MWh.
    # rt_mp : 실시간 에너지 가격. 거래시간 각 구간별 거래단위 변화 없다고 가정하고, 거래시간 총 24개로 구성. 원/kWh.
    # mgo : 거래 시간별 계량값 (== 실제 발전한 량). MWh.

    if len(da_mp) != 24 or len(da_se) != 24 or len(rt_mp) != 24 or len(mgo) != 24:
        raise Exception('잘못된 입력입니다.')

    np_da_mp = np.array(da_mp)
    np_da_se = np.array(da_se)
    np_rt_mp = np.array(rt_mp)
    np_mgo = np.array(mgo)

    return np.dot(np_da_mp, np_da_se) * 1000 + np.dot(np_rt_mp, (np_mgo - np_da_se)) * 1000