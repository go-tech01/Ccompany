import requests
import uuid
import time
import json
import pandas as pd

from cv2 import cv2
import numpy as np
from PIL import Image

api_url = 'https://97a0f00d78a4498d815fd055d0c9f2be.apigw.ntruss.com/custom/v1/11970/646bea3a9ab7013e4e0292974f38e3635b695b728cd1644363ffe72ed367fe51/general'
secret_key = 'Q0JuY0dhZk1FY0pnV1JOa1BxRHpuQkVEeGJNemZGZ3Y='
construction = {'가구공사' : ['가구공사', '가구 공사'],
                '도배공사' : ['도배공사', '도배 공사'],
                '도어공사' : ['도어공사', '도어 공사'],
                '도장공사' : ['도장공사', '도장 공사'],
                '목공사' : ['목공사', '목 공사', '목공공사', '목공 공사'],
                '바닥공사' : ['바닥공사', '바닥 공사'],
                '방수공사' : ['방수공사', '방수 공사'],
                '미장공사' : ['미장공사', '미장 공사'],
                '보일러공사' : ['보일러공사', '보일러 공사'],
                '설비공사' : ['설비공사', '설비 공사'],
                '공조공사' : ['공조공사', '공조 공사'],
                '기타공사' : ['기타공사', '기타 공사'],
                '정화조공사' : ['정화조공사', '정화조 공사'],
                '샷시공사' : ['샷시공사', '샤시공사'],
                '창호공사' : ['창호공사', '창호 공사'],
                '유리공사' : ['유리공사', '유리 공사'],
                '시트공사' : ['시트공사', '시트 공사'],
                '필름공사' : ['필름공사', '필림공사'],
                '욕실공사' : ['욕실공사', '욕실 공사'],
                '도기공사' : ['도기공사', '도기 공사'],
                '수전공사' : ['수전공사', '수전 공사'],
                '조적공사' : ['조적공사', '조적 공사'],
                '타일공사' : ['타일공사', '타일 공사'],
                '전기공사' : ['전기공사', '전기 공사'],
                '조명공사' : ['조명공사', '조명 공사'],
                '철거공사' : ['철거공사', '철거 공사'],
                '판넬공사' : ['판넬공사', '판넬 공사'],
                '확장공사' : ['확장공사', '확장 공사'],
               }
