import datetime
import json


def res_file(name, clas, res):
    key = f"{name} {clas}"
    time_dict = {key: res}
    time = str(datetime.date.today())[5:]
    with open('result.json', encoding='utf-8') as f:
        data = json.load(f)
        if time in data:
            data[time].update(time_dict)
            with open('result.json', 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=2)
        else:
            with open('result.json', 'w', encoding='utf-8') as outfile:
                json.dump({str(time)[5:]: time_dict}, outfile, ensure_ascii=False, indent=2)
    # time = datetime.date.today()
    # json_dict = {str(time)[5:]: time_dict}

    # with open('result.json') as f:
    #     templates = json.load(f)
    # with open('result.json', 'w') as file:
    #     json.dump(json_dict, file)



