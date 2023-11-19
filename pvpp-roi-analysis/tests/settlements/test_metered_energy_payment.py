import unittest
from src.settlements import metered_energy_payment
import numpy as np


class TestMeteredEnergyPayment(unittest.TestCase):

    def test_metered_energy_payment_correct_input(self):
        # 정상적인 입력값
        da_mp = [10] * 24
        da_se = [5] * 24
        rt_mp = [20] * 24
        mgo = [6] * 24

        print(da_mp)

        # 예상 결과 계산
        expected = np.array(da_mp) * np.array(da_se) * 1000 + np.array(rt_mp) * (np.array(mgo) - np.array(da_se)) * 1000

        # 함수 실행
        result = metered_energy_payment(da_mp, da_se, rt_mp, mgo)

        # np.allclose를 사용하여 배열 비교
        self.assertTrue(np.allclose(result, expected),
                        "The metered energy payment calculation did not match the expected result.")

    def test_metered_energy_payment_incorrect_input_length(self):
        # 잘못된 입력값 (길이가 24가 아님)
        da_mp = [10] * 23
        da_se = [5] * 23
        rt_mp = [20] * 23
        mgo = [6] * 23

        # 예외 발생 여부 확인
        with self.assertRaises(Exception):
            metered_energy_payment(da_mp, da_se, rt_mp, mgo)


# unittest를 실행
if __name__ == '__main__':
    unittest.main()