evaluation_list = ['화장실공사','바닥공사','도배공사']
code = [i for i in range(100,3000)]       # 공사 코드 [100~2999]
error = 15
# 공사 대분류 - 소분류
toilet_constructions = ['욕실공사', '도기공사', '수전공사', '조적공사', '타일공사']
class Process():
    def __init__(self, input_estimateimage, area):
        self.area = area
        global final_construction_dict, final_detail_dict, final_df, del_list
        image_path = 'media/' + str(input_estimateimage)
        image_1 = Image.open(image_path)
        image = np.array(image_1)
        gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        th1, img_bin = cv2.threshold(gray_scale, 150, 225, cv2.THRESH_BINARY)

        img_bin = ~img_bin

        line_min_width = 15

        kernal_h = np.ones((1, line_min_width), np.uint8)
        kernal_v = np.ones((line_min_width, 1), np.uint8)

        img_bin_h = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_h)

        img_bin_v = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_v)

        img_bin_final = img_bin_h | img_bin_v

        final_kernel = np.ones((3, 3), np.uint8)
        img_bin_final = cv2.dilate(img_bin_final, final_kernel, iterations=1)

        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8,
                                                                         ltype=cv2.CV_32S)

        y_list = []
        for i in range(len(stats)):
            y_list.append(stats[i][1])

        a_list = []
        b_list = []
        c_list = []
        for a, b, c in list(zip(y_list, y_list[1:], y_list[2:])):
            a_list.append(a)
            b_list.append(b)
            c_list.append(c)

        table_error = 5
        last_idx = []
        for i in range(len(y_list) - 2):
            if a_list[i] != b_list[i] != c_list[i] and abs(a_list[i] - b_list[i]) > table_error and abs(
                    b_list[i] - c_list[i]) > table_error:
                last_idx.append(i)

        want_idx = []
        for r in range(len(last_idx) - 1):
            if last_idx[r + 1] - last_idx[r] < table_error * 4:
                pass
            else:
                want_idx.append(last_idx[r + 1])
        result = stats[want_idx[0]]

        X = result[0]
        Y = result[1]
        W = result[2]
        H = result[3]

        cropped_img = image[0: (Y + H), 0: (X + W)]
        # cv2.imwrite('../media/cropped_img2.jpg', cropped_img)
        im = Image.fromarray(cropped_img)
        im = im.convert("RGB")
        im.save('media/cropped_img_1.jpg')

        input_file = 'media/cropped_img_1.jpg'
        request_json = {'images': [{'format': 'jpg',
                                    'name': 'demo'}],
                        'requestId': str(uuid.uuid4()),
                        'version': 'V1',
                        'timestamp': int(round(time.time() * 1000))}
        payload = {'message': json.dumps(request_json).encode('UTF-8')}
        files = [('file', open(input_file, 'rb'))]
        headers = {'X-OCR-SECRET': secret_key}
        response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
        res = json.loads(response.text.encode('utf8'))
        # 전처리
        res_images = res['images']
        res_fields = res_images[0]['fields']
        inferText = []                                            # self.inferText 라고 해주어야 하나 ???
        y_vertices = []
        for field in res_fields:
            inferText.append(field['inferText'])
            vertices = field['boundingPoly']['vertices']
            y_vertice = (vertices[0]['y'] + vertices[1]['y'] + vertices[2]['y'] + vertices[3]['y']) / 4
            y_vertices.append(y_vertice)
        text_to_y_dict = {}
        for i in range(len(res_fields)):
            text_to_y_dict[inferText[i] + '-' + str(i).zfill(3)] = y_vertices[i]
        # 데이터화
        construction_dict = {}  # construction_dict >> {특정 공사 : y좌표}
        detail_dict = {}  # detail_dict >> {최종 금액 detail 부분 : y좌표}
        final_construction_dict = {}
        final_detail_dict = {}
        last_y_vertice = 0
        # construction_dict 만드는 과정
        for text, y_vertice in text_to_y_dict.items():
            for construct_name, construct_names in construction.items():
                if text[:-4].replace(' ', '') in construct_names:  # replace() : OCR 변환한 문자열들 공백 없애기
                    if construct_name not in construction_dict.keys():
                        construction_dict[construct_name] = [y_vertice]
                    else:
                        construction_dict[construct_name].append(y_vertice)  # {'도장 공사' : [90.0, 150.2]}
                    last_y_vertice = y_vertice
        # detail_dict 만드는 과정
        for text, y_vertice in text_to_y_dict.items():
            if y_vertice > last_y_vertice + error:
                text = text[:-4].replace(',', '')
                text = text.replace('.', '')
                try:
                    int(text)
                    if int(text) not in code and 1000 < int(text):
                        expense = int(text)
                        detail_dict[expense] = y_vertice  # {28000000 : 850.0}
                except ValueError:
                    continue
        # final_construction_dict 만드는 과정
        for construct_name, y_coordinates in construction_dict.items():
            for y_coordinate in y_coordinates:
                for text, y_vertice in text_to_y_dict.items():
                    if y_vertice >= y_coordinate - error and y_vertice <= y_coordinate + error:
                        text = text[:-4].replace(',', '')
                        text = text.replace('.', '')
                        try:
                            int(text)
                            if int(text) not in code:
                                expense = int(text)
                                if construct_name not in final_construction_dict.keys():
                                    final_construction_dict[construct_name] = expense  # {'도장공사' : 8000000}
                                else:
                                    if final_construction_dict[construct_name] != expense:  # 금액이 같을 경우 중복된 값일 가능성이 크므로 무시
                                        final_construction_dict[construct_name] += expense  # 도장공사가 2개 이상 있다면 금액을 합치는 과정
                        except ValueError:
                            continue
        # final_construction_dict에서 공사 합치는 과정 (우선 화장실공사만 해당)
        del_list = []
        for toilet_construction in toilet_constructions:
            if toilet_construction in final_construction_dict.keys():
                if '화장실공사' not in final_construction_dict.keys():
                    final_construction_dict['화장실공사'] = final_construction_dict[toilet_construction]
                    del_list.append(toilet_construction)
                    del final_construction_dict[toilet_construction]
                else:
                    final_construction_dict['화장실공사'] += final_construction_dict[toilet_construction]
                    del_list.append(toilet_construction)
                    del final_construction_dict[toilet_construction]
        # final_detail_dict 만드는 과정
        for expense, expense_y_vertice in detail_dict.items():
            expense_corr_list = []  # 금액과 같은 높이에 있는 항목들 리스트
            for text, y_vertice in text_to_y_dict.items():
                if y_vertice >= expense_y_vertice - error and y_vertice <= expense_y_vertice + error:
                    if text[:-4].replace(',', '') != str(expense) and text[:-4] != '원':
                        text = text[:-4].replace(' ','')
                        expense_corr_list.append(text)
            expense_corr = ''.join(expense_corr_list)
            final_detail_dict[expense_corr] = expense  # {'공사비' : 16000000}
        # 두 딕셔너리 합쳐서 final_dict 만들기
        final_dict = dict(final_construction_dict, **final_detail_dict)
        # DataFrame화
        final_df = pd.DataFrame(final_dict.items())

    def df(self):
        return final_df.to_html()

    def construction(self):
        construction_evaluation_dict = {}
        construction_evaluation = []
        construction_evaluation.append(f'* 평당 공사비는 {final_df.iloc[:,1].max() / self.area:,.0f}원입니다.\n')
        for key, value in final_construction_dict.items():
            if key in evaluation_list:
                construction_evaluation_dict[key] = value
        for key, value in construction_evaluation_dict.items():
            if key == "화장실공사":
                if len(del_list) == 1 and del_list[0] == '타일공사':
                    pass
                else:
                    construction_evaluation.append(f'* 평가가능 항목인 {key}{del_list}가 존재합니다')
                    if '타일공사' in del_list:
                        toilet_cost = (final_construction_dict[key] - 600000) / max(1, del_list.count('수전공사'))
                    else:
                        toilet_cost = final_construction_dict[key]
                    construction_evaluation.append(f'화장실공사의 비용은 {toilet_cost:,.0f}원입니다.')
                    if 2200000 <= toilet_cost <= 3200000:
                        construction_evaluation.append("화장실공사가 적절한 비용으로 판단됩니다.")
                    elif toilet_cost < 2200000:
                        construction_evaluation.append("화장실공사가 다소 저렴한 편입니다. 세부사항을 확인해보세요")
                    elif 3200000 < toilet_cost:
                        construction_evaluation.append("화장실공사가 다소 비싼 편입니다. 세부사항을 확인해보세요")
                    construction_evaluation.append("\n")
            if key == "바닥공사":
                construction_evaluation.append(f'* 평가가능 항목인 {key}가 존재합니다')
                cost_per_area = final_construction_dict[key] / self.area
                construction_evaluation.append(f'바닥공사의 평단가는 {cost_per_area:,.0f}원입니다.')
                if 35000 <= cost_per_area <= 50000:
                    construction_evaluation.append("바닥공사가 장판이라면 적절한 비용으로 판단됩니다. 세부사항이 장판인지 확인해보세요")
                elif 100000 <= cost_per_area <= 120000:
                    construction_evaluation.append("바닥공사가 마루라면 적절한 비용으로 판단됩니다. 세부사항이 마루인지 확인해보세요")
                elif 50000 < cost_per_area < 100000:
                    construction_evaluation.append("세부사항이 장판인지 마루인지 확인해보세요. 장판이라면 다소 비용이 높은 편이고, 마루라면 저렴한 편입니다.")
                elif cost_per_area < 50000:
                    construction_evaluation.append("바닥공사가 다소 저렴한 편입니다. 세부사항을 확인해보세요")
                elif 120000 < cost_per_area:
                    construction_evaluation.append("바닥공사가 다소 비싼 편입니다. 세부사항을 확인해보세요")
                construction_evaluation.append("\n")
            if key == "도배공사":
                construction_evaluation.append(f'* 평가가능 항목인 {key}가 존재합니다')
                cost_per_area = final_construction_dict[key] / self.area
                construction_evaluation.append(f'도배공사의 평단가는 {cost_per_area:,.0f}원입니다.')
                if 40000 <= cost_per_area <= 60000:
                    construction_evaluation.append("도배공사가 합지라면 적절한 비용으로 판단됩니다. 세부사항이 합지인지 확인해보세요")
                elif 60000 < cost_per_area <= 85000:
                    construction_evaluation.append("도배공사가 실크라면 적절한 비용으로 판단됩니다. 세부사항이 실크인지 확인해보세요")
                elif cost_per_area < 40000:
                    construction_evaluation.append("도배공사가 다소 저렴한 편입니다. 세부사항을 확인해보세요")
                elif 85000 < cost_per_area:
                    construction_evaluation.append("도배공사가 다소 비싼 편입니다. 세부사항을 확인해보세요")
                construction_evaluation.append("\n")
        return construction_evaluation

    def detail(self):
        detail_evaluation = []
        # final_construction_dict, final_detail_dict, final_df = self.gennerate()
        total_expense = sum(final_construction_dict.values())
        for expense_corr, expense in final_detail_dict.items():
            if round(expense,-1) == round(total_expense,-1):
                순공사비 = expense_corr
                detail_evaluation.append(f'* {expense_corr} 존재하므로 평가 가능합니다\n')
                break
        try:
            print(순공사비)
            for expense_corr, expense in final_detail_dict.items():
                if "이윤" in expense_corr:
                    i = expense / total_expense * 100
                    detail_evaluation.append(f'* {expense_corr}는 공사비의 {i:.2f}%입니다\n')
                elif "산재보" in expense_corr:
                    i = expense / total_expense * 100
                    detail_evaluation.append(f'* 산재보험료는 공사비의 {i:.2f}%입니다')
                    if total_expense * 100 > 50000000:
                        detail_evaluation.append("(공사비용이 5천만원미만이므로 적절하지 못합니다)\n")
                    else:
                        detail_evaluation.append("\n")
                elif "산재고용" in expense_corr:
                    i = expense / total_expense * 100
                    detail_evaluation.append(f'* 산재고용보험료는 공사비의 {i:.2f}%입니다')
                    if total_expense * 100 > 50000000:
                        detail_evaluation.append("(공사비용이 5천만원미만이므로 적절하지 못합니다)\n")
                    else:
                        detail_evaluation.append("\n")
                elif "고용보" in expense_corr:
                    i = expense / total_expense * 100
                    detail_evaluation.append(f'* 고용보험료는 공사비의 {i:.2f}%입니다')
                    #             detail_evaluation.append(f'{expense_corr}.는 공사비의 {i:.2f}%입니다\n')
                    if total_expense * 100 > 50000000:
                        detail_evaluation.append("(공사비용이 5천만원미만이므로 적절하지 못합니다)\n")
                    else:
                        detail_evaluation.append("\n")
                elif 1000 < expense < total_expense * 0.10 and "단수" not in expense_corr:
                    i = expense / total_expense * 100
                    detail_evaluation.append(f'* 그 외 추가 비용 검토해보세요: {expense_corr}는 공사비의 {i:.2f}%입니다.\n')
        except:
            detail_evaluation.append('* 평가할 수 없습니다. 검토필요')
        return detail_evaluation